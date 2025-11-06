import zipfile, requests
import io
from ..constants import PROXIES

_global_session = requests.Session()
_global_session.proxies = PROXIES

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
        while True:
            response = self.session.head(self.url, allow_redirects=False)
            if response.status_code in (301, 302, 303, 307, 308):
                self.url = response.headers['Location']
            else:
                self.size = int(response.headers.get('Content-Length', 0))
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
        with open(url, 'rb') as f:
            self.file = f.read()
    
    def total_size(self):
        return len(self.file)
    
    def chunk(self, start, size):
        return self.file[start:start+size]

def create_range_reader(source):
    if source.startswith('http://') or source.startswith('https://'):
        return UrlRangeReader(source)
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
