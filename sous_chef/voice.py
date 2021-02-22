import asyncio
import discord
from discord.ext import commands
import sounddevice as sd


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def join(self, ctx):
        """Join the voice channel the calling user is in."""

        voice = ctx.message.author.voice
        if not voice or not voice.channel:
            await ctx.channel.send(f'{ctx.message.author.mention} you need to join a voice channel.')
            return

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(voice.channel)

        voice_client = await voice.channel.connect()

        # we need 20ms audio from each read() call
        self.stream = sd.RawInputStream(samplerate=44100, blocksize=(48000//50), device='default', channels=2, dtype='int16')
        self.stream.start()

        class SousAudio(discord.AudioSource):
            def __init__(self, cog):
                self.cog = cog

            def is_opus(self):
                return False

            def read(self):
                buf, overflow = self.cog.stream.read(48000//50)
                return buf[:]
        
        voice_client.play(SousAudio(self))



    @commands.command()
    async def leave(self, ctx):
        """Leave the voice channel."""

        self.stream.stop()

        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        else:
            await ctx.channel.send(f'{ctx.message.author.mention} I need to join a voice channel to leave it.')
