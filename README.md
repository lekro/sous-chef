What do you think I am, a **sous-chef**?

This is a discord bot that attempts to provide the missing "patch cable"
for "go live" streams broadcast from Linux. The goal is to be extremely simple -
this is really a "hack fix" until discord finds a solution for this problem.

The idea is that this bot will listen on some input device and play that
through discord.

*Note: this is just provided in case it may be useful. Use at your own peril.
Feel free to make changes if it doesn't work for you!*

## Usage

- Clone this repository somewhere
- Do the [usual bot setup](https://discordpy.readthedocs.io/en/latest/discord.html)
- Prepare a virtualenv: `python3 -m venv venv`
- Activate it: `. venv/bin/activate`
- Install required dependencies: `pip3 install discord.py[voice] sounddevice yaml numpy scipy`
- Put token in `config.yml`, following example
- Run with `python3 -m sous_chef`

## Usage for me

My audio is basically managed by [JACK](https://jackaudio.org/),
so I simply run `pacmd load-module module-jack-sink`, point Dolphin to the
new JACK sink and route it in JACK to "system". In pavucontrol, I assign
"Monitor of Jack Sink-01" to the sous-chef audio stream.

In this way, any pulseaudio or JACK stream can be routed (possibly using
module-jack-source) into sous-chef.

As usual, your mileage may vary. If using plain pulseaudio, you could probably
achieve the same thing using a null sink and loopback device.
