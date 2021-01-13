# DAW Livestream Helper
![Mockup Logo and prototype GUI](https://github.com/jasalt/daw-livestream-helper/blob/master/docs/210109-proto.jpg)

Posts Bitwig Studio project file changes automatically to Twitch livestream chat.

## Running
To start sending project name change data from BWS via OSC, copy or symlink daw-livestream-helper.control.js to `Documents > Bitwig Studio > Controller Scripts` folder and add it as a control surface in settings.

Making a hardlink on Windows Powershell:

    New-Item -ItemType HardLink -Path "$HOME\Documents\Bitwig Studio\Controller Scripts\daw-livestream-helper.control.js" -Target ".\daw-livestream-helper.control.js"

Install dependencies `pip install -r requirements.txt` for Python (tested on 3.8.6), `cd daw_livestream_helper` and run `briefcase dev`. Alternatively run file `app.py` from VSCode for debugging.

For now, the default Twitch credentials can be loaded from environment variables:

    export TWITCH_OAUTH="oauth:secretkeydatahere"
    export TWITCH_USER="554music"
    export TWITCH_CHAN="554music"

If these are not supplied they have to be input before initializing Twitch connection (see BUGS section).

No errors are given for failed login for other than error console. Restart and try again if mistyped credentials before connecting.

### Supported systems

Based on Python 3.8.6 and Beeware [Toga](https://toga.readthedocs.io/en/latest/) native GUI application framework (0.3.0.dev24). 

Written and tested on MacOS 11.1 (Intel) where it's working 100%. Windows has a memory leak problem waiting for fix from Toga side (see later section). Should run on Linux but haven't tested.
 
# Development

![Concept Image](https://github.com/jasalt/daw-livestream-helper/blob/master/docs/210107-daw-livestream-helper.png)

Listens OSC connection (port 9000) for receiving project file data from Bitwig Controller API (aiosc library) and sends it to Twitch via IRC (TwitchIO library).

Should be quite straightforward to make this work with some other DAW software but I'm not planning to do something like that myself for free (fork it or ask for quote ;-).

## TODO

- [X] BWS: Listen for DAW project name changes 
- [X] BWS: Broadcast them via OSC to Python
- [X] Send project name changes to Twitch chat
- [X] BWS: Wait for audio engine to be online before notifying about project changes
- [X] Input for Twitch API key, username and channel
- [X] Toggle sending on/off
- [X] Mockup Icon
- [X] Package to executable
- [!] Windows support
- [ ] Save Twitch login data for next run (for packaged MacOS version)
- [ ] BWS: Read project BPM
- [ ] BWS: Read project genre

## Windows support status

There is a known Windows issue with Toga version `0.3.0.dev25` which breaks async functionality https://github.com/beeware/toga/issues/1166. Using `0.3.0.dev24` for now which functions but **has memory leak while waiting for a proper fix from Toga**. As a workaround I'm running this on Mac and connecting via LAN from Windows DAW machine (requires changing server address in `daw-livestream-helper.control.js`)

![Winforms](https://github.com/jasalt/daw-livestream-helper/blob/master/docs/210113-winforms.jpg)

- [X] Toga GUI works
- [X] Bitwig controller script works and connects aiosc_test.py
- [X] twitchio_test.py hellobot connects and sends echo back (bit slow?)
- [X] Problems running aiosc with Toga event loop ([Toga issue 1166](https://github.com/beeware/toga/issues/1166))
- [X] Problems running TwitchIO with Toga event loop *(RuntimeError: There is no current event loop in thread 'Dummy-1'.)* ([Toga issue 1166](https://github.com/beeware/toga/issues/1166))
- [ ] Memory leak ([Toga issue 1166](https://github.com/beeware/toga/issues/1166))

## Later

- [ ] Set project name changes to livestream video title
- [ ] Help setting chapter marks for Youtube video description
- [ ] Proper Icon
- [ ] BWS: add host configuration to controller script settings page

# Motivation 

While making music I find myself often jumping from project file to another and after starting to livestream  felt necessary to add manually add some chapter marks to the past live videos. Doing this manually in various degrees got tedious till I figured to simply copy paste the project name to the chat every time I change the project. That's what this tool basically does automatically.

Now this Twitch chat log can be copy pasted with minor modifications to the Youtube description to function as chapter marks. Will probably automate this part also after finding a simple method for it.

Example archived video on Youtube with chapter marks https://www.youtube.com/watch?v=Melm6xq8gJI.

# API notes etc.

## Twitch IRC Chat
Restream does not seem to have interface for sending chat messages, but has a relay function so messages sent to Twitch chat would work. Using async Twitch IRC library https://github.com/TwitchIO/TwitchIO

## Restream (for title changes)
- OAuth2 https://developers.restream.io/docs#overview
- Update Description https://developers.restream.io/docs#channel-meta

## Python version notes
Written on Python 3.8 which is last one that supports Windows 7. Python 3.9 does not yet support Toga dependency [pythonnet](https://github.com/pythonnet/pythonnet).

# Copyright Notice
The draft app icons are strictly for personal use as they might contain design elements that could be considered as intellectual property of some 3rd parties. 

Code Licensed under GPLv3.