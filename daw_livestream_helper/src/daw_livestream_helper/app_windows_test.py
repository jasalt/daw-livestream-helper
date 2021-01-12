#! /usr/bin/env python3

import toga
from toga.style.pack import CENTER, COLUMN, ROW, Pack
import asyncio

# Adding tasts fails on Windows Python 3.8.6

class AsyncTest(toga.App):
    async def atest(self):
        print("start task")
        await asyncio.sleep(1)
        print('task ran')

    def button_handler(self, widget):
        self.add_background_task(self.atest())
        
    async def button2_handler(self, widget):
        print("start task")
        await asyncio.sleep(1)
        print('task ran')

    def startup(self):
        self.main_window = toga.MainWindow(title=self.name)
        self.button = toga.Button('add_bg_task', on_press=self.button_handler)
        self.button2 = toga.Button('async_handler', on_press=self.button2_handler)

        main_box = toga.Box(children=[self.button,self.button2])
        self.main_window.content = main_box
        self.main_window.show()

def main():
    app = AsyncTest('AsyncTest', 'org.beeware.asynctest')
    return app


if __name__ == '__main__':
    main().main_loop()