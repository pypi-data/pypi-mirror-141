import dataclasses
import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict
import pandas as pd


@dataclass
class Workspace:

    name: str = None
    file: str = None
    charts: Dict = field(default_factory=lambda: {'Chart1': {}})
    selected: str = 'Chart1'
    general: Dict = field(default_factory=dict)
    plot: List = field(default_factory=lambda: ['hist'] * 9)
    df: pd.DataFrame = field(default_factory=pd.DataFrame)
    path: str = None

    def save(self):
        with open(self.path, "w") as file:
            data = dataclasses.asdict(self)
            data.pop("df")
            data.pop("path")
            file.write(json.dumps(data))

    def __setattr__(self, key, value):
        super().__setattr__(key, value)

        if key == "file" and value is not None:
            self.df = pd.read_csv(value, parse_dates=True)
            self.path = workspace_from_filename(value)


def workspace_from_filename(path):
    p = Path(os.path.abspath(path))
    r = p.parent / ("." + p.stem + ".vws")
    return str(r)


_store = {"ws": Workspace()}


def __getattr__(name):
    if name == "cws":
        return _store.get("ws")


def load_workspace(path):

    with open(path) as f:
        cws = Workspace(**json.loads(f.read()))
        cws.file = cws.file
        _store["ws"] = cws

