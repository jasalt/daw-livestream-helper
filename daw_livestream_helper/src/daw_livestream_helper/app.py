"""
About
"""
import toga
import aiosc
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class OscServer(aiosc.OSCProtocol):
    def __init__(self):
        super().__init__(handlers={
            # '/sys/exit': lambda addr, path, *args: sys.exit(0),
            '//*': self.handle_message,
        })

    def handle_message(self, addr, path, *args):
        print("incoming message from {}: {} {}".format(addr, path, args))


class DAWLivestreamHelper(toga.App):
    def mock_button_fuction(self, widget, **kwargs):
        self.current_daw_title.text = "Mock button pressed..."

    def osc_switch_handler(self, widget, **kwargs):
        message = f"osc_switch is_on = {self.osc_switch.is_on}"
        print(message)
        self.current_daw_title.text = message

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

        ### Run Background tasks
        self.loop = self._impl.loop  # access asyncio.get_event_loop()

        # self.add_background_task( Coroutine )  # equals under the hood:
        # self.loop.call_soon(wrapped_handler(self, handler), self)

        coro = self.loop.create_datagram_endpoint(OscServer, local_addr=('127.0.0.1', 9000))
        self.loop.create_task(coro, name="osc_coro")

        ### Startup GUI
        self.main_window.show()
        

def main():
    return DAWLivestreamHelper()

if __name__ == '__main__':
    app = DAWLivestreamHelper('First App', 'org.beeware.helloworld')
    app.main_loop()