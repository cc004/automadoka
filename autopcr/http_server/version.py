"""Frontend API compatibility, shared by the server and web downloader.

Keep this module dependency-free so downloading the frontend does not require
importing the server, database or game protocol models.
"""

import re

APP_VERSION_MAJOR = 1
APP_VERSION_MINOR = 7


def parse_release_version(tag):
    """Return a stable release's numeric version, or None for other tags."""
    match = re.fullmatch(r"v?(\d+)\.(\d+)\.(\d+)", tag.strip())
    return tuple(map(int, match.groups())) if match else None


def is_compatible_release(tag):
    version = parse_release_version(tag)
    return version is not None and version[:2] == (
        APP_VERSION_MAJOR, APP_VERSION_MINOR
    )
