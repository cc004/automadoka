"""Restore the recognized ARM64 loader format, entirely within Python.

The reconstructed ELF is a static analysis artifact, never executed.
"""
import hashlib
import io
import json
import struct
from collections import Counter
from pathlib import Path

from elftools.elf.elffile import ELFFile

from .decoder import Decoder, DecodeError, MASK, bounded, gf

LOADER_SHA256 = '809eec69555fea14076b1376d6397147d81479a7ba1f27ced46de018d9cbfb36'


def unpack_words(data, key):
    output = bytearray(data)
    for i in range(len(output) // 4):
        raw = struct.unpack_from('<I', output, i * 4)[0]
        value = ((raw + (i + 3) * key) & MASK) ^ (((i + 1) * 0xbf20165d) & MASK)
        struct.pack_into('<I', output, i * 4, value)
    return bytes(output)


def locate_loader(binary, elf):
    candidates = []
    for section in elf.iter_sections():
        if section['sh_type'] != 'SHT_LOUSER': continue
        begin = section['sh_offset']
        end = begin + section['sh_size']
        bounded(binary, begin, end - begin)
        for offset in range(begin, min(end - 32, begin + 0x4000), 4):
            key = struct.unpack_from('<I', binary, offset)[0]
            if not 0 < key < 0x10000: continue
            header = list(struct.unpack('<8I', unpack_words(binary[offset:offset + 32], key)))
            header[0] = key
            start, size = header[2:4]
            if (start == 32 and 0x1000 <= size <= 0x100000 and offset + start + size <= end
                    and header[5] < size and header[6] < size and header[7] == size):
                candidates.append((offset, header))
    if len(candidates) != 1:
        raise DecodeError('Expected one protected loader header, found %d' % len(candidates))
    offset, header = candidates[0]
    start, size, key = header[2:5]
    owner = unpack_words(binary[offset + start:offset + start + size], key)
    if hashlib.sha256(owner).hexdigest() != LOADER_SHA256:
        raise DecodeError('Loader implementation changed; the Python decoder needs adaptation')
    return owner, {'header_offset': offset, 'header': header, 'data_offset': offset + ((start + size + 3) & ~3)}


def module_table(blob, module_id):
    mul = (module_id * 0x9d323cd7) & MASK
    key = ((mul >> (module_id & 7)) + 0x5e727d74 + ((mul << (module_id & 0xb)) & MASK) + 0xf71e3005) & MASK
    previous = 0xcbf0c1d8
    header = []
    for offset in range(0, 8, 4):
        raw = struct.unpack('<I', bounded(blob, offset, 4))[0]
        header.append(gf((raw + previous) & MASK) ^ (((offset + 1) * 0xebe81dba + key) & MASK))
        previous = raw
    key = (header[1] + key) & MASK
    rows = []
    for index in range(64):
        if 8 + (index + 1) * 0x5c > len(blob): break
        row = []
        previous = 0xf02f7685
        for offset in range(0, 0x5c, 4):
            raw = struct.unpack_from('<I', blob, 8 + index * 0x5c + offset)[0]
            value = gf(raw ^ (((previous * previous) & MASK) >> 3))
            value ^= ((((key + 0x96f60b71) * key) & MASK) << ((index + 1) & 3)) & MASK
            value = (value + (offset + 1) * 0x79934cf6 + key) & MASK
            value = (value - ((((key + 0x9d9b673d) * key) & MASK) >> ((offset + 3) & 5))) & MASK
            row.append(value)
            previous = raw
        if row[0] > 0x100 or row[2] > len(blob) or row[3] > len(blob): break
        rows.append(row)
    return rows


def saved_header(blob, owner, expected_size):
    candidates = []
    raw_header = struct.unpack('<23I', bounded(blob, 0, 92))
    for offset in range(max(0, len(owner) - 0x3000) // 4 * 4, len(owner) - 3, 4):
        seed = struct.unpack_from('<I', owner, offset)[0]
        if not seed: continue
        a = ((seed + 0xd3e87144) * seed) & MASK
        c = (a + seed * 0x0bd9418d) & MASK
        if ((raw_header[0] - a) & MASK) ^ (c >> (seed & 7)) != 0x9d: continue
        header = [((raw - ((a << (i * 4 & 7)) & MASK)) & MASK) ^ (c >> ((seed + i * 4) & 7))
                  for i, raw in enumerate(raw_header)]
        if header[:4] == [0x9d, 0x100, 0x5c, expected_size] and 0 < header[4] < len(blob) and header[5] > 0:
            candidates.append(header)
    if len(candidates) != 1:
        raise DecodeError('Expected one saved ELF header configuration, found %d' % len(candidates))
    return candidates[0]


def rebuild(original, memory, metadata, symbols):
    elf = ELFFile(io.BytesIO(original))
    result = bytearray(original)
    loads = [s for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD']
    report = {'recovered_memory_size': len(memory), 'segments': []}

    def file_offset(address, size=8):
        for segment in loads:
            if segment['p_vaddr'] <= address and address + size <= segment['p_vaddr'] + segment['p_memsz']:
                offset = segment['p_offset'] + address - segment['p_vaddr']
                if offset + size <= len(result): return offset
        raise DecodeError('Unmapped relocation address: %x' % address)

    for segment in loads:
        offset, address, size = segment['p_offset'], segment['p_vaddr'], segment['p_filesz']
        if address + size > len(memory) or offset + size > len(result):
            raise DecodeError('ELF segment outside recovered image')
        restored = 0
        for index, value in enumerate(memoryview(memory)[address:address + size]):
            if value:
                result[offset + index] = value
                restored += 1
        report['segments'].append({'vaddr': hex(address), 'filesize': size, 'restored_nonzero_bytes': restored})
    # Whole sections also restore zero bytes inside instructions.
    for section in elf.iter_sections():
        address, size = section['sh_addr'], section['sh_size']
        if not address or address + size > len(memory) or section['sh_type'] == 'SHT_NOBITS': continue
        recovered = memory[address:address + size]
        if any(recovered):
            offset = section['sh_offset']
            bounded(result, offset, size)
            result[offset:offset + size] = recovered
    for index, segment in enumerate(elf.iter_segments()):
        if segment['p_type'] != 'PT_LOAD' or segment['p_memsz'] == segment['p_filesz']: continue
        start = segment['p_offset'] + segment['p_filesz']
        end = segment['p_offset'] + segment['p_memsz']
        bounded(result, start, end - start)
        result[start:end] = b'\0' * (end - start)
        struct.pack_into('<Q', result, elf['e_phoff'] + index * elf['e_phentsize'] + 32, segment['p_memsz'])
    counts = Counter()
    for field in (32, 40):
        start, count = struct.unpack('<II', bounded(metadata, field, 8))
        entries = bounded(metadata, start, count * 24)
        for address, info, addend in struct.iter_unpack('<QQq', entries):
            kind = info & MASK
            counts[kind] += 1
            if kind == 1027:  # R_AARCH64_RELATIVE, image base zero
                struct.pack_into('<Q', result, file_offset(address), addend & 0xffffffffffffffff)
    data_size, _ = struct.unpack('<II', bounded(symbols, 0, 8))
    data = bounded(symbols, 8, data_size)
    count, symbol_offset, index_offset, cursor = struct.unpack('<4I', bounded(data, 0, 16))
    symtab = elf.get_section_by_name('.dynsym')
    strtab = elf.get_section_by_name('.dynstr')
    for index in range(count):
        symbol_index = struct.unpack('<I', bounded(data, index_offset + index * 4, 4))[0]
        entry = bounded(data, symbol_offset + index * 24, 24)
        if (symbol_index + 1) * 24 > symtab['sh_size']: raise DecodeError('Invalid symbol index')
        offset = symtab['sh_offset'] + symbol_index * 24
        result[offset:offset + 24] = entry
        name_offset = struct.unpack_from('<I', entry)[0]
        end = data.index(b'\0', cursor)
        name = data[cursor:end + 1]
        if name_offset + len(name) > strtab['sh_size']: raise DecodeError('Invalid symbol name offset')
        offset = strtab['sh_offset'] + name_offset
        if result[offset] == 0: result[offset:offset + len(name)] = name
        cursor = end + 1
    dynamic = elf.get_section_by_name('.dynamic')
    for offset in range(dynamic['sh_offset'], dynamic['sh_offset'] + dynamic['sh_size'], 16):
        tag, _ = struct.unpack_from('<QQ', result, offset)
        if tag in (8, 0x6ffffff9): struct.pack_into('<Q', result, offset + 8, 0)
    report.update(relocation_counts={str(k): v for k, v in counts.items()}, restored_symbols=count,
                  note='Base-zero ELF for static analysis; external imports are not resolved.')
    return result, report


def restore(run, log=print):
    run = Path(run)
    source = run / 'extracted/il2cpp/libil2cpp.so'
    output = source.with_name('libil2cpp.restored.so')
    original = source.read_bytes()
    elf = ELFFile(io.BytesIO(original))
    if elf['e_machine'] != 'EM_AARCH64' or not elf.little_endian:
        raise DecodeError('Only little-endian ARM64 ELF is supported')
    if not any(s['sh_type'] == 'SHT_LOUSER' for s in elf.iter_sections()):
        output.write_bytes(original)
        log('Unprotected ELF: no loader decoding required')
        return output
    analysis = run / 'analysis'
    analysis.mkdir(exist_ok=True)

    def save_json(name, value):
        (analysis / name).write_text(json.dumps(value, indent=2), encoding='utf-8')

    owner, info = locate_loader(original, elf)
    (analysis / 'stage2.bin').write_bytes(owner)
    save_json('stage2_info.json', info)
    blob = original[info['data_offset']:]
    decoder = Decoder()
    current_id, current_offset = 0xe2, 0
    inventory, modules = [], {}
    for depth in range(20):
        rows = module_table(blob[current_offset:], current_id)
        log('Decoding layer %x (%d modules)' % (current_id, len(rows)))
        if not rows: break
        first = next((row for row in rows if not row[1] & 2 and row[3]), None)
        if first is None: raise DecodeError('Layer has no decoder configuration sample')
        decoder.configure(owner, blob[current_offset + first[2]:], first[3])
        decoded = {}
        for row in rows:
            inventory.append({'layer': current_id, 'base_offset': current_offset, 'row': row})
            if row[1] & 2 or not row[3]: continue
            if row[0] in modules: raise DecodeError('Duplicate module ID')
            decoded[row[0]] = decoder.decode(blob[current_offset + row[2]:], row[3])
            (analysis / ('module_%x.bin' % row[0])).write_bytes(decoded[row[0]])
        modules.update(decoded)
        next_id = current_id + 1
        nested = next((row for row in rows if row[0] == next_id + 0x10 and row[1] & 2), None)
        if nested is None or next_id not in decoded: break
        owner, current_id, current_offset = decoded[next_id], next_id, current_offset + nested[2]
    else:
        raise DecodeError('Too many nested loader layers')
    save_json('module_inventory.json', inventory)
    entries = [entry for entry in inventory if entry['row'][0] == 0x9d and entry['row'][1] & 2]
    if len(entries) != 1 or 0x9b not in modules or 0x9e not in modules:
        raise DecodeError('Missing or ambiguous saved ELF modules')
    entry = entries[0]
    payload = bounded(blob, entry['base_offset'] + entry['row'][2], entry['row'][3])
    expected_size = max(s['p_vaddr'] + s['p_memsz'] for s in elf.iter_segments() if s['p_type'] == 'PT_LOAD')
    header = saved_header(payload, modules[0x9b], expected_size)
    save_json('9d_header.json', header)
    decoder.configure(modules[0x9b], payload[header[2]:], header[3], wide_seed=True)
    log('Restoring IL2CPP memory (%d bytes)' % header[3])
    memory = decoder.decode(payload[header[2]:], header[3])
    (analysis / 'libil2cpp_restored_memory.bin').write_bytes(memory)
    log('Restoring ELF relocations (%d bytes)' % header[5])
    metadata = decoder.decode(payload[header[4]:], header[5])
    (analysis / 'libil2cpp_restored_metadata.bin').write_bytes(metadata)
    log('Rebuilding ELF')
    result, report = rebuild(original, memory, metadata, modules[0x9e])
    output.write_bytes(result)
    report['sha256'] = hashlib.sha256(result).hexdigest()
    save_json('elf_rebuild_report.json', report)
    log('Restored ELF SHA256: ' + report['sha256'])
    return output
