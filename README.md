[![Build Status](https://secure.travis-ci.org/gengo/gengo-python.png)](http://travis-ci.org/gengo/gengo-python)

Gengo Python Library (for the [Gengo API](http://gengo.com/))
========================================================================================================
Translating your tools and products helps people all over the world access them; this is, of course, a
somewhat tricky problem to solve. **[Gengo](http://gengo.com/)** is a service that offers human-translation
(which is often a higher quality than machine translation), and an API to manage sending in work and watching
jobs. This is a Python interface to make using the API simpler.

Installation & Requirements
-------------------------------------------------------------------------------------------------------
Installing the library is fairly simple:

Get the repo:

    git clone git://github.com/myGengo/mygengo-python.git

And then install the library:

    sudo python setup.py install

This will also install the `requests` package. If you're running on a version of Python prior to 2.6, you'll need to install simplejson as well:

     sudo pip install simplejson


Tests - Running Them, etc
------------------------------------------------------------------------------------------------------
Gengo has a full suite of unit tests. To run them, export your public and private keys in the shell like so:

```shell
export GENGO_PUBKEY='your public key here'
export GENGO_PRIVKEY='your private key here'
```

Then grab the source, head into the gengo directory, and execute the tests file like so:

    python tests.py

Note that some of the tests rely on some deferred actions so there are timeouts (sleep) which you might have to adjust.

Question, Comments, Complaints, Praise?
------------------------------------------------------------------------------------------------------
If you have questions or comments and would like to reach us directly, please feel free to do
so at the following outlets. We love hearing from developers!

Email: api [at] gengo dot com
Twitter: **[@gengoit](https://twitter.com/gengoit)**

If you come across any issues, please file them on the **[Github project issue tracker](https://github.com/myGengo/mygengo-python/issues)**. Thanks!


Documentation
-----------------------------------------------------------------------------------------------------
Full documentation can be found **[here](http://developers.gengo.com)**, but anyone should be able to
get a working script with the following:

``` python
from gengo import Gengo

gengo = Gengo(
    public_key='your_public_key',
    private_key='your_private_key',
    sandbox=True,
)

print gengo.getAccountBalance()
```

All function definitions can be found inside gengo/mockdb.py as a dictionary: the
key of the dictionary entry is the function name, and the parameters are exactly the same as specified
over on the **[Gengo API docs](http://developers.gengo.com)**.
