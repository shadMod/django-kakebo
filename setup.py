import glob
from pathlib import Path

import setuptools

__version__ = "0.2.3"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_install_requires() -> list[str]:
    """Returns requirements.txt parsed to a list.

    Returns:
        list[str]: Requirements parsed to a list.
    """
    path_file = Path(__file__).parent / "requirements.txt"
    if path_file.exists():
        with open(path_file) as f:
            return f.read().splitlines()
    return []


setuptools.setup(
    name="django_kakebo",
    version=__version__,
    author="shadmod",
    author_email="support@shadmod.it",
    description="A simple django app that exploiting the kakebo method ('primitive_user' app is included).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadMod/django-kakebo/",
    download_url=f"https://github.com/shadMod/django-kakebo/archive/refs/tags/{__version__}.tar.gz",
    project_urls={
        'Documentation': 'https://docs.shadmod.it/django_kakebo/index',
        'GitHub': 'https://github.com/shadMod/django-kakebo/',
        "Bug Tracker": "https://github.com/shadMod/django-kakebo/issues/",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    include_package_data=True,
    packages=[
        "django_kakebo", "django_kakebo.migrations", "django_kakebo.templatetags",
        "django_kakebo.views", "django_kakebo_user"
    ],
    data_files=[
        (
            "django_kakebo/static",
            [filename for filename in glob.iglob("django_kakebo/static/**/*", recursive=True) if "." in filename],
        ),
        (
            "django_kakebo/templates",
            [filename for filename in glob.iglob("django_kakebo_templates/**/*", recursive=True) if "." in filename],
        ),
        (
            "django_kakebo/user_static",
            [filename for filename in glob.iglob("django_kakebo_user/static/**/*", recursive=True) if "." in filename],
        ),
    ],
    install_requires=get_install_requires(),
    python_requires=">=3.8",
)
