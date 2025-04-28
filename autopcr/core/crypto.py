import base64
import hashlib
import hmac
from datetime import datetime, timezone
from typing import Optional, Union, Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa, utils
from cryptography.hazmat.primitives.serialization import load_der_private_key
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import msgpack


class StrCnv1:
    @staticmethod
    def cnv(src: str) -> str:
        # 取出所有奇数下标的字符（与 C# 中 (2*i)|1 等价）
        return ''.join(src[i] for i in range(1, len(src), 2))


class Builtin:
    _elements = [
        "4dn9Sycy!ev)8f%_,Yay~pAj)~k4q!hNz,FHuWHFQe%+P*eW24Ac)yTAGeF$pJ)!7BU!9#ke%|3Ai%*jMa(Vi~B2j*L(uyvE/9cE$E_,WwV4irL$5RXgaC4ufu/4FB5p",
        "j%.i.LL|rL,+d6JA",
        "EZTv,6~NZQv(X9DU",
    ]

    @staticmethod
    def get_key(index: int) -> str:
        return StrCnv1.cnv(Builtin._elements[index])


class AppCryptoConfig:
    @staticmethod
    def hash_key() -> str:
        return Builtin.get_key(0)

    @staticmethod
    def hash_salt() -> str:
        return Builtin.get_key(1)

    @staticmethod
    def crypto_key() -> str:
        key = Builtin.get_key(2)
        return Hash.hash_string(key, 16)

    @staticmethod
    def get_hash_algorithm(secret_key: bytes):
        # 返回一个 HMAC-SHA256 对象
        return hmac.new(secret_key, digestmod=hashlib.sha256)


class Hash:
    @staticmethod
    def get_salt() -> str:
        salt = AppCryptoConfig.hash_salt()
        # 原 C# 逻辑实际上是返回整个字符串，这里保持一致
        return salt

    @staticmethod
    def get_hash_key() -> bytes:
        key = AppCryptoConfig.hash_key()
        return key.encode('utf-8')

    @staticmethod
    def hash_bytes(text: str, max_length: int) -> bytes:
        v8 = Hash.get_salt() + text
        hmac_obj = AppCryptoConfig.get_hash_algorithm(Hash.get_hash_key())
        h = hmac_obj.copy()
        h.update(v8.encode('utf-8'))
        v15 = h.digest()
        # 如果 max_length 为 0 或者原始长度不足，则返回完整结果
        if max_length == 0 or len(v15) < max_length:
            return v15
        offset = (len(v15) - max_length) // 2
        return v15[offset: offset + max_length]

    @staticmethod
    def hash_string(text: str, max_length: int) -> str:
        hb = Hash.hash_bytes(text, max_length)
        b64 = base64.b64encode(hb).decode('utf-8')
        if len(b64) > max_length:
            start = (len(b64) - max_length) // 2
            return b64[start:start + max_length]
        return b64

class BasicCrypto:
    @staticmethod
    def decrypt(crypto_key: Union[bytes, str], data: bytes) -> bytes:
        """
        前 crypto_key.Length 字节是 IV，其余是密文。
        使用 AES-CBC + PKCS7 解密。
        """
        if isinstance(crypto_key, str):
            crypto_key = crypto_key.encode('utf-8')

        iv = data[:len(crypto_key)]
        ciphertext = data[len(crypto_key):]

        # PyCryptodome 仅支持 128-bit block size
        cipher = AES.new(crypto_key, AES.MODE_CBC, iv=iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size)

    @staticmethod
    def encrypt(crypto_key: Union[bytes, str], data: bytes, iv: bytes) -> bytes:
        """
        对 data 做 AES-CBC + PKCS7 加密，返回 IV || 密文。
        """
        if isinstance(crypto_key, str):
            crypto_key = crypto_key.encode('utf-8')

        cipher = AES.new(crypto_key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return iv + ciphertext


class PackHelper:
    @staticmethod
    def unpack(crypted: bytes) -> Any:
        """
        解包：先调用 ApiCrypto.decrypt，得到 msgpack 二进制，
        再转换成 Python 原生结构（list/dict/基本类型）。
        """
        decrypted = ApiCrypto.decrypt(crypted)
        return msgpack.unpackb(decrypted, raw=False)

    @staticmethod
    def get_iv() -> bytes:
        """
        返回固定的 IV，C# 中是一串 HEX 数值。
        """
        hex_str = "88 46 51 55 30 61 67 82 55 2c ab 5e 1d 7c 85 0f"
        parts = hex_str.split()
        return bytes(int(x, 16) for x in parts)

    @staticmethod
    def pack(token: Any, iv: bytes) -> bytes:
        """
        打包：将 Python 结构转换成 msgpack 二进制，
        再调用 ApiCrypto.encrypt，返回加密后的字节串。
        """
        packed: bytes = msgpack.packb(token)
        return ApiCrypto.encrypt(packed, iv)


class ApiCrypto:
    _MSG_PACK_KEY = "UVFBdDtWKhpESJj3"

    @staticmethod
    def decrypt(encrypted: bytes) -> bytes:
        hk = Hash.hash_string(ApiCrypto._MSG_PACK_KEY, 16)
        return BasicCrypto.decrypt(hk, encrypted)

    @staticmethod
    def encrypt(raw: bytes, iv: bytes) -> bytes:
        hk = Hash.hash_string(ApiCrypto._MSG_PACK_KEY, 16)
        return BasicCrypto.encrypt(hk, raw, iv)

    @staticmethod
    def to_timestamp(time: datetime) -> int:
        # 转为 UTC 秒级时间戳
        return int(time.astimezone(timezone.utc).timestamp())

    @staticmethod
    def sign(encrypted: bytes, private_key_bytes: bytes) -> str:
        # 先对 encrypted 做 SHA1，然后 Base64
        sha1 = hashlib.sha1()
        sha1.update(encrypted)
        data = base64.b64encode(sha1.digest())

        # 加载 PKCS#8 DER 格式的私钥
        private_key: rsa.RSAPrivateKey = load_der_private_key(private_key_bytes, password=None)

        # 对 Base64(data) 再做一次 SHA1
        sha1_2 = hashlib.sha1()
        sha1_2.update(data)
        digest = sha1_2.digest()

        # 使用 RSA-SHA1 签名
        signature = private_key.sign(
            digest,
            padding.PKCS1v15(),
            utils.Prehashed(hashes.SHA1())
        )
        return base64.b64encode(signature).decode('utf-8')
