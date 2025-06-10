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
