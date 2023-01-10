import os
import shutil
from typing import TYPE_CHECKING

import aiofiles
import aioshutil
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

async def list(folder: str) -> Union[list[str],False]:
  path = os.path.join(FILEPATH,folder)
  try:
    return await aos.listdir(path)
  except FileNotFoundError:
    return False

async def exists(file: str) -> bool:
  path = os.path.join(FILEPATH,file)
  return os.access(path,os.F_OK)

async def move(src: str, dst: str) -> bool:
  sPath = os.path.join(FILEPATH,src)
  dPath = os.path.join(FILEPATH,dst)
  try:
    await aioshutil.move(sPath,dPath)
    return True
  except:
    return False

async def copy(src: str, dst: str) -> bool:
  sPath = os.path.join(FILEPATH,src)
  dPath = os.path.join(FILEPATH,dst)
  try:
    await aioshutil.copy2(sPath,dPath)
    return True
  except:
    return False

async def getSize(folder: str) -> Union[int,False]:
  path = os.path.join(FILEPATH,folder)
  try:
    size = shutil.disk_usage(path)
    return size.used
  except:
    return False

async def isReadOnly(folder: str) -> bool:
  path = os.path.join(FILEPATH,folder)
  try:
    return not os.access(path, os.W_OK)
  except:
    return True

