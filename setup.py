import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_kakebo",
    version="0.0.5",
    author="shadMod",
    author_email="support@shadmod.it",
    description="A simple site made with django and exploiting the kakebo method",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shadMod/django-kakebo/",
    # download_url="https://github.com/shadMod/django-jsheet/archive/refs/tags/0.2.4.tar.gz",
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
        "django_kakebo", "django_kakebo.src.django_kakebo"
    ],
    data_files=[
        ("themes", ["django_kakebo/src/themes/basic/home/index.html"]),
    ],
    python_requires=">=3.7"
)
