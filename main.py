from os import putenv
import pydirectinput
import pyautogui
import pynput
from pynput.keyboard import Key
import time
import os
import json
import asyncio

Queue = set()
with open('./script/running.json', mode='r', encoding='utf-8') as scriptData:
    script = json.load(scriptData)


async def runScript(key):
    while key in Queue:
        print(Queue, end=' ')
        await asyncio.sleep(100)
        '''for i in range(len(script['script']['type'])):
            if script['script']['type'][i] == 'keyboard':
                for tim in range(int(script['script']['time'][i])):
                    pydirectinput.keyDown(script['script']['key'][i])
                    time.sleep(float(script['script']['interval'][i]))
                    pydirectinput.keyUp(script['script']['key'][i])
            elif script['script']['type'][i] == 'mouse':
                for tim in range(int(script['script']['time'][i])):
                    pydirectinput.mouseDown(button=script['script']['key'][i])
                    time.sleep(float(script['script']['interval'][i]))
                    pydirectinput.mouseUp(button=script['script']['key'][i])'''


def on_press(key):
    if(key == eval(script['trigger'])):
        if key not in Queue:
            Queue.add(key)

            asyncio.run(runScript(key))
        elif key in Queue:
            Queue.remove(key)

        print("trigger", Queue)


def on_release(key):
    return True


if __name__ == '__main__':
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
