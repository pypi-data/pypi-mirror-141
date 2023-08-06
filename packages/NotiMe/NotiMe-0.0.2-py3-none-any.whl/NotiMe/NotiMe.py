"""
A simple notification program
"""

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

import getpass
import requests
import subprocess


LINE_NOTIFY_BOT_API_URL = 'https://notify-api.line.me/api/notify'

def send_write_notify(message):
	current_user = getpass.getuser()
	cmd1 = ['echo', '"' + message +'"']
	cmd2 = ['write', current_user]
	p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
	p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	p2.stdout.close()

def send_line_notify(message, line_api_token):
	if not line_api_token:
		raise ValueError('Missing Line Notify Access Token')
	if not message:
		raise ValueError('Missing Line Notify messages')
	headers = {'Authorization' : 'Bearer ' + line_api_token}
	params = {'message' : '[NotiMe] {0}'.format(message)}
	return requests.post(LINE_NOTIFY_BOT_API_URL, headers = headers, params = params, files= {})
