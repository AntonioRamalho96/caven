# Caven

A virtual environment and module management tool for C/C++.

## Why Caven

Unlike Python that has pip, C/C++ lacks a user-friendly module manager for managing dependencies. Debian packages don't allow installation from source and require sudo privileges to be installed. Besides, debian packages are tailored for system wide installs. 

Caven provides a solution by offering utilities to manage install modules and manage environments.
Caven addresses these pain points by providing:
- **Isolated environments**: Create project-specific virtual environments to avoid conflicts
- **Automatic dependency resolution**: Recursively install all required dependencies
- **Environment-level installation**: No sudo privileges needed; install to user directories
- **Source-based installation**: You can build and install modules from source, so that you can use local directories or remote repositories.

## Commands

### env
Set or display a virtual environment.

**Options:**
- `-p, --path` - Path to the virtual environment to create (default: `~/.caven`)
- `-d, --display` - Display path to the currently active virtual environment

**Example:**
```bash
caven env --path .
caven env --display
```

### install
Install, uninstall, or manage module dependencies. When installing a dependency, it automatically installs it's dependencies.

**Options:**
- `-d, --dependencies` - Path to module source code, will install its dependencies
- `-s, --source` - Path to folder containing the source of the module to install
- `-u, --uninstall` - Module name of module to uninstall

**Example:**
```bash
caven install --source /path/to/module                       # Install from your file system, supports relative paths
caven install --source gh:AntonioRamalho96/caven_my_module   # Install from GH, you can use @ to specify a branch or commit
caven install --dependencies ./module                        # Installs all dependencies for the module in the specified folder
caven install --uninstall module_name                        # Uninstalls a module given its name
```

### check
Check module information.

**Options:**
- `-p, --path` - Path to folder containing installed module
- `-v, --version` - Get version of an installed module
- `-d, --dependencies` - Get dependencies of installed module

**Arguments:**
- `module_name` - Name of the module to check

**Example:**
```bash
caven check -v module_name
caven check -d module_name
caven check -p module_name
```

### use
Commands to use a module during compilation.

**Action Options:**
- `-i, --include-dir` - Path to folder containing installed module(s) include directories
- `-if, --include-flags` - Get compilation flags to include directories
- `-l, --lib-dir` - Path to folder containing installed module(s) shared library(s)
- `-lf, --lib-flags` - Return flags to link the desired module(s) shared library(s)

**Target Options:**
- `-m, --module` - Name of the module
- `-s, --source` - Directory with the source of a module, will use all module dependencies

**Example:**
```bash
caven use -if -m module_name
caven use -lf -s /path/to/source
caven use -i -m module_name
```
