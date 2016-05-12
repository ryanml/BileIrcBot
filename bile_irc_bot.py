# Author: Ryan Lanese
import socket
import time
from channel_ops import *

class BileIrcBot(object):
    # Define Port
    PORT = 6667
    # Constructor
    # Params:
    #   server - type: string, the server to connect to ex 'irc.rizon.net'
    #   nick - type: string, the nickname to use for the bot ex 'BileBot'
    #   password - type: string, the password to authenticate the bot ex 'pass123'
    #   channels - type: list, a list of tuples containg the channels and their respective passwords
    #              If the channel does not have a password, False may be passed in its place
    #              Ex: [('#channelOne', 'passwordOne'), ('#channelTwo', False)]
    def __init__(self, server, nick, password, channels):
        self.server = server
        self.nick = nick
        self.password = password
        self.channels = channels
        # Creates socket object as attribute of bot
        self.irc_socket = None

    # connect_to_server - Connects the bot to the given server
    def connect_to_server(self):
        # Initializes our socket object to be ready for connection
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Sockets connects to bot.server via PORT
        self.irc_socket.connect((self.server, self.PORT))
        # Issues commands to network identifying bot as bot.nick
        self.sock_send('USER ' + self.nick + ' ' + self.nick + ' ' + self.nick + ' : ')
        self.sock_send('NICK ' + self.nick)
        # While connected
        while 1:
            # Recieve irc protocol messages in 512 byte increments
            msg = self.irc_socket.recv(512)
            # Strip unnecessary new lines
            msg = msg.strip('\n\r')
            # Direct message to message handle_stream
            self.handle_message(msg)

    # handle_message - Reads incoming messages and checks for Pings, Identity requests, and bot commands
    #   Params:
    #      msg - type: string, the message to read
    def handle_message(self, msg):
        if 'PING :' in msg:
            self.pong()
        elif 'NickServ IDENTIFY' in msg:
            self.identify()
        elif ':Password accepted' in msg:
            self.join_channels()
        elif ':$' in msg:
            cmd_info = self.parse_command(msg)
            self.dir_to_func(cmd_info)
        print msg

    # handle_message -
    #   Params:
    #      msg - type: string, the command to parse
    #   Returns:
    #      parsed_command type: dictionary, the object containting command attributes
    def parse_command(self, msg):
        # Parses the message to find the command issuing user, channel, and command name
        query = msg.split(':$')[1]
        user = msg.split(':')[1].split('!')[0]
        channel = msg.split('PRIVMSG')[1].split(':')[0].strip()
        command = query.split(' ')[0]
        # Checks for arguments following bot command, places them to args. If there are none, set args to False
        if ' ' in query:
            args = query.split(' ', 1)[1].strip('\n\t')
        else:
            args = False
        # Dictionary constructed and returned
        parsed_command = {
            'user': user,
            'channel': channel,
            'command': command,
            'args': args
        }
        return parsed_command

    # sock_send - Issues message commands to IRC protocol
    # Params:
    #   msg - type: string, the message to send
    def sock_send(self, msg):
        self.irc_socket.send(str(msg) + '\n')

    # pong - Responds to pings sent by IRC protocol with PONG
    def pong(self):
        self.sock_send('PONG :pingis')

    # identify - Issues the identify user command with the bot password
    def identify(self):
        self.sock_send('PRIVMSG NickServ :IDENTIFY ' + self.password)

    # join_channels - Joins the channels passed in the constructor
    def join_channels(self):
        # If channels were passed
        if self.channels:
            for chan in self.channels:
                channel = chan[0]
                key = chan[1]
                # If there is a key, send join command with key, else, just the channel
                if key:
                    self.sock_send('JOIN ' + channel + ' ' + key)
                else:
                    self.sock_send('JOIN ' + channel)

    # send_chan_msg - Sends message out to channel via socket
    #   params:
    #      chan - type: string, the #channel to send the message out to
    #      msg - type: string, the message to send out to the channel
    def send_chan_msg(self, chan, msg):
        self.sock_send('PRIVMSG ' + chan + ' :' + str(msg))

    # send_priv_msg - Sends a private message to a given user via socket
    #    params:
    #      user - type: string, the user to send the private message to
    #      msg - type: string, the message to send
    def send_priv_msg(self, user, msg):
        self.sock_send('PRIVMSG ' + user + ' :' + msg)

    # dir_to_func
    #    params:
    #       cmd_info - type: dictionary, the dictionary containing command info for the bot functions
    #                   [user, channel, command, args]
    def dir_to_func(self, cmd_info):
        command = cmd_info['command']
        # Looks for keywords and sends command info to respective function
        if command == 'time':
            get_time(self, cmd_info)
        elif command == 'hello':
            say_hello(self, cmd_info)
        else:
            # If no such command exists, send message to channel
            self.send_chan_msg(cmd_info['channel'], "Command $" + command + " does not exist.")
