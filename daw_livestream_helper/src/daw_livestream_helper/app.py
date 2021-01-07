"""
About
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


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
        self.main_window.show()


def main():
    return DAWLivestreamHelper()
