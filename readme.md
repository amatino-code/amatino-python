# Amatino Python

Amatino is a double-entry accounting system. It provides double entry accounting as a service via an HTTP API. Amatino Python is a library for interacting with the Amatino API from within a Python application. By using Amatino Python, a Python developer can utilise Amatino services without needing to deal with raw HTTP requests.

## About Amatino

Amatino gives you a full set of tools to store, organise and retrieve financial information. You don't need to set up databases or write any of your own double-entry accounting logic. All you need is this library, an [Amatino account (Try free for two weeks!)](https://amatino.io/subscribe), and you are off and running.

## Under construction

Right now, the Amatino API offers a full range of accounting services via HTTP requests. However, this Amatino Python library is in an 'Alpha' state. Its capabilities are limited. One class is available: `AmatinoAlpha`.

`AmatinoAlpha` is a thin wrapper around asynchronous HTTP requests to the Amatino API. It facilitates testing and experimentation with the Amatino API without having to resort to raw HTTP request manipulation and HMAC computation.

Amatino Python will eventually offer expressive, object-oriented interfaces for all Amatino API services. To be notified when Amatino Python enters a Beta state, with all capabilities available, sign up to the [Amatino Development Newsletter](https://amatino.io/newsletter).

In the mean time, you may wish to review [Amatino's HTTP documentation](https://amatino.io/documentation) to see what capabilities you can expect from Amatino Python in the future.

## Installation

Amatino Python may be installed via [PIP](https://pypi.org/project/amatino/).

````bash
$ pip install amatino
````

To use Amatino Python, you will need an active Amatino subscription. You can start a free trial at [https://amatino.io/subscribe](https://amatino.io/subscribe).

## Example Usage

The ````AmatinoAlpha```` object allows you to use the Amatino API without dealing with raw HTTP requests or HMACs. It lacks the expressive syntax, input validation, and error handling that Amatino Python will have in the beta stage.

Initialise an  `AmatinoAlpha` instance like so:

````Python
from Amatino import AmatinoAlpha

amatino_alpha = AmatinoAlpha(
    email="clever@cookie.com",
    secret="high entropy passphrase"
)
````

Requests may then be made:

````Python
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
````

Wherein `path`, `query_string`, `method` and `body` parameters are formed according to the requirements laid out in the [Amatino API HTTP documentation](https://amatino.io/documentation).

For example, the above request created an [Entity](https://amatino.io/documentation/entities). The requirements for Entity creation are available at https://amatino.io/documentation/entities#action-Create.

For more examples of `AmatinoAlpha` usage, see the [getting started guide](https://amatino.io/articles/getting-started).

## API stability & versioning


Amatino Python obeys the [Semantic Version](https://semver.org) convention. Until v1.0.0, the Python API (not to be confused with the Amatino HTTP API) should be considered unstable and liable to change at any time.

>**Watch out! API currently unstable!**

You can see available versions [in GitHub's releases section](https://github.com/amatino-code/amatino-python/releases) or [in PyPi's release history section](https://pypi.org/project/amatino/#history).

## Tell us what your think/want/like/hate

Please join us on the [Amatino discussion forums](https://amatino.io/discussion) and give us your feedback. We would love to hear from you. Amatino is in its earliest stages of development, and your feedback will influence the direction it moves in.

Pull requests, comments, issues, forking, and so on are also [most welcome on Github](https://github.com/amatino-code/amatino-python)!

## Useful links

 - [Amatino home](https://amatino.io)
 - [Development blog](https://amatino.io/blog)
 - [Development newsletter](https://amatino.io/newsletter)
 - [Discussion forum](https://amatino.io/discussion) 
 - [More Amatino client libraries](https://github.com/amatino-code)
 - [Documentation](https://amatino.io/documentation)
 - [Billing and account management](https://amatino.io/billing)
 - [About Amatino Pty Ltd](https://amatino.io/about)

## Get in contact

To quickly speak to a human about Amatino, [email hugh@amatino.io](mailto:hugh@amatino.io) or [yell at him on Twitter (@hugh_jeremy)](https://twitter.com/hugh_jeremy).
