# Author: Ryan Lanese
import socket
import time
from channel_ops import *
from parse import *

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
        # Creates an empty irc parser object
        self.parse = None
        # Creates socket object as attribute of bot
        self.irc_socket = None
        # Intializes channel ops objects to an empty list
        self.channel_ops = []

    # connect_to_server - Connects the bot to the given server
    def connect_to_server(self):
        # Initializes our socket object to be ready for connection
        self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Sockets connects to bot.server via PORT
        self.irc_socket.connect((self.server, self.PORT))
        # Issues commands to network identifying bot as bot.nick
        self.sock_send('USER ' + self.nick + ' ' + self.nick + ' ' + self.nick + ' : ')
        self.sock_send('NICK ' + self.nick)
        # Parser object is created
        self.parser = ParseIrcMsg()
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
        # Output raw message to terminal
        print msg
        # Check if incoming message is ping
        if self.parser.is_ping(msg):
            self.pong()
        # Check if incoming message requests password identity
        elif self.parser.is_call_for_identity(msg):
            self.identify()
        # Check if incoming message notifies us of password acceptance
        elif self.parser.is_pass_accepted(msg):
            self.join_channels()
        # Check for a channel join message. Check for an edge case that the user provides
        # a valid channel with an invalid case.
        elif self.parser.get_msg_type(msg) == 'JOIN':
            true_chan_case = msg.split('JOIN')[1].strip(' :')
            for channel in self.channels:
                # Sets channel passed in bot construction to the appropriate case
                if channel[0].lower() == true_chan_case.lower():
                    channel[0] = true_chan_case
                # Add channel operations object for channel
                self.channel_ops.append(ChannelOps(self, channel[0]))
        # Check for user list spit out upon channel join. Directs it to the appropriate channel op object
        elif self.parser.is_user_list(msg):
            usr_chan_dict = self.parser.get_user_list_and_chan(msg)
            channel_op = self.get_channel_op_by_chan(usr_chan_dict['channel'])
            channel_op.set_users(usr_chan_dict['user_list'])
        # Check if incoming message is a user issued bot command
        elif self.parser.is_bot_command(msg):
            # Parse command
            cmd_info = self.parser.parse_bot_command(msg)
            # Get the channel op object we are working with
            channel_op = self.get_channel_op_by_chan(cmd_info['channel'])
            # Leave object to handle command
            channel_op.handle_command(cmd_info)

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

    # get_channel_op_by_chan - Returns the channel operations object given a channel
    #   params:
    #      chan - type: string, the channel associated with the channel operations object
    #   return:
    #      channel_op - type: object, the corresponding chanel operations object
    def get_channel_op_by_chan(self, chan):
        for channel_op in self.channel_ops:
            if channel_op.channel == chan:
                return channel_op
