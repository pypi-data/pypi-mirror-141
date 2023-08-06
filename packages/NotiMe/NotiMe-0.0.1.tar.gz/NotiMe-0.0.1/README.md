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
edit .notime in your home directory, see notime.rc.example for guideline.

## Usage
$ execution_something_that_need_a_long_time_to_finish.sh && notime -l "That very long execution is done."

## References
- [LINE Notify API Document](https://notify-bot.line.me/doc/)