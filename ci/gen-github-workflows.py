import gen

publish = {
    "name": "Publish the release package to PyPI",
    "on": {"release": {"types": ["published"]}},
    "env": {"_workflow_file_generator": "ci/gen-github-workflows.py"},
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
                {"name": "Check out the repository", "uses": "actions/checkout@v4"},
                {
                    "name": "Build and publish the package",
                    "run": "sh ci/build-and-publish.sh",
                },
            ],
        }
    },
}

gen.gen(publish, ".github/workflows/publish-release-to-pypi.yaml")

ruff = {
    "name": "Ruff",
    "on": {"pull_request": {"branches": ["master"]}, "push": {"branches": ["master"]}},
    "permissions": {"contents": "read"},
    "env": {
        "_workflow_file_generator": "ci/gen-github-workflows.py",
    },
    "jobs": {
        "ruff": {
            "name": "Run ruff linting and formatting checks",
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Check out repository", "uses": "actions/checkout@v4"},
                {
                    "name": "Run ruff check",
                    "uses": "astral-sh/ruff-action@v3",
                    "with": {"args": "check --output-format=github"},
                },
                {
                    "name": "Run ruff format",
                    "uses": "astral-sh/ruff-action@v3",
                    "with": {"args": "format --check"},
                },
            ],
        }
    },
}

gen.gen(ruff, ".github/workflows/ruff.yaml")
