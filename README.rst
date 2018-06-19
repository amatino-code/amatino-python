Amatino Python
==============

Amatino is a double entry accounting system. It provides double entry accounting 
as a service. Amatino is served via an HTTP API. Amatino Python is a library for 
interacting with the Amatino API from within a Python application. By using
Amatino Python, a Python developer can utilise Amatino services without needing
to deal with raw HTTP requests.

Under Construction
------------------

Amatino Python is in an alpha state. It is not yet ready for widespread use
and should not be used by anyone for anything important.


Right now, Amatino Python's capabilities are limited. There is one class
available: AmatinoAlpha. AmatinoAlpha is a thin wrapper arround HTTP requests 
to the Amatino API. It facilitates testing an experimentation with the
Amatino API without having to resort to raw HTTP request manipulation and
HMAC generation.

To be notified when Amatino Python enters a beta state, with all capabilities
available, sign up to the Amatino Development Newsletter at
<https://amatino.io/newsletter/>.

In the mean time, you may wish to review Amatino's HTTP documentation
at <https://amatino.io/documentation/http>, to see what capabilities
you can expect from Amatino Python in future.

Installation
------------

Amatino Python may be installed via ``pip``::

    $ pip install amatino

Example Usage
-------------

During it's alpha stage, Amatino Python is limited to the ``AmatinoAlpha``
object. ``AmatinoAlpha`` is a thin wrapper around raw HTTP requests to the
Amatino API. It allows you to make requests to the Amatino API without
dealing with raw HTTP requests and HMACs, but lacks the expressive syntax,
input validation, and error handling that Amatino Python will have in the
beta stage.

The ``AmatinoAlpha`` object may be initialised like so::

    amatino_alpha = AmatinoAlpha(
        email="clever@cookie.com",
        secret="high entropy passphrase"
    )

And then requests may be made::

    entity = amatino_alpha.request(
        path="/entities",
        query_string=None,
        method="POST"
        body=[{
            "name": "My First Entity",
            "description": None,
            "region_id": None
        }]
    )

Wherein ``path``, ``query_string``, ``method`` and ``body`` parameters are
formed according to the requirements laid out in the Amatino API's
HTTP documentation: <https://amatino.io/documentation/http>.

For more examples of ``AmatinoAlpha`` usage, see the getting started guide at
<https://amatino.io/articles/getting_started>.