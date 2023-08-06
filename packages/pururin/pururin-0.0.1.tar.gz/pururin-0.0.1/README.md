# Gawain
Booru armor wrapper
[![Testing](https://github.com/sinkaroid/gawain/actions/workflows/test.yml/badge.svg)](https://github.com/sinkaroid/gawain/actions/workflows/test.yml)

```py
import asyncio
from gawain import Booru


async def get():
    data = Booru()
    print(data.gelbooru(tags="cat_girl", limit=100, pid=1, block="loli", shuffle=True))


async def main():
    await asyncio.gather(get())

asyncio.run(main())

```