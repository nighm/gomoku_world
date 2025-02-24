"""Version information."""

version = "2.1.2"
__version__ = version
__version_info__ = tuple(
    int(num) if num.isdigit() else num
    for num in __version__.replace("-", ".", 1).split(".")
)