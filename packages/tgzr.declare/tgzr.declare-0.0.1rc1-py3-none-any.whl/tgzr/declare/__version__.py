major = 0
minor = 0
patch = 1
rc = 1

version_str = f"{major}.{minor}.{patch}"
if rc:
    version_str += f"rc{rc}"

__version__ = version_str
