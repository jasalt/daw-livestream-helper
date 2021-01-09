# DAW Livestream Helper

Listen DAW project file changes and automatically add them as chapter marks to livestream video chat and description to make videos more easy to view and process later by project name.

Using generic OSC connection for receiving project file data from DAW with example implementation for Bitwig Studio ("BWS") which might be simple to implement for Ableton etc.

Behind the scenes video of building this https://www.instagram.com/stories/highlights/17883447325989693/ (requires Instagram account, sadly).

![Concept Image](https://github.com/jasalt/daw-livestream-helper/blob/master/docs/210107-daw-livestream-helper.png)

## Running
To start sending project name change data from BWS side via OSC, copy or symlink daw-livestream-helper.control.js to `Documents > Bitwig Studio > Controller Scripts` folder and add it as a control surface in settings.

Install dependencies `pip install -r requirements.txt` for Python (tested on 3.8.6), `cd daw_livestream_helper` and run `briefcase dev`. Alternatively run file `app.py` from VSCode for debugging.

For now, the default Twitch credentials can be loaded from environment variables:

    export TWITCH_OAUTH="oauth:secretkeydatahere"
    export TWITCH_USER="554music"
    export TWITCH_CHAN="554music"

If these are not supplied they have to be input before initializing Twitch connection (see BUGS section).

## Draft UI
![Draft UI](https://github.com/jasalt/daw-livestream-helper/blob/master/docs/210107-daw-livestream-helper-ui.png)

## TODO

- [X] BWS: Listen for DAW project name changes 
- [X] BWS: Broadcast them via OSC to Python
- [X] Send project name changes to Twitch chat
- [X] BWS: Wait for audio engine to be online before notifying about project changes
- [X] Input for Twitch API key, username and channel
- [X] Toggle sending on/off
- [ ] Icon
- [ ] Windows support

## BUGS

- [ ] MacOS 11.1 the input values get erased if input focus changes to another input field, workaround is to focus any other application window after input (not tested elsewhere)

###  Later

- [ ] Set project name changes to livestream video title
- [ ] Set chapter marks for Youtube video description (needs to be defined better)

## Example Youtube Video description chapter mark formatting 

Here I manually sent the opened project file name as a chat message, and later copy pasted the Twitch chat log into the Youtube description with some manual formatting.

https://www.youtube.com/watch?v=Melm6xq8gJI

Previously used to skim through livestream recordings adding project file names and "highlight parts" manually which was even more tedious.

## API notes
- OAuth2 https://developers.restream.io/docs#overview
- Update Description https://developers.restream.io/docs#channel-meta

Restream does not seem to have interface for sending chat messages, but has a relay function so messages sent to Twitch chat would work.

- Async Twitch API wrapper https://github.com/TwitchIO/TwitchIO


## Supported systems

Built with Python 3.8.6 and [Toga](https://toga.readthedocs.io/en/latest/) GUI library.

Written and tested on MacOS 11.1 (Intel) and Windows 10. Should work on Apple Silicon and on Window 7 and Linux with minor tweaks.