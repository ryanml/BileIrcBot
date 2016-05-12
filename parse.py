# Author: Ryan Lanese
# title: parse.py

class ParseIrcMsg(object):

    # Constants
    BOT_COMMAND_TOKEN = ':$'

    # parse_msg -
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      parsed_msg type: dictionary, dictionary containing the irc message's source, type, and trailing info
    def parse_msg(self, msg):
        space_split = msg.split(' ')
        source = space_split[0].strip(':')
        if len(space_split) > 1:
            msg_type = space_split[1]
            msg_trail = msg.split(msg_type)[1]
        else:
            msg_type = ''
            msg_trail = ''
        parsed_msg = {
            'source': source,
            'type': msg_type,
            'trail': msg_trail
        }
        return parsed_msg

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

    # is_bot_command - Checks if irc msg is a bot command
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_bot_command(self, msg):
        parsed_msg = self.parse_msg(msg)
        if not parsed_msg['type'] == 'PRIVMSG':
            return False
        if not self.BOT_COMMAND_TOKEN in parsed_msg['trail']:
            return False
        else:
            return True

    # is_call_for_identity - Checks if irc msg is requesting password identification
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_call_for_identity(self, msg):
        parsed_msg = self.parse_msg(msg)
        if not parsed_msg['type'] == 'NOTICE':
            return False
        if not 'NickServ IDENTIFY' in parsed_msg['trail']:
            return False
        else:
            return True

    # is_pass_accepted - Checks if irc msg is notifying the bot user of a successful password identification
    #   Params:
    #      msg - type: string, irc message to parse
    #   Returns:
    #      bool type: boolean
    def is_pass_accepted(self, msg):
        parsed_msg = self.parse_msg(msg)
        if not parsed_msg['type'] == 'NOTICE':
            return False
        if not 'Password accepted' in parsed_msg['trail']:
            return False
        else:
            return True

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
