import os
import re
import shutil
import subprocess

import yaml

_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "installations.yaml")

class SourceInstaller:
    def __init__(self, config_path = _CONFIG):
        self.__config = SourceInstaller._load_config(config_path)
        self.__directories_to_clean = []

    def install_source(self, source_input: str) -> str:
        """
        Match source_input against the sources defined in config_path (a YAML file).
        For the first matching source, runs any listed commands (with capture-group
        substitution) and returns the resolved source_path.

        Raises ValueError  - if no source pattern matches source_input.
        Raises RuntimeError - if any shell command exits with a non-zero status.
        """
        
        sources = self.__config.get("sources", [])

        for source in sources:
            pattern = source["pattern"]
            match = re.match(pattern, source_input)
            if match:
                return self._apply_source(source, match)

        raise ValueError(f"No source matched input: {source_input!r}")

    def cleanup(self):
        for dir in self.__directories_to_clean:
            print("Deleting " + dir)
            shutil.rmtree(dir, ignore_errors=True)
        self.__directories_to_clean = []

    @classmethod
    def _load_config(cls, config_path: str) -> dict:
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
        
    def _apply_source(self, source : dict, match : re.Match[str]) -> str:
        print(f"Source of type {source["name"]}")
        # Run commands to install the source
        for cmd_template in source.get("commands", []):
            cmd = SourceInstaller._substitute_groups(cmd_template, match)
            result = subprocess.run(cmd, shell=True)
            if result.returncode != 0:
                raise RuntimeError(
                    f"Command failed (exit {result.returncode}): {cmd}"
                )

        # Store directories that need to be deleted
        for to_remove_dir in source.get("to_remove", []):
            self.__directories_to_clean.append(SourceInstaller._substitute_groups(to_remove_dir, match))
            
        return SourceInstaller._substitute_groups(source["source_path"], match)

    @classmethod
    def _substitute_groups(cls, template: str, match: re.Match) -> str:
        """Replace $1, $2, ... with the corresponding regex capture groups."""
        def replacer(m):
            idx = int(m.group(1))
            groups = match.groups()
            if 1 <= idx <= len(groups):
                return groups[idx - 1] or ""
            return m.group(0)
        return re.sub(r"\$(\d+)", replacer, template)


        




# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import unittest
    from unittest.mock import MagicMock, patch

    

    class TestResolveSource(unittest.TestCase):

        # -- good weather -------------------------------------------------------

        def test_local_good_weather(self):
            result = SourceInstaller(_CONFIG).install_source("/home/user/myproject")
            self.assertEqual(result, "/home/user/myproject")

        def test_gh_http_good_weather(self):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = SourceInstaller(_CONFIG).install_source("gh:octocat/Hello-World")
            self.assertEqual(result, "/tmp/.caven/gh_src/Hello-World")

        def test_gh_http_at_good_weather(self):
            with patch("subprocess.run") as mock_run:
                mock_run.return_value = MagicMock(returncode=0)
                result = SourceInstaller(_CONFIG).install_source("gh:octocat/Hello-World@v2.1.0")
            self.assertEqual(result, "/tmp/.caven/gh_src/Hello-World")

        # -- bad weather --------------------------------------------------------

        def test_no_source_match_raises(self):
            with self.assertRaises(ValueError):
                SourceInstaller(_CONFIG).install_source(":::this_will_not_match:::")

    unittest.main()
