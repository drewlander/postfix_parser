from parser import MailParser, MailObject
from datetime import datetime
from collections import Counter
import time
import argparse


class PostfixAmavisStats(object):
    def __init__(self, num_results, maillog):
        # number of results to return
        self.num_results = num_results
        # location of maillog to parse
        self.maillog = maillog
        self.mailevents = self.get_mail_events(maillog)

    def get_authentication_stats(self):
        success_auths = [ x for x in self.mailevents if x.logtype == "successful_authentication"]
        failed_auths = [ x for x in self.mailevents if x.logtype == "failed_authentication"]
        most_common_success_auths = self.get_most_common_item([x.sasl_username for x in success_auths])
        most_common_failed_auths = self.get_most_common_item([x.sending_ip for x in failed_auths])
        print "Most common successful authentications for users: %s" % most_common_success_auths
        print "Most common failed authentications for ip: %s" % most_common_failed_auths

    def get_spam_stats(self):
        #mailevents = self.get_mail_events(self.maillog)
        spams = [x for x in self.mailevents if hasattr(x, 'mail_type') and x.mail_type == 'SPAM']
        spams= sorted(spams, key=lambda x: datetime.strptime(x.timestamp, '%b %d %H:%M:%S'))
        year = datetime.now().year
        first = datetime.strptime(spams[0].timestamp, '%b %d %H:%M:%S').replace(year=year)
        last =  datetime.strptime(spams[len(spams)-1].timestamp, '%b %d %H:%M:%S').replace(year=year)
        elapsed = last-first
        elapsed_seconds =  elapsed.seconds
        elapsed_minutes = elapsed.seconds/60
        elapsed_hours =  elapsed.seconds/3600
        print "In %s hours we marked %i messages as spam" % (elapsed_hours, len(spams))
        most_common_mailfrom = self.get_most_common_item([x.mailfrom for x in spams])
        most_common_rcptto = self.get_most_common_item([x.rcptto for x in spams])
        most_common_sending_ip = self.get_most_common_item([x.sending_ip for x in spams])
        print "Most common sending email address being marked as spam: %s" % most_common_mailfrom
        print "Most common email address received mail marked as spam: %s" % most_common_rcptto
        print "Most common ip address sending email marked as spam: %s" % most_common_sending_ip
    
    def get_most_common_item(self, items):
        data = Counter(items)
        return data.most_common(self.num_results)
    
    def get_mail_events(self, logfile):
        mailevents = []
        p = MailParser()
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
    parser.add_argument('-n', '--num_results', dest='num_results',
                         default=1, type=int,
                         help='number of results to show')
    parser.add_argument('-a', '--authentication_overview',
                         dest='authentication_overview',
                         action='store_true',
                         default=False,
                         help="Overview of authentication stats")
    args = parser.parse_args()
    return parser, args

def main():
    parser, args = parse_args()
    num_results = args.num_results
    if args.spam_overview:
        s = PostfixAmavisStats(args.num_results, args.logfile)
        #mailevents = get_mail_events(args.logfile)
        s.get_spam_stats()
    if args.authentication_overview:
        s = PostfixAmavisStats(args.num_results, args.logfile)
        s.get_authentication_stats()
    #else:
    #    parser.print_help()




if __name__ == '__main__':
    main()
