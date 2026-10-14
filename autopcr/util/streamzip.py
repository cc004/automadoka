import hashlib, json, os, shutil, zipfile, requests
import io
from pathlib import Path
from ..constants import PROXIES, CACHE_DIR

_global_session = requests.Session()
_global_session.proxies = PROXIES

DOWNLOAD_CACHE_KEEP = 2

class RangeReader:
    def total_size(self):
        raise NotImplementedError()
    
    def chunk(self, start, size):
        raise NotImplementedError()
    
    def close(self): ...

class UrlRangeReader(RangeReader):
    def __init__(self, url):
        self.session = _global_session
        self.url = url
        self.etag = ''
        while True:
            response = self.session.head(self.url, allow_redirects=False)
            if response.status_code in (301, 302, 303, 307, 308):
                self.url = response.headers['Location']
            else:
                self.size = int(response.headers.get('Content-Length', 0))
                self.etag = (response.headers.get('ETag')
                             or response.headers.get('Last-Modified') or '')
                return
    
    def total_size(self):
        return self.size

    def chunk(self, start, size):
        end = start + size - 1
        headers = {'Range': f'bytes={start}-{end}'}
        response = self.session.get(self.url, headers=headers)
        response.raise_for_status()
        return response.content

    def close(self):
        self.session.close()

class FileRangeReader(RangeReader):
    def __init__(self, url):
        self.file = open(url, 'rb')
        self.file.seek(0, io.SEEK_END)
        self.size = self.file.tell()
    
    def total_size(self):
        return self.size
    
    def chunk(self, start, size):
        self.file.seek(start)
        return self.file.read(size)

    def close(self):
        self.file.close()

class DiskCacheReader(RangeReader):
    """Spool every fetched range to disk so an interrupted run resumes locally.

    The spool is keyed by the resolved URL, its size and its validator, so a new
    build can never be served out of an older build's spool. A chunk is written
    to a temporary name and then moved into place, so a kill during the write
    cannot leave a half chunk that a later run would trust.
    """
    def __init__(self, reader, key, root=None):
        self.reader = reader
        self.directory = Path(root if root is not None else Path(CACHE_DIR) / 'download') / key
        self.directory.mkdir(parents=True, exist_ok=True)

    def total_size(self):
        return self.reader.total_size()

    def chunk(self, start, size):
        path = self.directory / ('%012d-%08d.bin' % (start, size))
        try:
            cached = path.read_bytes()
        except OSError:
            cached = None
        if cached is not None and len(cached) == size:
            return cached
        data = self.reader.chunk(start, size)
        temporary = path.with_name(path.name + '.part')
        temporary.write_bytes(data)
        os.replace(str(temporary), str(path))
        return data

    def close(self):
        self.reader.close()

def cache_key(reader):
    """Identify a remote build by resolved URL, size and validator."""
    identity = json.dumps([reader.url, reader.total_size(), getattr(reader, 'etag', '')],
                          sort_keys=True)
    return hashlib.sha256(identity.encode()).hexdigest()[:16]

def prune_download_cache(root=None, keep=DOWNLOAD_CACHE_KEEP):
    """Keep only the newest spools; a finished update never needs the older ones."""
    root = Path(root if root is not None else Path(CACHE_DIR) / 'download')
    try:
        entries = [path for path in root.iterdir() if path.is_dir()]
    except OSError:
        return []
    entries.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    removed = []
    for path in entries[keep:]:
        try:
            shutil.rmtree(path)
        except OSError:
            continue
        removed.append(path.name)
    return removed

def create_range_reader(source):
    if source.startswith('http://') or source.startswith('https://'):
        reader = UrlRangeReader(source)
        return DiskCacheReader(reader, cache_key(reader))
    else:
        return FileRangeReader(source)

class IOWrapper():
    CHUNK_SIZE = 1024 * 1024  # 1MB
    def __init__(self, range_reader: RangeReader):
        self.reader = range_reader
        self.total_size = self.reader.total_size()
    
        self.chunk_count = (self.total_size + self.CHUNK_SIZE - 1) // self.CHUNK_SIZE

        self.buffer = [None] * self.chunk_count
        self.pos = 0
    def tell(self) -> int:
        return self.pos
    
    def read(self, size: int = -1) -> bytes:
        if size < 0:
            size = self.total_size - self.pos
        
        if self.pos >= self.total_size:
            return b''
        
        if self.pos + size > self.total_size:
            size = self.total_size - self.pos
        
        start_chunk = self.pos // self.CHUNK_SIZE
        end_chunk = (self.pos + size - 1) // self.CHUNK_SIZE
        
        result = bytearray()
        
        for chunk_index in range(start_chunk, end_chunk + 1):
            if self.buffer[chunk_index] is None:
                chunk_start = chunk_index * self.CHUNK_SIZE
                chunk_size = min(self.CHUNK_SIZE, self.total_size - chunk_start)
                self.buffer[chunk_index] = self.reader.chunk(chunk_start, chunk_size)
            
            chunk_data = self.buffer[chunk_index]
            chunk_start_pos = chunk_index * self.CHUNK_SIZE
            read_start = max(self.pos, chunk_start_pos)
            read_end = min(self.pos + size, chunk_start_pos + len(chunk_data))
            
            if read_start < read_end:
                result.extend(chunk_data[read_start - chunk_start_pos:read_end - chunk_start_pos])
        
        self.pos += size
        return bytes(result)

    def seekable(self) -> bool:
        return True
    
    def seek(self, offset: int, whence: int = io.SEEK_SET) -> int:
        if whence == io.SEEK_SET:
            self.pos = offset
        elif whence == io.SEEK_CUR:
            self.pos += offset
        elif whence == io.SEEK_END:
            self.pos = self.total_size + offset
        
        if self.pos < 0:
            self.pos = 0
        
        if self.pos > self.total_size:
            self.pos = self.total_size
        
        return self.pos

    def close(self):
        self.reader.close()
        self.buffer = []

class StreamZip(zipfile.ZipFile):
    def __init__(self, url):
        self.wrapper = IOWrapper(create_range_reader(url))
        super().__init__(self.wrapper)
    
    def close(self):
        super().close()
        self.wrapper.close()
