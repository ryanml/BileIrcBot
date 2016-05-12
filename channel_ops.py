# Author: Ryan Lanese

import time
import json
import requests
import random

# get_time - Gets and formats the current time and sends it out to channel
#    params:
#       cmd_info - type: dictionary, the dictionary containing command info
def get_time(bot, cmd_info):
    current_time = time.strftime('%H:%M:%S [%Z]')
    bot.send_chan_msg(cmd_info['channel'], 'The current time is: \x02' + current_time + '\x02')

# say_hello - Responds with a message to the user issuing the command
#    params:
#       cmd_info - type: dictionary, the dictionary containing command info
def say_hello(bot, cmd_info):
    bot.send_priv_msg(cmd_info['user'], 'Hello there, ' + cmd_info['user'] + '!')
