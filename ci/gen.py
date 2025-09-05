import json
import pathlib

ACTIONS_CHECKOUT = {"name": "Check out repository", "uses": "actions/checkout@v5"}
DEFAULT_BRANCH = "master"
THIS_FILE = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path().resolve())
)


def gen(content: dict, target: str):
    pathlib.Path(target).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(target).write_text(
        json.dumps(content, indent=2, sort_keys=True), newline="\n"
    )


def gen_dependabot():
    target = ".github/dependabot.yaml"
    content = {
        "version": 2,
        "updates": [
            {
                "package-ecosystem": e,
                "allow": [{"dependency-type": "all"}],
                "directory": "/",
                "schedule": {"interval": "daily"},
            }
            for e in ["github-actions", "uv"]
        ],
    }
    gen(content, target)


def gen_publish_workflow():
    target = ".github/workflows/publish-release-to-pypi.yaml"
    content = {
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "name": "Publish the release package to PyPI",
        "on": {"release": {"types": ["published"]}},
        "jobs": {
            "publish": {
                "name": "Publish the release package to PyPI",
                "runs-on": "ubuntu-latest",
                "environment": {
                    "name": "pypi-release",
                    "url": "https://pypi.org/p/rainwave-tools",
                },
                "permissions": {"id-token": "write"},
                "steps": [
                    ACTIONS_CHECKOUT,
                    {
                        "name": "Build and publish the package",
                        "run": "sh ci/build-and-publish.sh",
                    },
                ],
            }
        },
    }
    gen(content, target)


def gen_ruff_workflow():
    target = ".github/workflows/ruff.yaml"
    content = {
        "name": "Ruff",
        "on": {
            "pull_request": {"branches": [DEFAULT_BRANCH]},
            "push": {"branches": [DEFAULT_BRANCH]},
        },
        "permissions": {"contents": "read"},
        "env": {
            "description": f"This workflow ({target}) was generated from {THIS_FILE}"
        },
        "jobs": {
            "ruff-check": {
                "name": "Run ruff check",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff check", "run": "sh ci/ruff-check.sh"},
                ],
            },
            "ruff-format": {
                "name": "Run ruff format",
                "runs-on": "ubuntu-latest",
                "steps": [
                    ACTIONS_CHECKOUT,
                    {"name": "Run ruff format", "run": "sh ci/ruff-format.sh"},
                ],
            },
        },
    }
    gen(content, target)


def main():
    gen_dependabot()
    gen_publish_workflow()
    gen_ruff_workflow()


if __name__ == "__main__":
    main()
