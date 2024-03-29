"""
About
"""
import toga
import aiosc
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from twitchio.ext import commands
from os import environ

import socket

app = None

class OscServer(aiosc.OSCProtocol):
    def __init__(self):
        print("Initializing OSC connection on port 9000")
        super().__init__(handlers={
            # '/sys/exit': lambda addr, path, *args: sys.exit(0),
            '//*': self.handle_message,
        })

    def handle_message(self, addr, path, *args):
        print("incoming message from {}: {} {}".format(addr, path, args))
        project_name = args[0].replace('|','@')
        app.daw_project_name.text = project_name  # BUG gets cut off, some problem with encoding?
        if app.switch.value:
            app.bot.send_message(project_name)


class Bot(commands.Bot):
    def __init__(self):
        global app
        super().__init__(irc_token=app.twitch_key_input.value, nick=app.twitch_user_input.value, prefix='!', #client_id='...'
                         initial_channels=[app.twitch_channel_input.value])

    async def start(self,discarded_arg):
        """|coro|
        
        HACK Overrides method and adds extra fn argument that gets passed during Toga's add_background_task

        An asynchronous call which starts the IRC Bot event loop.

        This should only be used when integrating Twitch Bots with Discord Bots.
        :meth:`.run` should be used instead.

        .. warning::
            Do not use this function if you are using :meth:`.run`
        """
        await self._ws._connect()

        try:
            await self._ws._listen()
        except KeyboardInterrupt:
            pass
        finally:
            self._ws.teardown()

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    def send_message(self, message):
        global app
        chan = app.bot.get_channel(app.twitch_channel_input.value)  # should be self.bot?
        loop = app._impl.loop  # equals asyncio.get_event_loop()
        loop.create_task(chan.send(f"[{message}]"))
        print("Sending to Twitch chat")


class DAWLivestreamHelper(toga.App):
    def send_button_fuction(self, widget, **kwargs):
        self.bot.send_message(self.daw_project_name.text)

    def switch_toggle_handler(self, widget, **kwargs):
        message = f"switch.value = {self.switch.value}"
        print(message)
        # self.daw_project_name.text = message

    async def start_bot(self):
        await self.bot.start

    def twitch_connect(self, widget, *kwargs):
        self.bot = Bot()
        self.add_background_task(self.bot.start)  # works but sends one extra parameter which causes error
        widget.label = "Connected"
        widget.enabled = False


    def startup(self):
        """
        Construct and show the Toga application.
        """
        self.daw_project_name_title = toga.Label(text="Project name:", style=Pack(color="#808080"))
        self.daw_project_name = toga.Label('Waiting for data...')

        self.daw_project_name_container = toga.Box(children=[self.daw_project_name_title,
                                                             self.daw_project_name],
                                                             style=Pack(direction=ROW, padding=10))

        local_ip = '127.0.0.1'

        self.hostname_title = toga.Label(text="Listening on:", style=Pack(color="#808080"))
        self.hostname = toga.Label(local_ip + ":9000")

        self.hostname_container = toga.Box(children=[self.hostname_title,
                                                             self.hostname],
                                                             style=Pack(direction=ROW, padding=10))

        self.twitch_input_label = toga.Label(text="Twitch settings")

        # Sets initial values from environment variables TWITCH_USER TWITCH_CHAN TWITCH_OAUTH  
        # TODO Store from user input for next launch

        # BUG on Mac 11.1: the input values get erased if input focus changes to another input field
        # WORKAROUND: focus other application window after input

        self.twitch_user_input = toga.TextInput(initial=environ.get('TWITCH_USER', None), 
                                                    placeholder='username')
        self.twitch_channel_input = toga.TextInput(initial=environ.get('TWITCH_CHAN', None), 
                                                   placeholder='channel')
        self.twitch_key_input = toga.PasswordInput(initial=environ.get('TWITCH_OAUTH', None), 
                                                   placeholder="auth token")

        self.twitch_settings_container = toga.Box(style=Pack(direction=COLUMN, padding=10),
                                                  children=[self.twitch_input_label,   
                                                            self.twitch_user_input,
                                                            self.twitch_channel_input, 
                                                            self.twitch_key_input])

        self.twitch_connect_button = toga.Button('Connect', on_press=self.twitch_connect, style=Pack(flex=0.5, padding_right=5))
        self.send_button = toga.Button('Send current project name', on_press=self.send_button_fuction, style=Pack(flex=1))
        self.switch = toga.Switch('Enable automatic sending', on_change=self.switch_toggle_handler, style=Pack(flex=1, padding_left=10, padding_top=3))

        self.twitch_controls_container = toga.Box(style=Pack(direction=ROW, padding=10),
                                                  children=[self.twitch_connect_button, self.send_button, self.switch])

        main_box = toga.Box(style=Pack(direction=COLUMN,padding=10,flex=1),
                            children=[self.hostname_container, self.daw_project_name_container,
                                      self.twitch_settings_container, 
                                      self.twitch_controls_container])

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        ### HACK Running background tasks

        # aiosc is uses lover level functions for running the example code
        # self.add_background_task( Coroutine ) -> equals under the hood:  
        #                                          self.loop.call_soon(wrapped_handler(self, handler), self)

        loop = self._impl.loop  # equals asyncio.get_event_loop()

        osc_coro = loop.create_datagram_endpoint(OscServer, local_addr=('0.0.0.0', 9000))
        osc_task = loop.create_task(osc_coro, name="osc_coro")

        # Connect Twitch automatically if credentials are set 
        if environ.get('TWITCH_USER', None) and environ.get('TWITCH_CHAN', None) and environ.get('TWITCH_OAUTH', None):
            self.twitch_connect(self.twitch_connect_button)

        ### Startup GUI
        self.main_window.show()
        

def main():
    global app
    app = DAWLivestreamHelper()
    return app


def main_cli():
    '''Hacky way to run it via command line (for temporary Windows support). 
       Uses mock object to mimick Toga app object. 
       Restructuring of this whole file recommended. '''
    import asyncio
    from unittest.mock import MagicMock
    global app
    app = MagicMock()
    app.switch.value = True

    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print("Listening on " + local_ip + ":9000")

    loop = asyncio.get_event_loop()
    app._impl.loop = loop

    osc_coro = loop.create_datagram_endpoint(OscServer, local_addr=('0.0.0.0', 9000))
    osc_task = loop.create_task(osc_coro, name="osc_coro")

    app.twitch_user_input.value = environ.get('TWITCH_USER', None)
    app.twitch_channel_input.value = environ.get('TWITCH_CHAN', None)
    app.twitch_key_input.value = environ.get('TWITCH_OAUTH', None)

    app.bot = Bot()
    app.bot.run()    


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:  # Run via command line by passing any argument
        main_cli()
        exit(1)

    app = DAWLivestreamHelper('DAW Livestream Helper', 'com.saltiolabs')
    app.main_loop()
