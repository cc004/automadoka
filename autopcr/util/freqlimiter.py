import asyncio

def FreqLimiter(limit: int, interval: float):
    sema = None
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nonlocal sema
            if sema is None: sema = asyncio.Semaphore(limit)
            await sema.acquire()
            asyncio.get_running_loop().call_later(interval, sema.release)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def RunningLimiter(limit: int):
    sema = None
    def decorator(func):
        async def wrapper(*args, **kwargs):
            nonlocal sema
            if sema is None: sema = asyncio.Semaphore(limit)
            await sema.acquire()
            try:
                return await func(*args, **kwargs)
            finally:
                sema.release()
        return wrapper
    return decorator