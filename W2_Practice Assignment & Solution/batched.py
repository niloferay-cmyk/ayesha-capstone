import asyncio
import time


async def batched(items, size, fn):
    out = []
    for i in range(0, len(items), size):
        chunk = items[i:i+size]
        out += await asyncio.gather(*(fn(x) for x in chunk))
        await asyncio.sleep(0.1)  # gentle pace
    return out


async def fake_call(x):
    await asyncio.sleep(0.2)  # pretend this is an API call
    return x * 2


async def main():
    items = list(range(20))
    start = time.time()
    result = await batched(items, size=5, fn=fake_call)
    print(result)
    print(f"Took {time.time() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())