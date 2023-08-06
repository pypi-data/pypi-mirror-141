"""Module containing stream related abstractions."""

import ssl
import socket
import abc
from typing import Union, Optional


class BaseStream(abc.ABC):
    """Asynchronous stream base class for the IRC-TMI protocol."""

    @abc.abstractmethod
    def connect(
        self, host: str, port: Union[int, str], ssl_ctx: Optional[ssl.SSLContext] = None
    ) -> None:
        """Create a connection to the server represented by `host` and `port`.
        If `ssl_ctx` is not `None` initiates an SSL connection.

        Must raise `AttributeError` if a connection is alredy in place.
        May raise `OSError` exceptions.
        """

    @abc.abstractmethod
    def disconnect(self) -> None:
        """Terminate the connection with the server.

        Must raise `AttributeError` if no connection is in place.
        May raise `OSError` exceptions.
        """

    @abc.abstractmethod
    def write(self, data: bytes) -> None:
        """Write to a buffer and when the delimiter `\\r\\n` is found flushes it.

        Must raise `AttributeError` if no connection is in place.
        May raise `OSError` exceptions.
        """

    @abc.abstractmethod
    def read(self) -> bytes:
        """Read from a buffered stream until the delimiter `\\r\\n` or EOF.

        Must raise `AttributeError` if no connection is in place.
        May raise `OSError` exceptions.
        """

    @abc.abstractproperty
    def connected(self) -> bool:
        """Return `True` if there is a connection in place, otherwise `False`."""


class SyncStream(BaseStream):
    """Stream class for the IRC-TMI protocol which provides SSL support."""

