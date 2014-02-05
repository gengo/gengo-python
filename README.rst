|Build Status|

Gengo Python Library (for the `Gengo API <http://gengo.com/api/>`__)
====================================================================

Translating your tools and products helps people all over the world
access them; this is, of course, a somewhat tricky problem to solve.
`Gengo <http://gengo.com/>`__ is a service that offers
human-translation (which is often of higher quality than machine
translation), and an API to manage sending in work and watching jobs.
This is a Python interface to make using the API simpler.

Installation & Requirements
---------------------------

Installing this library using pip is very simple:

::

    pip install gengo

Otherwise, you can install from source by getting the repo:

::

    git clone git://github.com/gengo/gengo-python.git

And then installing the library:

::

    python setup.py install

This will also install the ``requests`` package. If you're running on a
version of Python prior to 2.6, you'll need to install simplejson as
well:

::

    pip install simplejson

Tests - Running Them, etc
-------------------------

Gengo has a full suite of unit tests. To run them, make sure you have
the ``mock`` library installed, and then simply run:

::

    python setup.py test

If you wish to run a single test, such as
TestTranslationJobFlowFileUpload:

::

    python -m unittest -v gengo.tests.TestTranslationJobFlowFileUpload

Question, Comments, Complaints, Praise?
---------------------------------------

If you have questions or comments and would like to reach us directly,
please feel free to do so at the following outlets. We love hearing from
developers!

-  Email: api [at] gengo dot com
-  Twitter: `@gengoit <https://twitter.com/gengoit>`__
-  IRC: `#gengo <irc://irc.freenode.net/gengo>`__

If you come across any issues, please file them on the `Github project
issue tracker <https://github.com/gengo/gengo-python/issues>`__. Thanks!

Documentation
-------------

Full documentation can be found `here <http://developers.gengo.com>`__,
but anyone should be able to get a working script with the following:

.. code:: python

    from gengo import Gengo

    gengo = Gengo(
        public_key='your_public_key',
        private_key='your_private_key',
        sandbox=True,
    )

    print gengo.getAccountBalance()

All function definitions can be found inside gengo/mockdb.py as a
dictionary: the key of the dictionary entry is the function name, and
the parameters are exactly the same as specified in the `Gengo API
docs <http://developers.gengo.com>`__.

.. |Build Status| image:: https://secure.travis-ci.org/gengo/gengo-python.png
   :target: http://travis-ci.org/gengo/gengo-python
