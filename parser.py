from datetime import datetime, timedelta
import sys
import time
import re
import argparse

argparser = argparse.ArgumentParser()
argparser.add_argument('--i')
argparser.add_argument('--o')
argparser.add_argument('--h')
argparser.add_argument('--m')
argparser.add_argument('--s')
argparser.add_argument('--ms')

INSTRUCTIONS = """\nInsufficient arguments. The accepted flags are:
  \n\t--i\t[input filename]\
  \n\t--o\t[output filename]\
  \n\t--h\t[hours]\
  \n\t--m\t[minutes]\
  \n\t--s\t[seconds]\
  \n\t--ms\t[milliseconds]\
  \n\n For example: 'parser.py --i=subs.srt --o=fixed.srt --s=-3 --ms=200'
  """

def replacer(match, delta):  
  match = match.group()
  time, milliseconds = match.split(",")
  time = "{}.{}".format(time, int(milliseconds) * 1000)
  initial_datetime = datetime.strptime(time, "%H:%M:%S.%f")
  delayed_datetime = initial_datetime + delta
  as_time, milliseconds = delayed_datetime.strftime("%H:%M:%S.%f").split(".")
  milliseconds = milliseconds[:-3]
  time_formatted = "{},{}".format(as_time, milliseconds)
  return time_formatted

def parser(input_file, output_file, delta):
  p = re.compile('[01][0-9]:[0-9]{2}:[0-9]{2},[0-9]{3}')
  lines = ""
  with open(input_file, "r") as data:
    lines = "".join(data.readlines())
    lines = re.sub(p, lambda x: replacer(x, delta), lines)
  with open(output_file, "w") as data:
    data.write(lines)
    print("[SUCCESS] Subtitle saved at {}".format(output_file))

def to_delta(hours=0, minutes=0, seconds=0, milliseconds=0):
  hours = int(hours)
  minutes = int(minutes)
  seconds = int(seconds)
  microseconds = int("{}000".format(milliseconds))
  return timedelta(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)


if __name__ == "__main__":
  args = argparser.parse_args()

  if (args.h or args.m or args.s or args.ms) and args.i:
    hours = args.h if args.h else 0
    minutes = args.m if args.m else 0
    seconds = args.s if args.s else 0
    milliseconds = args.ms if args.ms else 0
    input_file = args.i   
    output_file = args.o if args.o else "fixed-{}".format(input_file)
    delta = to_delta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    parser(input_file, output_file, delta)

  else:
    print(INSTRUCTIONS)