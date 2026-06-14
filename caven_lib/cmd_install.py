from pathlib import Path
import subprocess
import shlex
import os
import shutil

from caven_lib.arg_parsing import InstallInput, InstallInputType
from caven_lib.info_parser import DependencyInfo, parse_source_info, convert_to_target_info, SourceInfoParseException, SourceInfo, save_as_json
import caven_lib.path_manager as path_manager
from caven_lib.install_source import SourceInstaller


class Installer:
    def __init__(self):
        self.src_installer = SourceInstaller()

    def handle_install_cmd(self, input : InstallInput):
        _ = path_manager.GetEnvPath() # Simply to crash if env is not set

        if input.val_type == InstallInputType.SOURCE:
            source = input.value
            current_path = Path(".").resolve()
            self._install_from_source_with_dependencies(source, current_path)
            self.src_installer.cleanup()
            exit(0)

        if input.val_type == InstallInputType.DEPS:
            module_src_path = Path(input.value).resolve()
            module_info = self._get_source_info(module_src_path)
            dependencies = module_info.dependencies
            self._install_dependencies(dependencies, module_src_path, module_info.module_name)
            self.src_installer.cleanup()
            exit(0)

        if input.val_type == InstallInputType.UNINSTALL:
            try:
                self._uninstall(input.value)
                print(f"Uninstalled '{input.value}'")
                exit(0)
            except FileNotFoundError:
                print(f"Module '{input.value}' is not installed")
                exit(1)

        raise RuntimeError("Unsupported")

    def _install_from_source(self, source_path : Path, source_info : SourceInfo):
        tmp_target_path = Path("/tmp/.caven") / source_info.module_name
        self._create_target_folder_from_src(source_info, source_path, tmp_target_path)
        self._install_from_targets(source_info.module_name, tmp_target_path)

    def _install_from_source_with_dependencies(self, source : str, current_path : Path):
        installed_source_path = self._install_source(source, current_path)
        source_info = self._get_source_info(installed_source_path)
        if(path_manager.DoesInfoExist(source_info.module_name)):
            print(f"Module '{source_info.module_name}' is already installed")
            return
        print(f"Installing '{source_info.module_name}'")
        self._install_dependencies(source_info.dependencies, installed_source_path, source_info.module_name)
        self._install_from_source(installed_source_path, source_info)
        print(f"Successfully installed '{source_info.module_name}'")

    def _create_target_folder_from_src(self, source_info : SourceInfo ,source_path : Path, dest_path : Path):
        self._execute_build_cmd_in_directory(source_info.build_cmd, source_path, source_info.module_name)
        self._create_target_from_built_src(source_info, source_path, dest_path)

    def _get_source_info(self, source_path : Path):
        source_info_path = path_manager.GetSourceInfoPath(source_path)
        try:
            source_info = parse_source_info(source_info_path)
        except SourceInfoParseException:
            print(f"Exception parsing info.caven at {source_info_path}")
            raise
        return source_info

    def _execute_build_cmd_in_directory(self, cmd : str, dir : Path, module_name : str):
        print(f"Will run the following command to build '{module_name}':")
        print("$> " + cmd)
        wd = os.getcwd()
        os.chdir(dir)
        try:
            subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
            print(f"Successfully built '{module_name}'")
        except subprocess.CalledProcessError as e:
            print(e.output.decode("utf-8"))
            print(f"Failed to build module '{module_name}' with command:")
            print("$> " + cmd)
            print("In directory:")
            print("  " + str(dir))
            os.chdir(wd)
            exit(1)

    def _create_target_from_built_src(self, source_info : SourceInfo, source_path : Path, target_path : Path):
        target_inc_path = target_path / "inc"
        target_lib_path = target_path / "lib"
        
        # Clean tmp directory if exists
        shutil.rmtree(target_path, ignore_errors=True)

        # Write target info
        print("target_path: " + str(target_path))
        os.makedirs(target_path, exist_ok=True)
        target_info = convert_to_target_info(source_info)
        save_as_json(target_info, target_path / "info.caven")
        
        # Write include headers
        os.makedirs(target_inc_path, exist_ok=True)
        self._copy_headers(source_info, source_path, target_inc_path)

        # Write library
        os.makedirs(target_lib_path, exist_ok=True)
        self._copy_library(source_info, source_path, target_lib_path)

    def _copy_library(self, source_info : SourceInfo, source_path : Path, target_lib_dir : Path):
        if source_info.library_dir is not None:
            shutil.copy(Path(source_path) / source_info.library_dir / f"lib{source_info.module_name}.so", target_lib_dir)
        else:
            self._create_empty_library(target_lib_dir / f"lib{source_info.module_name}.so")

    def _create_empty_library(self, library_path : Path):
        print("No .so lib dir specified, creating empty library") 
        empty_src_dir = Path("/tmp/.caven")
        empty_src_path = empty_src_dir / "empty.c"
        shutil.rmtree(empty_src_path, ignore_errors=True)
        os.makedirs(empty_src_dir, exist_ok= True)
        open(empty_src_path, "w").close()
        cmd = ["gcc", "-shared", str(empty_src_path),"-o", str(library_path)]
        subprocess.run(cmd)

    def _copy_headers(self, source_info : SourceInfo, source_path : Path, target_inc_dir : Path):
        for header_file in source_info.public_headers:
            shutil.copy(Path(source_path) / header_file, target_inc_dir)
        # TODO support root/roots, maybe check to ensure that all headers are in source

    def _uninstall(self, module_name : str, allow_not_exist = False):
        if(os.path.exists(path_manager.GetModuleLibSymlinkPath(module_name)) and
           os.path.exists(path_manager.GetModulePath(module_name))):
            # Remove if there was installed
            os.unlink(path_manager.GetModuleLibSymlinkPath(module_name))
            shutil.rmtree(path_manager.GetModulePath(module_name), ignore_errors=True)
        else:
            if(not allow_not_exist):
                raise FileNotFoundError(f"Tried to uninstall module '{module_name}' but it is not installed")

    def _install_from_targets(self, module_name : str, target_path : Path):
        # Copy files and create sym link for lib
        shutil.copytree(target_path, path_manager.GetModulePath(module_name))
        os.symlink(path_manager.GetModuleLibPath(module_name), path_manager.GetModuleLibSymlinkPath(module_name))

    def _install_dependencies(self, dependencies : list[str], current_path : Path, module_name : str):
        deps = DependencyInfo.get_dependency_info(dependencies)
        if(len(deps) > 0):
            print(f"Installing dependencies of module '{module_name}'")
        for dep in deps:
            if(path_manager.DoesInfoExist(dep.dep_name)):
                print(f"Module '{dep.dep_name}' is already installed, skipping...")
                continue

            if dep.dep_src is not None:
                self._install_from_source_with_dependencies(dep.dep_src, current_path)
            else:
                print(f"Cannot install '{dep.dep_name}', no source defined... install manually")
                exit(1)

    def _install_source(self, source_str : str, current_path : Path) -> str:
        source_path = self.src_installer.install_source(source_str)
        if not source_path.startswith("/"):
            source_path = str(Path(current_path) / source_path)
        return source_path


