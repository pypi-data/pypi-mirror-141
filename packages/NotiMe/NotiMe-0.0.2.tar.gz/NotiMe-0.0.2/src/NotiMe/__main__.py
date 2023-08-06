# Copyright (c) 2022 Pruet Boonma <pruetboonma@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import argparse
import configparser
from sys import platform
from NotiMe import send_line_notify
from NotiMe import send_write_notify

LOCAL_RC_FILE_NAME = '.notime.rc'
GLOBAL_RC_FILE_PATH = '/etc/notime.rc'

def main():
	try:
		# Arguement parser
		parser = argparse.ArgumentParser(description='Parse arguments.....')
		parser.add_argument('message', help='Notification message')
		parser.add_argument('-c', '--configuration', help='Load configuration file')
		parser.add_argument('-l', '--line', action='store_true', help='Send Line notification')
		parser.add_argument('-w', '--write', action='store_true', help='Write to terminal of this user (Unix only)')
		args = parser.parse_args()

		# Configuration parser
		config = configparser.ConfigParser()
		## Try to read from command line argument first
		if args.configuration:
			config_result = config.read(args.configuration)
		else:
			## Second, local local rc file
			local_rc_file = os.path.join(os.path.expanduser('~'), LOCAL_RC_FILE_NAME)
			if os.path.exists(local_rc_file):
				config_result = config.read(local_rc_file)
			else:
				## Third, load global rc file, only support linux now
				if platform == 'linux' or platform == 'linux2':
					if os.path.exists(GLOBAL_RC_FILE_PATH):
						config_result = config.read(GLOBAL_RC_FILE_PATH)

		if not config_result:
			raise ValueError('Can\'t find configuration file');
		sent = False

		# Send write notify
		if config.get('WRITE', 'SendByDefault', vars=None) == 'True' or args.write == True:
			if platform == 'linux' or platform == 'linux2':
				send_write_notify(args.message)
				sent = True	

		# Send line notify
		if config.get('LINE', 'SendByDefault', vars=None) == 'True' or args.line == True:
			line_api_token = config.get('LINE', 'AccessToken', vars=None)
			send_line_notify(args.message, line_api_token)
			sent = True

		if not sent:
			print('Error: No notification channel specified.')	

	except Exception as ex:
		print('Error: ' + str(ex))

if __name__=='__main__':
	sys.exit(main())