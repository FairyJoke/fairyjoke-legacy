import shutil
from argparse import ArgumentParser

import uvicorn

from fairyjoke import TMP_PATH, App


def run():
    uvicorn.run(
        "fairyjoke.app:App",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )


parser = ArgumentParser()
parser.add_argument("--init", action="store_true")
parser.add_argument(
    "action", choices=["init", "prepare", "run"], default="run", nargs="?"
)
args = parser.parse_args()

if args.init or args.action == "init":
    shutil.rmtree(TMP_PATH, ignore_errors=True)
    App.init()

if args.action == "prepare":
    App.prepare()

if args.action == "run":
    run()
