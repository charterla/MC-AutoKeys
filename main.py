import pydirectinput
import pyautogui
import keyboard
import os
import json
import asyncio


class runScript():
    def __init__(self):
        self.Queue = set()
        self.setup()

        keyboard.add_hotkey(self.script['trigger'], lambda: self.trigger())

        self.loop = asyncio.get_event_loop()
        self.task = asyncio.ensure_future(self.detect())
        self.loop.run_forever()
        pass

    def setup(self):
        with open('./script/running.json', mode='r', encoding='utf-8') as scriptData:
            self.script = json.load(scriptData)

    def trigger(self):
        if self.script['trigger'] not in self.Queue:
            self.Queue.add(self.script['trigger'])
        elif self.script['trigger'] in self.Queue:
            self.Queue.remove(self.script['trigger'])

        # print('pressed')
        pass

    async def detect(self):
        run = None

        while True:
            await asyncio.sleep(0)

            if self.script['trigger'] in self.Queue and run == None:
                run = asyncio.ensure_future(self.runTask())
            elif self.script['trigger'] not in self.Queue and run != None:
                if not run.cancelled():
                    run.cancel()
                else:
                    run = None

    async def runTask(self):
        while True:
            while self.script['trigger'] in self.Queue:
                for i in range(len(self.script['script']['type'])):
                    if self.script['script']['type'][i] == 'keyboard':
                        for time in range(int(self.script['script']['time'][i])):
                            pydirectinput.keyDown(
                                self.script['script']['key'][i])
                            await asyncio.sleep(float(self.script['script']['continue'][i]))

                            pydirectinput.keyUp(
                                self.script['script']['key'][i])
                            await asyncio.sleep(float(self.script['script']['interval'][i]))

                    elif self.script['script']['type'][i] == 'mouse':
                        for time in range(int(self.script['script']['time'][i])):
                            pydirectinput.mouseDown(
                                button=self.script['script']['key'][i])
                            await asyncio.sleep(float(self.script['script']['continue'][i]))

                            pydirectinput.mouseUp(
                                button=self.script['script']['key'][i])
                            await asyncio.sleep(float(self.script['script']['interval'][i]))


if __name__ == '__main__':
    runScript()
