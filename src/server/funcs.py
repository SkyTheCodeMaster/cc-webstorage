import os
from typing import TYPE_CHECKING

import aiofiles
from aiofiles import os as aos

from config import FILEPATH

if TYPE_CHECKING:
  from typing import Union


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

async def makeDir(folder: str) -> bool:
  path = os.path.join(FILEPATH,folder)
  try:
    await aos.makedirs(path,0o777,True)
    return True
  except:
    return False

async def list(folder:str) -> Union[list[str],False]:
  path = os.path.join(FILEPATH,folder)
  try:
    return await aos.listdir(path)
  except FileNotFoundError:
    return False