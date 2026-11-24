import os
import unittest
import json
import re

class TestRenovateConfiguration(unittest.TestCase):
    def setUp(self):
        self.root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    def test_core_files_exist(self):
        required = [
            "README.md",
            "Makefile",
            "SECURITY.md",
            ".gitattributes",
            "renovate.json",
            "presets/enterprise-default.json",
            "scripts/validate-config.sh",
            "scripts/healthcheck.sh",
            "docs/architecture.svg"
        ]
        for f in required:
            p = os.path.join(self.root, f)
            self.assertTrue(os.path.exists(p), f"Required file '{f}' must exist")

    def test_renovate_json_fields(self):
        cfg_path = os.path.join(self.root, "renovate.json")
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        
        self.assertIn("$schema", cfg)
        self.assertIn("customManagers", cfg)
        self.assertIn("packageRules", cfg)
        self.assertIn("semanticCommitType", cfg)
        self.assertIn("vulnerabilityAlerts", cfg)
        self.assertTrue(cfg["vulnerabilityAlerts"]["automerge"])

    def test_regex_managers_compilation(self):
        cfg_path = os.path.join(self.root, "renovate.json")
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        
        for cm in cfg.get("customManagers", []):
            for pattern in cm.get("matchStrings", []):
                # JS (?<name>...) -> Python (?P<name>...)
                py_compat = re.sub(r"\(\?<([a-zA-Z0-9_]+)>", r"(?P<\1>", pattern)
                compiled = re.compile(py_compat)
                self.assertIsNotNone(compiled)

    def test_gitattributes_content(self):
        path = os.path.join(self.root, ".gitattributes")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("* text=auto eol=lf", content)
        self.assertIn("Makefile linguist-vendored=true", content)

if __name__ == "__main__":
    unittest.main()
