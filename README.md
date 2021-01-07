# DAW Livestream Helper

Listen DAW project file changes and automatically add them as chapter marks to livestream video chat and description to make videos more easy to view and process later by project name.

Using generic OSC connection for receiving project file data from DAW with example implementation for Bitwig which might be simple to implement for Ableton etc.

![Concept Image](https://github.com/jasalt/daw-livestream-helper/blob/master/210107-daw-livestream-helper.jpg)

## Draft UI
![Draft UI](https://github.com/jasalt/daw-livestream-helper/blob/master/210107-daw-livestream-helper-ui.png)

## TODO

- [X] Listen DAW project file changes
- [ ] Broadcast via OSC to Python
- [ ] Forward to Restream.io or Twitch chat
- [ ] Set chapter marks for Youtube video description
- [ ] Set project file into livestream video title (useful?)

## Example Youtube Video description chapter mark formatting 

Here I manually sent the opened project file name as a chat message, and later copy pasted the Twitch chat log into the Youtube description with some manual formatting.

https://www.youtube.com/watch?v=Melm6xq8gJI

Previously used to skim through livestream recordings adding project file names and "highlight parts" manually which was even more tedious.

## Supported systems

Built with Python 3.8.6 and [Toga](https://toga.readthedocs.io/en/latest/) GUI library.

Written and tested on MacOS 11.1 (Intel) and should work on Apple Silicon and with minor tweaks on Window 10/7 and Linux.