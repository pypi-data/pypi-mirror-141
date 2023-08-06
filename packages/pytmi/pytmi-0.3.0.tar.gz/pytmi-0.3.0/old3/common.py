from typing import Tuple
import random


# Twitch IRC server `https://dev.twitch.tv/docs/irc/guide#connecting-to-twitch-irc`
TMI_SERVER = "irc.chat.twitch.tv"
TMI_SERVER_PORT = 6667
TMI_SERVER_SSLPORT = 6697

TMI_PING_MESSAGE = b"PING :tmi.twitch.tv\r\n"
TMI_PONG_MESSAGE = b"PONG :tmi.twitch.tv\r\n"

TMI_CAPS = [
    (
        f"CAP REQ :twitch.tv/{cap}\r\n".encode(),
        f":tmi.twitch.tv CAP * ACK :twitch.tv/{cap}\r\n".encode(),
    )
    for cap in ["membership", "tags", "commands"]
]


# Default client limits
# These are arbitrary values
CLIENT_MAX_RETRY = 8
CLIENT_MAX_BUFFER_SIZE = 128
CLIENT_MESSAGE_INTERVAL = 0.5


def make_anonymous() -> Tuple[str, str]:
    token = "random_string"
    nick = "justinfan" + str(random.randint(12345, 67890))
    return (token, nick)
