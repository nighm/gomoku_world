"""
GomokuWorld setup configuration
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gomoku_world",
    version="1.4.0",
    author="GomokuWorld Team",
    author_email="team@gomokuworld.org",
    description="A modern Gomoku (Five in a Row) game with AI and online multiplayer support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gomokuworld/gomoku_world",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
        "Framework :: Pygame",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pygame>=2.5.0",
        "numpy>=1.24.0",
        "opencv-python>=4.8.0",
    ],
    entry_points={
        "console_scripts": [
            "gomoku_world=gomoku_world.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "gomoku_world": [
            "resources/*.json",
            "resources/fonts/*",
            "resources/images/*",
            "resources/sounds/*",
        ],
    },
) 