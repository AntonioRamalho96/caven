
import os
from pathlib import Path

class EnvNotSetException(Exception):
    """Exception raised when the Caven environment is not set."""
    pass


DEFAULT_ENV_PATH = Path("~/.caven").expanduser()

def GetEnvPath() -> Path:
    env_path = os.environ.get("CAVEN_ENV_DIR", None)
    if env_path is None:
        raise EnvNotSetException("Caven environment is not set, you can do so running:\n   caven env -p <path_to_env>")
    return Path(env_path)

def SetEnvPath(source_path : str):
    os.environ["CAVEN_ENV_DIR"] = str(Path(source_path) / ".caven_env")

def GetDepsPath() -> Path:
    return GetEnvPath() / "deps" 

def GetLibPath() -> Path:
    return GetEnvPath() / "lib" 

def GetActivatePath() -> Path:
    return GetEnvPath() / "activate" 

def GetModulePath(module_name : str) -> Path:
    return GetDepsPath() / module_name

def GetModuleIncPath(module_name : str) -> Path:
    return GetModulePath(module_name) / "inc"

def GetModuleLibDirPath(module_name : str) -> Path:
    return GetModulePath(module_name) / "lib"

def GetModuleLibPath(module_name : str) -> Path:
    return GetModuleLibDirPath(module_name) / f"lib{module_name}.so"

def GetModuleLibSymlinkPath(module_name : str) -> Path:
    return GetLibPath() / f"lib{module_name}.so"

def GetModuleInfoPath(module_name : str) -> Path:
    return GetModulePath(module_name) / "info.caven"

def GetSourceInfoPath(module_src_path : str):
    return Path(module_src_path) / "info.caven"

def DoesInfoExist(module_name : str):
    return os.path.isfile(GetModuleInfoPath(module_name))

def DoesSourceInfoExist(module_src_path : str):
    return os.path.isfile(GetSourceInfoPath(module_src_path))
