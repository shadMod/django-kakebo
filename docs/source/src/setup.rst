:orphan:

.. _setup:

Setup installation
=========================================

.. meta::
   :description: Glossary for the Pylons Project Documentation Style Guide.
   :keywords: Setup, Set-up, Installation

first of all, install the app with your favorite package manager:

e.g.:

.. code-block::

    pip install django-kakebo

Before deploy the code, some parameters must be entered in settings.py

Imports parameters

.. code-block:: python

    from django_kakebo import DIR_TEMPLATE, DJANGO_KAKEBO_TEMPLATETAGS, DIR_STATIC_KAKEBO, DIR_STATIC_USER

Install app

.. code-block:: python

    INSTALLED_APPS = [
        ...
        "django_kakebo",
        ...
    ]

Install templates and templatetags

.. code-block:: python

    TEMPLATES = [
        {
            ...
            "DIRS": [
                ...
                DIR_TEMPLATE,
                ...
            ],
            ...
            "OPTIONS": {
                ...
                "libraries": DJANGO_KAKEBO_TEMPLATETAGS,
                ...
            },
        },
    ]

.. warning::
    **DIR_TEMPLATE** is a string, while **DJANGO_KAKEBO_TEMPLATETAGS** is a dictionary

    If the key 'libraries' is already present, it should be added with the use of the update() method (see e.g.)

    .. code-block:: python

        TEMPLATES[0]['OPTIONS']['libraries'].update(DJANGO_KAKEBO_TEMPLATETAGS)

Added static files

.. code-block:: python

    STATICFILES_DIRS = [DIR_STATIC_KAKEBO, DIR_STATIC_USER]

.. note::
    obviously in case it was already instantiated, they should simply be added with the use of extends()

    .. code-block:: python

        STATICFILES_DIRS.extends(DIR_STATIC_KAKEBO, DIR_STATIC_USER)

In case a different field is used to get the user (other than auth.User.username => e.g. email or others) add:

.. code-block:: python

    USER_FIELD_KAKEBO = 'email'