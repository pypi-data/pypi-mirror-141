Packaging example with no setup.cfg
===================================

.. image:: https://badge.fury.io/py/orbipatch.png
    :target: https://badge.fury.io/py/orbipatch

This example follows the guidelines in the
`request for testing`_
in order to test a
*minimal*
example.
It is probably not useful as additional testing data:
people have tested minimal examples.

.. _request for testing: https://discuss.python.org/t/help-testing-experimental-features-in-setuptools/13821

It does,
however,
show how this looks in practice,
at least for a simple package.
After cloning the repository,
build with

.. code::

    $ python -m build
    ...
    Successfully built orbipatch-2022.3.6.tar.gz and orbipatch-2022.3.6-py3-none-any.whl
    
Note the lack of any
"boilerplate"
files other than:

* The README (you are reading it right now)
* :code:`pyproject.toml`

In principle,
the README itself could also be embedded into
:code:`pyproject.toml`.
However,
having a README at the top
helps GitHub
(and most other version control servers)
display a nice explanation
when people see the project in a browser.

A few notes:

The
:code:`authors`
field needs to be carefully formatted:

.. code::

    authors = [{name = "Moshe Zadka", email = "orbipatch-author@devskillup.com"}]

It is a TOML
**list**
of
**objects**
(the equivalent to Python
**dicts**)
with the keys:

* :code:`name`
* :code:`email`

The
:code:`project.urls`
section treats the key
:code:`Home-Page`
as a special case,
using it as the
:code:`Home-Page`
metadata.
All other keys are used as
:code:`project_urls`
metadata.
