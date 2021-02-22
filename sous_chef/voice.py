import asyncio
import discord
from discord.ext import commands
import sounddevice as sd
import numpy as np
from scipy.signal import resample


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
        self.stream = sd.InputStream(blocksize=100, device='default', channels=2, dtype='int16')
        blocksize = int(self.stream.samplerate) // 50
        target_samplerate = 48000
        target_blocksize = 48000 // 50
        self.stream.start()

        # This is implemented in a very simple way. We maintain a rolling window
        # of the audio of size blocksize*3 so as to avoid window edge effects.
        # At each read from the sound device, we put it into the last part
        # of the rolling window, resample the rolling window into the output
        # buffer, and send its center bit to discord.

        class SousAudio(discord.AudioSource):
            def __init__(self, cog):
                self.cog = cog
                self.window = np.zeros((blocksize * 3, 2), dtype='int16') # buffer

            def is_opus(self):
                return False

            def read(self):
                # Move the buffers over
                self.window[:2*blocksize] = self.window[blocksize:]

                # Read into last part of window
                self.window[2*blocksize:, ...], overflow = self.cog.stream.read(blocksize)

                # Resample to 48 kHz sampling rate
                rs_window = resample(self.window, target_blocksize * 3).astype('int16')

                # Output the middle part of the buffer
                return rs_window[target_blocksize:2*target_blocksize].tobytes()
        
        voice_client.play(SousAudio(self))



    @commands.command()
    async def leave(self, ctx):
        """Leave the voice channel."""

        self.stream.stop()

        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
        else:
            await ctx.channel.send(f'{ctx.message.author.mention} I need to join a voice channel to leave it.')
