"""
About
"""
import toga
import aiosc
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from twitchio.ext import commands
from os import environ


class OscServer(aiosc.OSCProtocol):
    def __init__(self):
        super().__init__(handlers={
            # '/sys/exit': lambda addr, path, *args: sys.exit(0),
            '//*': self.handle_message,
        })

    def handle_message(self, addr, path, *args):
        print("incoming message from {}: {} {}".format(addr, path, args))
        project_name = args[0]
        app.daw_project_name.text = project_name
        if app.on_switch.is_on:
            print("Sending to Twitch chat")
            app.bot.send_message(f"[{project_name}]")


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(irc_token=environ['TWITCH_OAUTH'], nick='554music', prefix='!', #client_id='...'
                         initial_channels=['554music'])

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
        chan = app.bot.get_channel('554music')
        loop = app._impl.loop  # equals asyncio.get_event_loop()
        loop.create_task(chan.send(message))


class DAWLivestreamHelper(toga.App):
    def mock_button_fuction(self, widget, **kwargs):
        self.daw_project_name.text = "Mock button pressed..."

    def on_switch_handler(self, widget, **kwargs):
        message = f"on_switch is_on = {self.on_switch.is_on}"
        print(message)
        # self.daw_project_name.text = message

    async def start_bot(self):
        await self.bot.start

    def startup(self):
        """
        Construct and show the Toga application.
        """
        self.daw_project_name = toga.Label('Waiting for data...', style=Pack(padding=10))
        self.mock_button = toga.Button('mock_button', on_press=self.mock_button_fuction)

        self.on_switch = toga.Switch('Enable', on_toggle=self.on_switch_handler)
        self.on_switch.style.padding = 10
        self.on_switch.style.flex = 1

        self.twitch_input_label = toga.Label(text="Twitch settings")
        self.twitch_username_input = toga.TextInput(placeholder='username', on_change=None)
        self.twitch_channel_input = toga.TextInput(placeholder='channel', on_change=None)
        self.twitch_key_input = toga.PasswordInput(placeholder="auth token", on_change=None)

        self.twitch_settings_container = toga.Box(style=Pack(direction=COLUMN),
                                                  children=[self.twitch_input_label,   
                                                            self.twitch_username_input,
                                                            self.twitch_channel_input, 
                                                            self.twitch_key_input])

        main_box = toga.Box(style=Pack(direction=COLUMN,padding=10,flex=1),
                            children=[self.daw_project_name,   # self.mock_button, 
                                      self.twitch_settings_container, self.on_switch])

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box

        ### HACK Running background tasks

        # aiosc is uses lover level functions for running the example code
        # self.add_background_task( Coroutine ) -> equals under the hood:  
        #                                          self.loop.call_soon(wrapped_handler(self, handler), self)

        loop = self._impl.loop  # equals asyncio.get_event_loop()

        osc_coro = loop.create_datagram_endpoint(OscServer, local_addr=('127.0.0.1', 9000))
        osc_task = loop.create_task(osc_coro, name="osc_coro")

        self.bot = Bot()
        self.add_background_task(self.bot.start)  # works but sends one extra parameter which causes error

        ### Startup GUI
        self.main_window.show()
        

def main():
    return DAWLivestreamHelper()

if __name__ == '__main__':
    app = DAWLivestreamHelper('DAW Livestream Helper', 'com.saltiolabs')
    app.main_loop()