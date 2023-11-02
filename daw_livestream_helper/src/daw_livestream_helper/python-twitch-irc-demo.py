from python_twitch_irc import TwitchIrc
from os import environ

# Simple echo bot.
class MyOwnBot(TwitchIrc):
    def on_connect(self):
         self.join('#twitchname')

    # Override from base class
    def on_message(self, timestamp, tags, channel, user, message):
        self.message(channel, message)

client = MyOwnBot('MyBot', environ['TWITCH_OAUTH']).start()
client.message("twitchname", "testingtest")
client.handle_forever()
