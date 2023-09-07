.. django_kakebo documentation master file
    created on 02/09/2023 16:00

Django Kakebo docs
==================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

A simple site made with django and exploiting the kakebo method.

Indices and tables
~~~~~~~~~~~~~~~~~~

 * :ref:`setup`
 * :ref:`django_kakebo_models`

The Kakebo (*Japanese: 家計簿*) is a method of household savings and financial management method originated and developed in Japan.
An early copy of a kakebo was published by journalist Motoko Hani (in 1904).

Literally translatable as "**household ledger**"; there are different types where the structure changes, but the basic idea is the same.

At the beginning of the month: the user notes the income and expenses needed for the initial month and decides on some sort of savings goal, adding any cues or resolutions.
On a daily basis: the user records his or her expenses, which are added up at the end of the week and at the end of the month.\
At the end of the month: the user draws up an end-of-month balance sheet with any notes and/or verification of why the goal imposed at the beginning of the month was not met.

In addition to expenses and income, also written in the Kakebo are: thoughts and observations, with the goal of increasing awareness of one's consumption.

In this project, a site is developed through python3 (with the use of the django framework) that brings back the same spirit as the traditional Kakebo, giving the user a clean and usable interface right out of the box, with the simple installation of the package/app.\

Included in the package is:

 * '**Home Page**' : can be deactivated from settings's project
 * **'user' app** : which allows user management (login and registration // with reCAPTCHA)
