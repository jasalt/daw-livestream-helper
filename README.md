# DAW Livestream Helper

Listen DAW project file changes and automatically add them as chapter marks to livestream video chat and description to make videos more easy to view and process later by project name.

Using generic OSC connection for receiving project file data from DAW with example implementation for Bitwig Studio ("BWS") which might be simple to implement for Ableton etc.

Behind the scenes video clips of building this https://www.instagram.com/stories/highlights/17883447325989693/.

![Concept Image](https://github.com/jasalt/daw-livestream-helper/blob/master/210107-daw-livestream-helper.jpg)

## Running
Install dependencies `pip install -r requirements.txt` for Python (tested on 3.8.6), `cd daw_livestream_helper` and run `briefcase dev`. Alternatively run file `app.py` from VSCode for debugging.

For now, set Twitch OAuth token (https://twitchapps.com/tmi/) as environment variable TWITCH_OAUTH.

## Draft UI
![Draft UI](https://github.com/jasalt/daw-livestream-helper/blob/master/210107-daw-livestream-helper-ui.png)

## TODO

- [X] BWS: Listen for DAW project name changes 
- [X] BWS: Broadcast them via OSC to Python
- [X] Send project name changes to Twitch chat
- [ ] Set project name changes to livestream video title

###  Later

- [ ] BWS: Wait for audio engine to be online before notifying about project changes
- [ ] Twitch API key password input
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

Written and tested on MacOS 11.1 (Intel) and should work on Apple Silicon and with minor tweaks on Window 10/7 and Linux.