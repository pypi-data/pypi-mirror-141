from typing import Optional, Union
from pytmi.message import Message
from pytmi.common import CLIENT_MAX_RETRY, make_anonymous
import ssl
import socket


class SyncClient(object):
    def __init__(self, use_ssl: bool = True) -> None:

        self.__use_ssl = use_ssl
        self.__buffer = []
        self.__socket = None

    def login_oauth(self, token: str, nick: str, retry: int = CLIENT_MAX_RETRY) -> None:
        if not token.startswith("oauth:"):
            token = "oauth:" + token


    def login_anonymous(self, retry: int = CLIENT_MAX_RETRY) -> None:
        self.login_oauth(*make_anonymous(), retry=retry)

    def logout(self) -> None:
        pass

    def send_join(self, channel: str) -> None:
        pass

    def send_part(self, channel: Optional[str] = None) -> None:
        pass

    def send_privmsg(self, message: str, channel: Optional[str] = None) -> None:
        pass

    def get_message(self, raw: bool = False) -> Union[Message, bytes]:
        pass

__all__ = ["SyncClient"]
