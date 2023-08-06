Packaging example with no setup.cfg
===================================

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
