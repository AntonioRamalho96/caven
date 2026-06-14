from dataclasses import dataclass, field
import json
from pathlib import Path

class SourceInfoParseException(Exception):
    """ Exception parsing info.caven at source """
    pass

class TargetInfoParseException(Exception):
    """ Exception parsing info.caven at target """
    pass

@dataclass
class TargetInfo:
    module_name : str
    author : str = "Anonymous"
    email : str = ""
    version : str = "N/A"
    description : str = "No description available"
    dependencies : list[str] = field(default_factory=lambda: [])


@dataclass
class SourceInfo(TargetInfo):
    public_headers : list[str] = field(default_factory=lambda: []) # Relative paths to headers
    header_root_dir : str = None # Root of the header tree, in such a way that it works properly with -Iroot
    library_dir : str = None # Folder where the library lib{module_name}.so is
    build_cmd : str = 'echo "Nothing to be built"'



# =========================================== #
def parse_source_info(info_path : str):
    try:
        with open(info_path, "r") as f:
            json_obj = json.load(f)
            return SourceInfo(**json_obj)
    except Exception as e:
        raise SourceInfoParseException(f"Exception parsing source info.caven: {str(e)}")

def parse_target_info(info_path : str):
    try:
        with open(info_path, "r") as f:
            json_obj = json.load(f)
            return TargetInfo(**json_obj)
    except Exception as e:
        raise TargetInfoParseException(f"Exception parsing source info.caven: {str(e)}")
    
def convert_to_target_info(source_info : SourceInfo) -> TargetInfo:
    result = TargetInfo("")
    for attr in [attr for attr in dir(TargetInfo("")) if not attr.startswith("__")]:
        # Get attribute from source and copy it to the target
        attr_in_src = getattr(source_info, attr)
        setattr(result, attr, attr_in_src)
    # Remove sources for dependencies
    result.dependencies = [dep.split("<-")[0].strip() for dep in result.dependencies]
    return result

def save_as_json(info : TargetInfo|SourceInfo, out_path : str):
    with open(out_path, "w") as f:
        f.write(json.dumps(info.__dict__, indent= 4))

class DependencyInfo:
    def __init__(self, dep_str : str):
        deps_split = dep_str.split("<-")
        self.dep_name = deps_split[0].strip()
        self.dep_src = deps_split[1].strip() if len(deps_split) > 1 else None

    @classmethod
    def get_dependency_info(cls, deps : list[str]):
        return [cls(dep_str) for dep_str in deps]