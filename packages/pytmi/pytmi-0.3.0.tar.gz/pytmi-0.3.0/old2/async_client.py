from typing import Optional, Union, cast, Type
from pytmi.message import Message, make_privmsg
from pytmi.common import *
import asyncio


class AsyncClient(object):
    def __init__(
        self,
        use_ssl: bool = True,
        use_task: bool = False,
        stream: Type[TmiBaseStream] = TmiStream,
        max_buffer_size: int = CLIENT_MAX_BUFFER_SIZE,
        message_interval: float = CLIENT_MESSAGE_INTERVAL,
    ) -> None:
        assert False and "TODO"
        self.__stream_type = stream
        self.__buf = TmiBuffer(max_buffer_size)

        self.__use_ssl = use_ssl
        self.__stream = self.__stream_type()

        self.__joined: Optional[str] = None
        self.__logged: bool = False

        self.__use_task: bool = use_task
        self.__task: Optional[asyncio.Task] = None
        self.__interval: float = message_interval  # Seconds

    async def login_oauth(
        self, token: str, nick: str, retry: int = CLIENT_MAX_RETRY
    ) -> None:
        if self.__logged:
            raise AttributeError("Alredy logged in")

        if not token.startswith("oauth:"):
            token = "oauth:" + token

        nick = nick.lower()

        if retry < 0:
            retry = CLIENT_MAX_RETRY

        backoff = 0

        # TODO: Improve connection error handling
        while retry > 0:
            retry -= 1
            try:
                await self.__login(token, nick)
                return
            except Exception as e:
                if not isinstance(e, (AssertionError, ConnectionError)):
                    raise

                # Wait a bit before retrying
                if backoff <= 1:
                    backoff += 1
                else:
                    backoff *= 2
                    await asyncio.sleep(backoff / 1.5)

        raise ConnectionError("Connection failed")

    async def login_anonymous(self, retry: int = CLIENT_MAX_RETRY) -> None:
        await self.login_oauth(*make_anonymous(), retry=retry)

    async def __login(self, token: str, nick: str) -> None:
        if self.__use_ssl:
            await self.__stream.connect(
                TMI_SERVER, TMI_SERVER_SSLPORT, ssl_ctx=ssl.create_default_context()
            )
        else:
            await self.__stream.connect(TMI_SERVER, TMI_SERVER_PORT)

        pass_command = "PASS " + token + "\r\n"
        await self.__stream.write_buf(pass_command.encode())

        nick_command = "NICK " + nick.lower() + "\r\n"
        await self.__stream.write_buf(nick_command.encode())

        welcome1 = f":tmi.twitch.tv 001 {nick} :Welcome, GLHF!\r\n"
        assert await self.__stream.read_buf() == welcome1.encode()

        welcome2 = f":tmi.twitch.tv 002 {nick} :Your host is tmi.twitch.tv\r\n"
        assert await self.__stream.read_buf() == welcome2.encode()

        welcome3 = f":tmi.twitch.tv 003 {nick} :This server is rather new\r\n"
        assert await self.__stream.read_buf() == welcome3.encode()

        welcome4 = f":tmi.twitch.tv 004 {nick} :-\r\n"
        assert await self.__stream.read_buf() == welcome4.encode()

        welcome5 = f":tmi.twitch.tv 375 {nick} :-\r\n"
        assert await self.__stream.read_buf() == welcome5.encode()

        welcome6 = f":tmi.twitch.tv 372 {nick} :You are in a maze of twisty passages, all alike.\r\n"
        assert await self.__stream.read_buf() == welcome6.encode()

        welcome7 = f":tmi.twitch.tv 376 {nick} :>\r\n"
        assert await self.__stream.read_buf() == welcome7.encode()

        # Capabilities
        for req, ack in TMI_CAPS:
            await self.__stream.write_buf(req)
            assert await self.__stream.read_buf() == ack

        self.__logged = True

        if self.__use_task:
            self.__task = asyncio.get_event_loop().create_task(self.__recv_task())

    async def __recv_message(self) -> bytes:
        line = await self.__stream.read_buf()

        if line == TMI_PING_MESSAGE:
            await self.__stream.write_buf(TMI_PONG_MESSAGE)
            line = await self.__stream.read_buf()

        return line

    async def __recv_task(self) -> None:
        while self.__logged:
            line = await self.__recv_message()
            self.__buf.append(line)
            await asyncio.sleep(self.__interval)

    async def logout(self) -> None:
        if not self.__logged:
            raise AttributeError("Not logged in")

        try:
            if self.__joined is not None:
                await self.part(self.__joined)
        except:
            self.__joined = None  # FIXME

        self.__logged = False
        await self.__stream.disconnect()

        if self.__use_task:
            # assert self.__task is not None
            # self.__task.cancel()

            # with suppress(asyncio.CancelledError):
            #    asyncio.get_event_loop().run_until_complete(self.__task)

            self.__task = None

    async def send_join(self, channel: str) -> None:
        if not self.__logged:
            raise AttributeError("Not logged in")

        if not channel.startswith("#"):
            channel = "#" + channel

        self.__joined = channel

        command = "JOIN " + channel + "\r\n"
        await self.__stream.write_buf(command.encode())

    async def send_join(self, channel: Optional[str] = None) -> None:
        if not self.__logged:
            raise AttributeError("Not logged in")

        if channel is None:
            channel = self.__joined
            if channel is None:
                raise AttributeError("Unspecified channel")

        channel = cast(str, channel)
        if not channel.startswith("#"):
            channel = "#" + channel

        command = "PART " + channel + "\r\n"
        await self.__stream.write_buf(command.encode())

        self.__joined = None

    async def send_privmsg(self, message: str, channel: Optional[str] = None) -> None:
        if not self.__logged:
            raise AttributeError("Not logged in")

        if channel is None:
            channel = self.__joined
            if channel is None:
                raise AttributeError("Unspecified channel")

        channel = cast(str, channel)
        if not channel.startswith("#"):
            channel = "#" + channel

        await self.__stream.write_buf(make_privmsg(channel, message))

    async def __get_raw(self) -> bytes:
        if not self.__logged:
            raise AttributeError("Not logged in")

        if self.__use_task:
            while self.__buf.empty():
                await asyncio.sleep(self.__interval)

            return self.__buf.pop()

        return await self.__recv_message()

    async def get_message(self, raw: bool = False) -> Union[Message, bytes]:
        if raw:
            return Message(await self.__get_raw())
        else:
            return await self.__get_raw()


__all__ = ["AsyncClient"]
