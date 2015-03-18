from parser import MailParser, MailObject
from datetime import datetime
from collections import Counter
import time
import argparse

p = MailParser()
mailevents = []

def get_spam_emails(mailevents):
    spams = [x for x in mailevents if hasattr(x, 'mail_type') and x.mail_type == 'SPAM']
    spams= sorted(spams, key=lambda x: datetime.strptime(x.timestamp, '%b %d %H:%M:%S'))
    year = datetime.now().year
    first = datetime.strptime(spams[0].timestamp, '%b %d %H:%M:%S').replace(year=year)
    last =  datetime.strptime(spams[len(spams)-1].timestamp, '%b %d %H:%M:%S').replace(year=year)
    elapsed = last-first
    elapsed_seconds =  elapsed.seconds
    elapsed_minutes = elapsed.seconds/60
    elapsed_hours =  elapsed.seconds/3600
    #emails = sorted(spams, key=lambda x: x.mailfrom)
    print "In %s hours we marked %i messages as spam" % (elapsed_hours, len(spams))
    most_common_mailfrom = get_most_common_item([x.mailfrom for x in spams])
    most_common_rcptto = get_most_common_item([x.rcptto for x in spams])
    most_common_sending_ip = get_most_common_item([x.sending_ip for x in spams])
    print "Most common sending email address being marked as spam: %s" % most_common_mailfrom
    print "Most common email address received mail marked as spam: %s" % most_common_rcptto
    print "Most common ip address sending email marked as spam: %s" % most_common_sending_ip

def get_most_common_item(items):
    data = Counter(items)
    return data.most_common(1)

def get_args(args):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                       help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                       const=sum, default=max,
                       help='sum the integers (default: find the max)')
    return parser

def get_mail_events(logfile):
    with open(logfile) as f:
        for line in f:
            o =  p.parse(line)
            if o:
                mailevents.append(o)
        return mailevents
    

def parse_args():
    parser = parser = argparse.ArgumentParser(description = "Get some stats!")
    parser.add_argument('-s', '--spam_overview',
                      action='store_true',
                      default=False,
                      dest='spam_overview',
                      help='Generic overview of spam stats')
    parser.add_argument('-f', '--logfile', dest='logfile',
                         default='/var/log/maillog')
    args = parser.parse_args()
    return parser, args

def main():
    parser, args = parse_args()
    if args.spam_overview:
        mailevents = get_mail_events(args.logfile)
        get_spam_emails(mailevents)
    else:
        parser.print_help()




if __name__ == '__main__':
    main()
