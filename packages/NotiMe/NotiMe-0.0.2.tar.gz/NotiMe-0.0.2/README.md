# NotiMe
This program send a notify to user through many channels.

## Prerequisites
### Line
You have to generate access token from Line Notify Bot website https://notify-bot.line.me

### Write
Only support linux 'write' command, might not work with WSL.

## Installation
pip install NotiMe

## Configuration
edit .notime.rc in your home directory, see notime.rc.example for guideline.

## Usage
### CLI
    $ execution_something_that_need_a_long_time_to_finish.sh && notime -l "That very long execution is done."

### Python package
    from NotiMe import send_write_notify
    from NotiMe import send_line_notify

    send_write_notify('Done')                   # send notify through write command to local user
    send_line_notify('Done', LINE_API_TOKEN)    # send notify through Line API using LINE_API_TOKEN (see Prerequisites)

## References
- [LINE Notify API Document](https://notify-bot.line.me/doc/)
