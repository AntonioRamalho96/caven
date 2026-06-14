from caven_lib.arg_parsing import CheckInput, CheckInputType
from caven_lib.info_parser import parse_target_info
import caven_lib.path_manager as path_manager

def check_module_exists(module_name):
    if not path_manager.DoesInfoExist(module_name):
        print(f"Module '{module_name}' not found in '{path_manager.GetModulePath(module_name)}'")
        exit(1)


def handle_check_cmd(input : CheckInput):
    if input.what_to_check == CheckInputType.PATH:
        print(path_manager.GetModulePath(input.module_name))

    if input.what_to_check == CheckInputType.VERSION:
        check_module_exists(input.module_name)
        print(parse_target_info(path_manager.GetModuleInfoPath(input.module_name)).version)
        
    if input.what_to_check == CheckInputType.DEPS:
        check_module_exists(input.module_name)
        print("\n".join(parse_target_info(path_manager.GetModuleInfoPath(input.module_name)).dependencies))