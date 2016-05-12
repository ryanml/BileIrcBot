# Author: Ryan Lanese

import time
import json
import requests
import random

class ChannelOps(object):
    # Commands accepted by this class
    COMMANDS = ['time', 'hello']
    # Creates tokens for user levels
    FOUNDER = '~'
    OPERATOR = '@'
    HALF_OPERATOR = '%'
    VOICE = '+'

    # Is initialized with a bot object and a channel
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.users = []

    def handle_command(self, cmd_info):
        command = cmd_info['command']
        if command in self.COMMANDS:
            if command == 'hello':
                self.say_hello(cmd_info)
            elif command == 'time':
                self.get_time(cmd_info)
        else:
            self.send_chan_msg("Command $" + command + " does not exist.")

    # send_chan_msg - Sends message out to channel via socket
    #   params:
    #      msg - type: string, the message to send out to the channel
    def send_chan_msg(self, msg):
        self.bot.sock_send('PRIVMSG ' + self.channel + ' :' + str(msg))

    # send_priv_msg - Sends a private message to a given user via socket
    #    params:
    #      user - type: string, the user to send the private message to
    #      msg - type: string, the message to send
    def send_priv_msg(self, user, msg):
        self.bot.sock_send('PRIVMSG ' + user + ' :' + msg)

    # say_hello - Responds with a message to the user issuing the command
    #    params:
    #       cmd_info - type: dictionary, the dictionary containing command info
    def say_hello(self, cmd_info):
        self.send_priv_msg(cmd_info['user'], 'Hello there, ' + cmd_info['user'] + '!')

    # get_time - Gets and formats the current time and sends it out to channel
    #    params:
    #       cmd_info - type: dictionary, the dictionary containing command info
    def get_time(self, cmd_info):
        current_time = time.strftime('%H:%M:%S [%Z]')
        self.send_chan_msg('The current time is: \x02' + current_time + '\x02')
