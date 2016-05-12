# Author: Ryan Lanese
# title: parse.py

class ParseIrcMsg(object):

    # Constants
    BOT_COMMAND_TOKEN = ':$'

    # is_ping - Checks if irc msg is a ping request
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_ping(self, msg):
        source = msg.split(' ')[0]
        if source == 'PING':
            return True
        else:
            return False

    # get_msg_type - Returns the type of IRC message
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      msg_type - type: string, type of irc message
    def get_msg_type(self, msg):
        s_s = msg.split(' ')
        if len(s_s) > 1:
            msg_type = s_s[1]
        else:
            msg_type = ''
        return msg_type

    # is_bot_command - Checks if irc msg is a bot command
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_bot_command(self, msg):
        if self.BOT_COMMAND_TOKEN in msg:
            return True
        else:
            return False

    # is_call_for_identity - Checks if irc msg is requesting password identification
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_call_for_identity(self, msg):
        if 'NickServ IDENTIFY' in msg:
            return True
        else:
            return False

    # is_pass_accepted - Checks if irc msg is notifying the bot user of a successful password identification
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_pass_accepted(self, msg):
        if 'Password accepted' in msg:
            return True
        else:
            return False
            
    # is_user_list - Checks if irc msg is a list of channel users
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_user_list(self, msg):
        s_s = msg.split(' ')
        if len(s_s) >= 4 and '=' in s_s:
            return True
        else:
            return False

    # get_user_list_and_chan - Fetches the channel for a given user list and the unparsed userlist
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      ch_usr type: dictionary, dictionary containing a channel and user list
    def get_user_list_and_chan(self, msg):
        s_s = msg.split(' ')
        channel = s_s[4]
        user_list = msg.split(':')[2]
        ch_usr = {
            'channel': channel,
            'user_list': user_list,
        }
        return ch_usr

    # parse_bot_command -
    #   Params:
    #      msg - type: string, the command to parse
    #   Returns:
    #      parsed_command type: dictionary, dictionary containing command attributes
    def parse_bot_command(self, msg):
        # Parses the message to find the command issuing user, channel, and command name
        query = msg.split(self.BOT_COMMAND_TOKEN)[1]
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
