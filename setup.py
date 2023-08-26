import os
import glob
import setuptools

__version__ = "0.1.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


def get_install_requires() -> list:
    """Returns requirements.txt parsed to a list"""
    fname = os.path.join(os.path.dirname(__file__), "requirements.txt")
    targets = []
    if os.path.exists(fname):
        with open(fname, 'r') as f:
            targets = f.read().splitlines()
    return targets


setuptools.setup(
    name="django_kakebo",
    version=__version__,
    author="shadMod",
    author_email="support@shadmod.it",
    description="A simple site made with django and exploiting the kakebo method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadMod/django-kakebo/",
    download_url=f"https://github.com/shadMod/django-kakebo/archive/refs/tags/{__version__}.tar.gz",
    project_urls={
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
        "django_kakebo", "django_kakebo.src.django_kakebo", "django_kakebo.src.django_kakebo.migrations",
        "django_kakebo.src.django_kakebo.templatetags", "django_kakebo.src.django_kakebo.views",
        "django_kakebo.src.user"
    ],
    data_files=[
        (
            "static",
            [fn for fn in glob.iglob("django_kakebo/src/django_kakebo/static/**/*", recursive=True) if "." in fn],
        ),
        (
            "themes",
            [fn for fn in glob.iglob("django_kakebo/src/themes/**/*", recursive=True) if "." in fn],
        ),
        (
            "static_user",
            [fn for fn in glob.iglob("django_kakebo/src/user/static/**/*", recursive=True) if "." in fn],
        ),
    ],
    install_requires=get_install_requires(),
    python_requires=">=3.8",
)
