=======
MAGNets
=======


.. image:: https://img.shields.io/pypi/v/magnets.svg
        :target: https://pypi.python.org/pypi/magnets

.. image:: https://travis-ci.com/meghnathomas/MAGNets.svg?branch=master
    :target: https://travis-ci.com/meghnathomas/MAGNets

.. image:: https://readthedocs.org/projects/magnets/badge/?version=latest
        :target: https://magnets.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pepy.tech/badge/magnets
        :target: https://pepy.tech/project/magnets
        :alt: PyPI - Downloads


A Python package to aggregate and reduce water distribution network models


Overview
--------

MAGNets is a Python package designed to perform the reduction and aggregation of water distribution network models. The software is capable of reducing a network around an optional operating point and allows the user to customize which junctions they would like retained in the reduced model. 

Installation: Stable release
--------

To install MAGNets, run this command in your terminal:

.. code:: python

   pip install magnets

This is the preferred method to install MAGNets, as it will always install the most recent stable release.

If you don’t have pip installed, this `Python installation guide`_ can guide you through the process.

.. _`Python installation guide`: https://docs.python-guide.org/starting/installation/


Installation: From sources
--------

The sources for MAGNets can be downloaded from the Github repo.

You can either clone the public repository:

.. code:: python

    git clone git://github.com/meghnathomas/magnets
    
Or download the tarball:

.. code:: python

    curl -OJL https://github.com/meghnathomas/magnets/tarball/master
    
Once you have a copy of the source, you can install it with:

.. code:: python

    python setup.py install
    

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
