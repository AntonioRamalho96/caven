from caven_lib.arg_parsing import UseInput, UseActionType, UseTargetType
import caven_lib.path_manager as path_manager
import caven_lib.info_parser as info_parser


def handle_use_cmd(input : UseInput):
    if input.use_target_type == UseTargetType.MODULE:
        print(get_output(input.use_action_type, input.use_target))
        
    if input.use_target_type == UseTargetType.MODULE_DEPS:
        if(not path_manager.DoesSourceInfoExist(input.use_target)):
            print("Could not find info.caven")
            exit(1)
        deps = info_parser.parse_source_info(path_manager.GetSourceInfoPath(input.use_target)).dependencies
        module_names = [dep_info.dep_name for dep_info in info_parser.DependencyInfo.get_dependency_info(deps)]
        print(" ".join([get_output(input.use_action_type ,module) for module in module_names]))

def get_output(in_type : UseActionType, module_name : str) -> str:
    if in_type == UseActionType.INC_FLAGS:
        return f"-I {path_manager.GetModuleIncPath(module_name)}"
    if in_type == UseActionType.LIB_FLAGS:
        return f"-l{module_name}"
    raise NotImplementedError("This functionality is not available yet")
