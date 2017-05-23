import asyncio


@asyncio.coroutine
def hello_world():
    while True:
        yield from asyncio.sleep(1)
        print('Hello World')

@asyncio.coroutine
def good_evening():
    while True:
        yield from asyncio.sleep(4)
        print('Good Evening')

print('step: asyncio.get_event_loop()')
loop = asyncio.get_event_loop()
try:
    print('step: loop.run_until_complete()')
    loop.run_until_complete(asyncio.wait([
        hello_world(),
        good_evening()
    ]))
    print('step: loop.run_until_complete()')
except KeyboardInterrupt:
    pass
finally:
    print('step: loop.close()')
    loop.close()