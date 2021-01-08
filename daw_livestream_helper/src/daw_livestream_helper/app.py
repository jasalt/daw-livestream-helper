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
        app.current_daw_title.text = args
        print("incoming message from {}: {} {}".format(addr, path, args))


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


class DAWLivestreamHelper(toga.App):
    def mock_button_fuction(self, widget, **kwargs):
        self.current_daw_title.text = "Mock button pressed..."

    def osc_switch_handler(self, widget, **kwargs):
        message = f"osc_switch is_on = {self.osc_switch.is_on}"
        print(message)
        self.current_daw_title.text = message

    async def start_bot(self):
        await self.bot.start

    def startup(self):
        """
        Construct and show the Toga application.
        """
        self.current_daw_title = toga.Label('Waiting for data...', style=Pack(padding=10))
        self.mock_button = toga.Button('mock_button', on_press=self.mock_button_fuction)

        self.osc_switch = toga.Switch('Enable OSC Listener', on_toggle=self.osc_switch_handler)
        self.osc_switch.style.padding = 10
        self.osc_switch.style.flex = 1

        main_box = toga.Box(style=Pack(direction=COLUMN,padding=10,flex=1),
                            children=[self.current_daw_title, self.mock_button, 
                                      self.osc_switch])


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