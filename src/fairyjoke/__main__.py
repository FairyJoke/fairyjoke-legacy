from argparse import ArgumentParser

import uvicorn

import fairyjoke


def run():
    uvicorn.run(
        "fairyjoke:create_app",
        factory=True,
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["src"],
    )


parser = ArgumentParser()
parser.add_argument("--init", action="store_true")
parser.add_argument("action", choices=["init", "run"], default="run", nargs="?")
args = parser.parse_args()

if args.init or args.action == "init":
    fairyjoke.init()

if args.action == "run":
    run()
