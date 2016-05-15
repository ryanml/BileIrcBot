# Author: Ryan Lanese
# channel_ops.py

import time
import json
import requests
import random

class ChannelOps(object):
    # Commands accepted by this class
    COMMANDS = ['time', 'hello', 'kick']

    # Level Values
    # [ level_symbol, level_weight ]
    LEVELS = {
        '~': 4,
        '@': 3,
        '%': 2,
        '+': 1,
        '': 0
    }

    # Is initialized with a bot object and a channel
    def __init__(self, bot, channel):
        self.bot = bot
        self.channel = channel
        self.users = []

    # set_users - Given a list of users, sets self.users to a list of lists, each containing
    #             a user and their respective user level ex [['@', 'the_operator'], ['+', 'the_voice']]
    #   params:
    #      user_list - a list of concatenated levels and users
    def set_users(self, user_list):
        self.users = []
        u_s = user_list.split(' ')
        for u in u_s:
            user = ['', '']
            if not u[0].isalpha():
                user[0] = u[0]
                user[1] = u[1:]
            else:
                user[1] = u
            self.users.append(user)

    # get_user - Given a nick, returns a dictionary with the nick's user level if it exists
    #   params:
    #      nick - type: string, nick to fetch
    #   Returns:
    #      Dictionary or None if no user exists
    def get_user(self, nick):
        for user in self.users:
            if user[1] == nick.strip(' '):
                return {
                    'nick': nick.strip(' '),
                    'level': user[0]
                }
        return None

    # handle_command - Given a bot command, directs it to the correct function
    #   params:
    #      cmd_info - type: dictionary, a dictionary of bot command info
    def handle_command(self, cmd_info):
        command = cmd_info['command']
        if command in self.COMMANDS:
            if command == 'hello':
                self.say_hello(cmd_info)
            elif command == 'time':
                self.get_time(cmd_info)
            elif command == 'kick':
                self.kick_user(cmd_info)
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

    # get_time - Sends a call to IRC protocol for the channel's name list
    def get_names(self):
        self.bot.sock_send('NAMES ' + self.channel)

    # kick_user - Attempts to kick a given user
    #    params:
    #       cmd_info - type: dictionary, the dictionary containing command info
    def kick_user(self, cmd_info):
        to_kick = self.get_user(cmd_info['args'])
        if to_kick:
            cmd_user = self.get_user(cmd_info['user'])
            if self.LEVELS[cmd_user['level']] > self.LEVELS[to_kick['level']]:
                self.bot.sock_send('KICK ' + self.channel + ' ' + to_kick['nick'])
            else:
                self.send_chan_msg('Error: Failed Kick. Insufficient User Level')
        else:
            self.send_chan_msg('Error: Failed Kick. No Such User')
