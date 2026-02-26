from pathlib import Path

def get_project_root():
    """
    Returns the root directory of the project.
    It searches upward until it finds a .git folder.
    """
    current = Path(__file__).resolve()

    for parent in [current] + list(current.parents):
        if (parent / ".git").exists():
            return parent

    raise Exception("Project root not found. Make sure this is inside a Git project.")