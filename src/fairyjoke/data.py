import json

import toml
import yaml

from fairyjoke import DATA_PATH


class Data:
    def __init__(self, path=None):
        self.path = DATA_PATH
        if path:
            self.path = self.path / path

    def dict(self):
        for path in self.path.glob("*"):
            try:
                yield path.stem, self.load(path)
            except ValueError:
                continue

    def load(self, path):
        if path.suffix == ".json":
            return json.loads(path.read_text())
        elif path.suffix in [".yaml", ".yml"]:
            return yaml.safe_load(path.read_text())
        elif path.suffix == ".toml":
            return toml.loads(path.read_text())
        else:
            raise ValueError(f"Unknown file type: {path}")
