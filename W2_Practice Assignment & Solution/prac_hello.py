import asyncio

# async def hello():
#     print("start")
#     await asyncio.sleep(1)
#     print("done")


# #asyncio.run(hello())
# async def main():
# # run three of them together — total time is ~1s, not ~3s
#     await asyncio.gather(hello(), hello(), hello())
    
# asyncio.run(main())

import asyncio

async def call(i):
    await asyncio.sleep(1)
    return i * 2

async def main():
    results = await asyncio.gather(*(call(i) for i in range(10)))
    print(results)
    
asyncio.run(main())
# 10 calls fire together. Total time: ~1 s, not 10 s.
# gather waits for all of them and returns results in order.