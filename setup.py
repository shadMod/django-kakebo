import glob
import setuptools

__version__ = "0.0.10"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

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
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    packages=[
        "django_kakebo", "django_kakebo.src.django_kakebo", "django_kakebo.src.django_kakebo.migrations",
        "django_kakebo.src.django_kakebo.templatetags", "django_kakebo.src.django_kakebo.views"
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
    ],
    python_requires=">=3.7",
)
