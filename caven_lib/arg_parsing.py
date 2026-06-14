import argparse
from dataclasses import dataclass
from enum import Enum

from caven_lib.path_manager import DEFAULT_ENV_PATH


def parse_arguments():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest="subcommand", description="Action to perform", required=True)

    # Parse env option
    env_parser = subparsers.add_parser('env', help="Set a virtual environment")
    env_options = env_parser.add_mutually_exclusive_group(required=False)
    env_options.add_argument('-p', '--path', help=f"Path to the virtual environment to create, the default is {DEFAULT_ENV_PATH}", default=DEFAULT_ENV_PATH)
    env_options.add_argument('-d', '--display', help=f"Display path to the currently active virtual environment", action="store_true")

    # Parse install option
    install_parser = subparsers.add_parser('install', help="Install one or more modules")
    install_options = install_parser.add_mutually_exclusive_group(required=True)
    install_options.add_argument("-d", "--dependencies", help= "Path to module source code, will install it's dependencies")
    install_options.add_argument("-s", "--source", help= "Path to folder containing the source of the module to install")
    install_options.add_argument("-u", "--uninstall", help= "Module name of module to uninstall")

    check_parser = subparsers.add_parser('check', help="Commands to check a module information")
    check_options = check_parser.add_mutually_exclusive_group(required=True)
    check_options.add_argument("-p", "--path", help= "Path to folder containing installed module", action="store_true")
    check_options.add_argument("-v", "--version", help= "Get version of an installed module", action="store_true")
    check_options.add_argument("-d", "--dependencies", help= "Get dependencies of installed module", action="store_true")

    check_parser.add_argument("module_name", help="Name of the module to check")


    use_parser = subparsers.add_parser('use', help="Commands to use a module during compilation")
    use_options = use_parser.add_mutually_exclusive_group(required=True)
    use_options.add_argument("-i", "--include-dir", help= "Path to folder containing installed module(s) include directories", action="store_true")
    use_options.add_argument("-if", "--include-flags", help= "Get compilation flags to include directories regarding this module(s)", action="store_true")
    use_options.add_argument("-l", "--lib-dir", help= "Path to folder containing installed module(s) shared library(s)", action="store_true")
    use_options.add_argument("-lf", "--lib-flags", help= "Return flags to link the desired module(s) shared library(s)", action="store_true")

    use_target = use_parser.add_mutually_exclusive_group(required=True)
    use_target.add_argument("-m", "--module", help="Name of the module")
    use_target.add_argument("-s", "--source", help="Directory with the source of a module, will use all module dependencies")

    return parser.parse_args()

# ---------------------------------------------#
# Option: ENV
# ---------------------------------------------#
class EnvInputType(Enum):
    PATH = 1
    DISPLAY = 2

@dataclass
class EnvInput:
    in_type : EnvInputType
    path : str
    

def get_env_inputs(args):
    return EnvInput(
        in_type = EnvInputType.DISPLAY if args.display else EnvInputType.PATH,
        path = args.path if args.path else DEFAULT_ENV_PATH
    ) 


# ---------------------------------------------#
# Option: INSTALL
# ---------------------------------------------#
class InstallInputType(Enum):
    DEPS = 1
    SOURCE = 3
    UNINSTALL = 4

@dataclass
class InstallInput:
    val_type : InstallInputType
    value: str

def get_install_inputs(args):
    if args.dependencies:
        inst_type = InstallInputType.DEPS
        value = args.dependencies
    if args.source:
        inst_type = InstallInputType.SOURCE
        value = args.source
    if args.uninstall:
        inst_type = InstallInputType.UNINSTALL
        value = args.uninstall

    return InstallInput(
        val_type = inst_type,
        value = value
    )


# ---------------------------------------------#
# Option: CHECK
# ---------------------------------------------#
class CheckInputType(Enum):
    PATH = 1
    VERSION = 2
    DEPS = 3

@dataclass
class CheckInput:
    what_to_check : CheckInputType
    module_name: str

def get_check_inputs(args):
    if args.path:
        what_to_check = CheckInputType.PATH
    if args.version:
        what_to_check = CheckInputType.VERSION
    if args.dependencies:
        what_to_check = CheckInputType.DEPENDENCIES
    return CheckInput(
        what_to_check=what_to_check,
        module_name=args.module_name
    )


# ---------------------------------------------#
# Option: USE
# ---------------------------------------------#
class UseActionType(Enum):
    INC_DIR = 1
    INC_FLAGS = 2
    LIB_DIR = 3
    LIB_FLAGS = 4

class UseTargetType(Enum):
    MODULE=1
    MODULE_DEPS=2

@dataclass
class UseInput:
    use_action_type : UseActionType
    use_target_type : UseTargetType
    use_target : str

def get_use_inputs(args):
    # Parse action type
    if args.include_dir:
        use_action_type = UseActionType.INC_DIR
    elif args.include_flags:
        use_action_type = UseActionType.INC_FLAGS
    elif args.lib_dir:
        use_action_type = UseActionType.LIB_DIR
    elif args.lib_flags:
        use_action_type = UseActionType.LIB_FLAGS
    
    # Parse target type and target
    if args.module:
        use_target_type = UseTargetType.MODULE
        use_target = args.module
    elif args.source:
        use_target_type = UseTargetType.MODULE_DEPS
        use_target = args.source
    
    return UseInput(
        use_action_type=use_action_type,
        use_target_type=use_target_type,
        use_target=use_target
    )
    