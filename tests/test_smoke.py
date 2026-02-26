import os


def test_repo_files_present():
    # Simple smoke check: essential docs exist (no heavy imports)
    assert os.path.exists("README.md")
    assert os.path.exists("requirements.txt")
