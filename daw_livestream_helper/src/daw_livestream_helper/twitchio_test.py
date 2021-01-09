from twitchio.ext import commands
from os import environ
import asyncio


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(irc_token=environ['TWITCH_OAUTH'], nick='554music', prefix='!', #client_id='...'
                         initial_channels=['554music'])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a different decorator
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')

    def send_message(self, channel, message_content):
        ''' Call from external code to send message to a channel. '''
        chan = self.get_channel(channel)
        loop = asyncio.get_event_loop()
        loop.create_task(chan.send(message_content), name="msg_coro")

bot = Bot()
bot.run()

