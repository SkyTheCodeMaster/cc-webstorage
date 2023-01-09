import os

import aiofiles
from aiofiles import os as aos

from config import FILEPATH


async def delete(file: str) -> bool:
  path = os.path.join(FILEPATH,file)
  try:
    await aos.remove(path)
    return True
  except OSError:
    try:
      await aos.rmdir(path)
      return True
    except FileNotFoundError:
      return False
  except FileNotFoundError:
    return False

