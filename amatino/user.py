"""
Amatino API Python Bindings
User Module
Author: hugh@amatino.io
"""
from amatino.internal.immutable import Immutable


class User:
    """
    A User is a human producer and consumer of data stored by Amatino. When you
    create an Amatino account on the Amatino website, a User is generated in
    your name. You can create other Users at will to serve the needs of your
    application. For example, you might wish to create an Amatino User to
    associate with each end-user of your application, in order to link financial
    information stored in Amatino with that end-user.

    Users created via the Amatino API cannot login or otherwise interact with
    the amatino.io website in any way. They are not eligbile to receive customer
    support from us directly (though you are most welcome to request customer
    support to assist you with users you create), and don't generate associated
    discussion forum accounts. You have absolute control over their lifecycle.
    They can make requests to the Amatino API on their own behalf.

    Generally, if you are creating User accounts for your fellow developers,
    you will want to do so in your billing dashboard. Doing so will allow them
    to manage their password, post to the discussion forums, and contact us for
    support. If you are creating Users to manage financial data inside your
    application, you will want to do so via the Amatino API.

    Users and Entities are woven together using permission graphs. Any User may
    be granted read and or write access to any Account in any Entity, whether
    they were created in the billing dashboard or via the Amatino API.

    If you are on a Fixed Price plan, each additional user you create in the
    Amatino API will count towards your monthly bill. If you are on a Pay Per
    Use plan, creating additional Users incurs no direct marginal cost. You can
    change your plan at any time.
    """

    def __init__(
        self,
        id_: int,
        email: str,
        name: str,
        handle: str,
        avatar_url: str
    ) -> None:

        self._id = id_,
        self._email = email,
        self._name = name,
        self._handle = handle,
        self._avatar_url = avatar_url

        return

    id_ = Immutable(lambda s: s._id)
    email = Immutable(lambda s: s._email)
    name = Immutable(lambda s: s._name)
    handle = Immutable(lambda s: s._handle)
    avatar_url = Immutable(lambda s: s._avatar_url)
