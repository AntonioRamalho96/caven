import os

from caven_lib.arg_parsing import EnvInput, EnvInputType
import caven_lib.path_manager as path_manager

def handle_env_cmd(input : EnvInput):
    if input.in_type == EnvInputType.DISPLAY:
        try:
            print(path_manager.GetEnvPath())
        except path_manager.EnvNotSetException:
            print("Caven environment not set")
            exit(1)

    if input.in_type == EnvInputType.PATH:
        create_env(input.path)



ACTIVATE_SCRIPT_FROM_LINE_2 = """

# Create deactivate script
echo "unset CAVEN_ENV_DIR"                     >  $CAVEN_PATH/deactivate
echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH" >> $CAVEN_PATH/deactivate
echo "export LIBRARY_PATH=$LIBRARY_PATH"       >> $CAVEN_PATH/deactivate
echo "export PS1=\\\"$PS1\\\""                     >> $CAVEN_PATH/deactivate

# Create activate environment
export CAVEN_ENV_DIR=$CAVEN_PATH
export LD_LIBRARY_PATH=$CAVEN_ENV_DIR/lib
export LIBRARY_PATH=$LIBRARY_PATH:$CAVEN_ENV_DIR/lib
export PS1="(caven) $PS1"
"""

def create_env(env_path : str):
    path_manager.SetEnvPath(env_path) # This is lost after the python returns

    abs_path = os.path.realpath(path_manager.GetEnvPath())
    
    os.makedirs(path_manager.GetDepsPath(), exist_ok=True)
    os.makedirs(path_manager.GetLibPath(), exist_ok=True)
    with open(path_manager.GetActivatePath(), "w") as f:
        f.write(f"CAVEN_PATH={abs_path}\n")
        f.write(ACTIVATE_SCRIPT_FROM_LINE_2)
    print("To activate the created caven environemtn run:")
    print(f"   source {path_manager.GetActivatePath()}")
