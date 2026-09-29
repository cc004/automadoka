"""Python implementation of the recognized loader's packet codec.

Transcribed from the matching 3.16.1/3.19.1 loader: encrypted packet headers,
AES-256-CBC, and its prefix-coded literal/repeat/back-reference stream.
No ARM emulator or executable decoder core is used.
"""
import struct
from Crypto.Cipher import AES

MASK = 0xffffffff


def _gf(value):
    factor, result = 0x94511dd2, 0
    while factor:
        if factor & 1: result ^= value
        high = value >> 31
        value = (value << 1) & MASK
        if high: value ^= 0x579357eb
        factor >>= 1
    return result


_GF = tuple(tuple(_gf(x << shift) for x in range(256)) for shift in (0, 8, 16, 24))


def gf(value):
    return _GF[0][value & 255] ^ _GF[1][value >> 8 & 255] ^ _GF[2][value >> 16 & 255] ^ _GF[3][value >> 24 & 255]


class DecodeError(ValueError):
    pass


def bounded(data, offset, size):
    if offset < 0 or size < 0 or offset + size > len(data):
        raise DecodeError('Packet range outside input: %x + %x' % (offset, size))
    return data[offset:offset + size]


def aes_key(schedule):
    if len(schedule) != 244 or schedule[:4] != b'\x00\x01\x0e\x00':
        raise DecodeError('Unknown AES schedule format')
    words = b''.join(x.to_bytes(4, 'big') for x in struct.unpack('<60I', schedule[4:]))
    def xt(x): return ((x << 1) ^ (0x11b if x & 128 else 0)) & 255
    second = bytearray()
    for i in range(208, 224, 4):
        x, y, z, w = words[i:i + 4]
        t = x ^ y ^ z ^ w
        second.extend((x ^ t ^ xt(x ^ y), y ^ t ^ xt(y ^ z), z ^ t ^ xt(z ^ w), w ^ t ^ xt(w ^ x)))
    return words[224:240] + second


def decrypt_words(data, seed):
    result = bytearray(data)
    key, v1, v2 = seed, 0x07b48238, 0xe34eac63
    for i in range(len(data) // 4):
        v1 = (((v1 + 0xe9fa57e4) * v1 + key + 0x8e495673) << (i & 7)) & MASK
        v2 = (((v2 + 0x4f8b1bca) * v2 + key + 0x72f6fcbe) & MASK) >> ((i * i) & 15)
        key = v1 ^ v2
        raw = struct.unpack_from('<I', result, i * 4)[0]
        value = ((raw + (i & 13) * 0xb43b9baf) & MASK) ^ (((i & 3) * 0xaf57f7fb) & MASK)
        struct.pack_into('<I', result, i * 4, ((value - key) & MASK) ^ key)
    return bytes(result)


def decompress(data, expected, table):
    if len(data) == expected: return data
    output = bytearray()
    padded = data + b'\0' * 4
    bit_position = prefix = 0
    while len(output) < expected:
        if bit_position >= len(data) * 8: raise DecodeError('Truncated compressed stream')
        value = struct.unpack_from('<I', padded, bit_position >> 3)[0] >> (bit_position & 7)
        entry, bits = table[value & 255]
        if not entry & 0x8000:
            bits += 1
            while True:
                if bits > 24: raise DecodeError('Invalid prefix tree depth')
                index = (entry & 0x7fff) + ((value >> (bits - 1)) & 1)
                if index >= len(table): raise DecodeError('Invalid prefix tree link')
                entry, _ = table[index]
                if entry & 0x8000: break
                bits += 1
        if not 0 < bits <= 24: raise DecodeError('Invalid prefix code length')
        bit_position += bits
        if bit_position > len(data) * 8: raise DecodeError('Truncated prefix code')
        symbol = entry & 0x7fff
        kind, value = symbol & 0x300, symbol & 255
        if kind == 0:
            output.append(value)
        elif kind == 0x100:
            if prefix > 255: raise DecodeError('Oversized length prefix')
            prefix = (prefix << 8) | value
        elif kind == 0x200:
            if value not in (1, 2, 4) or len(output) < value:
                raise DecodeError('Invalid repeated pattern')
            length = value * (prefix or 1)
            if len(output) + length > expected: raise DecodeError('Repeated pattern exceeds output')
            output.extend(output[-value:] * (prefix or 1))
            prefix = 0
        else:
            distance = prefix + value
            if not value or distance > len(output) or len(output) + value > expected:
                raise DecodeError('Invalid back reference')
            start = len(output) - distance
            output.extend(output[start:start + value])
            prefix = 0
    if (bit_position + 7) // 8 != len(data): raise DecodeError('Unused compressed bytes')
    return bytes(output)


class Decoder:
    def configure(self, owner, payload, expected_size, wide_seed=False):
        candidates = []
        raw = struct.unpack_from('<I', payload)[0]
        for offset in range(max(0, len(owner) - 0x3000) // 4 * 4, len(owner) - 3, 4):
            seed = struct.unpack_from('<I', owner, offset)[0]
            if not seed or (not wide_seed and seed >= 0x10000): continue
            key = (((seed * seed) & MASK) >> 17) ^ (((seed * seed) << 11) & MASK)
            size = (gf(raw) + key * 0xf87b337c + (0xa21dfb3a << (key & 7))) & MASK
            if size == expected_size: candidates.append((offset, seed))
        schedules = [i for i in range(len(owner) - 243) if owner[i:i + 4] == b'\x00\x01\x0e\x00']
        if len(candidates) != 1 or len(schedules) != 1:
            raise DecodeError('Unknown or ambiguous decoder configuration')
        offset, self.seed = candidates[0]
        self.aes = aes_key(owner[schedules[0]:schedules[0] + 244])
        return {'seed_offset': offset, 'seed': self.seed, 'aes_offset': schedules[0]}

    def decode(self, data, expected_size):
        if not 0 < expected_size <= 0x20000000: raise DecodeError('Invalid decoded size')
        key = (((self.seed * self.seed) & MASK) >> 17) ^ (((self.seed * self.seed) << 11) & MASK)
        raw_size, raw_flags, raw_table_size = struct.unpack('<3I', bounded(data, 0, 12))
        size = (gf(raw_size) + key * 0xf87b337c + (0xa21dfb3a << (key & 7))) & MASK
        if size != expected_size: raise DecodeError('Decoded size does not match module header')
        flags = gf(raw_flags) ^ ((key + (0x416e2af2 >> (key & 13)) + 0xbd19c63c) & MASK)
        count = flags & 255
        skip_aes = (flags >> 8 & 255) == 1
        table_size = (gf(raw_table_size) + (0x643a3a3b << (key & 11)) - (key ^ 0x3b2bf538)) & MASK
        if not 0 < count <= 256 or not 768 <= table_size <= 0x1b00:
            raise DecodeError('Invalid packet header')
        table_data = bytearray(bounded(data, 12, table_size))
        for off in range(0, len(table_data) // 4 * 4, 4):
            struct.pack_into('<I', table_data, off, gf(struct.unpack_from('<I', table_data, off)[0]))
        for i, value in enumerate(table_data):
            adjust = gf((((key + 0xf1cb5b81) * key) << (i & 27)) & MASK)
            adjust = (adjust - (((key + 0xce18397e) * key & MASK) >> (i & 23))) & MASK
            table_data[i] = (value + (adjust >> (i & 31))) & 255
        table = [(int.from_bytes(table_data[i:i + 2], 'little'), table_data[i + 2])
                 for i in range(0, len(table_data) - 2, 3)]
        cursor = (12 + table_size + 3) & ~3
        descriptors = []
        for off in range(0, count * 8, 4):
            raw = struct.unpack('<I', bounded(data, cursor + off, 4))[0]
            value = gf(raw ^ ((((key + 0xb31f451c) * key) << ((off & 3) + 3)) & MASK))
            value = (value + (((key + 0x30ef5cef) * key & MASK) >> ((off & 7) + 5))) & MASK
            descriptors.append(value)
        output = bytearray(size)
        for offset, length in zip(descriptors[::2], descriptors[1::2]):
            block = decrypt_words(bounded(data, offset, length), self.seed)
            if not skip_aes:
                full = len(block) // 16 * 16
                block = AES.new(self.aes, AES.MODE_CBC, iv=b'\0' * 16).decrypt(block[:full]) + block[full:]
            base, chunks, entries, content = struct.unpack('<4I', bounded(block, 0, 16))
            for i in range(chunks):
                destination, unpacked, packed, _ = struct.unpack('<4I', bounded(block, entries + i * 16, 16))
                if base + destination + unpacked > size: raise DecodeError('Chunk exceeds decoded image')
                decoded = decompress(bounded(block, content, packed), unpacked, table)
                output[base + destination:base + destination + unpacked] = decoded
                content += packed
        return bytes(output)
