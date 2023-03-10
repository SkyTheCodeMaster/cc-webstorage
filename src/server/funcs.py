import os
import shutil
from typing import TYPE_CHECKING

import aiofiles
import aioshutil
from aiofiles import os as aos

from config import FILEPATH,CAPACITY

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

async def getFreeSpace(folder: str) -> Union[int,False]:
  size = await getSize(folder)
  if size == False: return False

  return CAPACITY - size

async def getCapacity(folder: str) -> int:
  return CAPACITY

async def isDir(folder: str) -> bool:
  path = os.path.join(FILEPATH,folder)
  return os.path.isdir(path)

async def attributes(file: str) -> Union[dict[str,Union[int,bool]],False]:
  path = os.path.join(FILEPATH,file)
  try:
    isdir = await isDir(file)
    readonly = await isReadOnly(file)
    stat = await aos.stat(path)
    attr = {
      "size": stat.st_size,
      "isDir": isdir,
      "isReadOnly": readonly,
      "created": stat.st_ctime,
      "modified": stat.st_mtime,
    }
    return attr
  except:
    return False

async def write(file: str, mode: str, contents: Union[bytes,str]) -> bool:
  path = os.path.join(FILEPATH,file)
  try:
    async with aiofiles.open(path,mode) as f:
      await f.write(contents)
    return True
  except:
    return False

async def read(file: str, mode: str) -> Union[Union[str,bytes],False]:
  path = os.path.join(FILEPATH,file)
  try:
    async with aiofiles.open(path,mode) as f:
      contents = await f.read()
    return contents
  except:
    return False

commands = {
  "attributes": attributes,
  "isDir": isDir,
  "getCapacity": getCapacity,
  "getFreeSpace": getFreeSpace,
  "isReadOnly": isReadOnly,
  "getSize": getSize,
  "copy": copy,
  "move": move,
  "exists": exists,
  "list": list,
  "makeDir": makeDir,
  "delete": delete,
  "write": write,
  "read": read,
}