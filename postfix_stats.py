from parser import MailParser, MailObject
from datetime import datetime
import time
import argparse

p = MailParser()
mailevents = []

def get_spam_emails():
    spams = [x for x in mailevents if hasattr(x, 'mail_type') and x.mail_type == 'SPAM']
    spams= sorted(spams, key=lambda x: datetime.strptime(x.timestamp, '%b %d %H:%M:%S'))
    year = datetime.now().year
    first = datetime.strptime(spams[0].timestamp, '%b %d %H:%M:%S').replace(year=year)
    last =  datetime.strptime(spams[len(spams)-1].timestamp, '%b %d %H:%M:%S').replace(year=year)
    elapsed = last-first
    elapsed_seconds =  elapsed.seconds
    elapsed_minutes = elapsed.seconds/60
    elapsed_hours =  elapsed.seconds/3600
    print "%s %s %s" %(elapsed_seconds, elapsed_minutes, elapsed_hours)
    print "In %s hours we marked %i messages as spam" % (elapsed_hours, len(spams))


def get_args(args):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                       help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum, default=max,
                       help='sum the integers (default: find the max)')
    return parser

with open("maillog") as f:
    for line in f:
        o =  p.parse(line)
        if o:
            mailevents.append(o)




def parse_args():
    parser = parser = argparse.ArgumentParser(description = "Get some stats!")
    parser.add_argument('-s', '--spam_overview',
                      action='store_true',
                      default=False,
                      dest='spam_overview',
                      help='Generic overview of spam stats')
    args = parser.parse_args()
    return parser, args

def main():
    parser, args = parse_args()
    if args.spam_overview:
        get_spam_emails()
    else:
        parser.print_help()




if __name__ == '__main__':
    main()
