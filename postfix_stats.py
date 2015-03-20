#!/usr/bin/env python
from parser import MailParser, MailObject
from datetime import datetime
from platform import python_version
version = python_version()[:3]
if version == '2.6':
    print "Importing backported Counter"
    from fakecollections import Counter
else:
    from collections import Counter
import time
import argparse
#from argparse import subparsers


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

    def get_elapsed_time_for_address(self, address):
        emails = sorted(self.mailevents, key=lambda x: datetime.strptime(x.timestamp, '%b %d %H:%M:%S'))
        if not emails:
            return []
        year = datetime.now().year
        first = datetime.strptime(emails[0].timestamp, '%b %d %H:%M:%S').replace(year=year)
        last =  datetime.strptime(emails[len(self.mailevents)-1].timestamp, '%b %d %H:%M:%S').replace(year=year)
        elapsed = last-first
        elapsed_seconds =  elapsed.seconds
        elapsed_minutes = elapsed.seconds/60
        elapsed_hours =  elapsed.seconds/3600
        return {"hours":elapsed_hours, "minutes": elapsed_minutes, 
                "seconds": elapsed_seconds}

    def get_spam_stats(self):
        #mailevents = self.get_mail_events(self.maillog)
        spams = [x for x in self.mailevents if hasattr(x, 'mail_type') and x.mail_type == 'SPAM']
        spams= sorted(spams, key=lambda x: datetime.strptime(x.timestamp, '%b %d %H:%M:%S'))
        if not spams:
            return []
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

  
    def find_emails_for_address(self, address):
        print "Finding emails for %s" % address
        sent_to = [x for x in self.mailevents if hasattr(x, 'to') and address in x.to]
        mail_from = [x for x in self.mailevents if hasattr(x, 'mailfrom') and address in x.mailfrom]
        for email in sent_to:
            print email.__dict__

    def find_email_by_messageid(self, messageid):
        print "Finding email with %s message ID" % messageid
        email = [x for x in self.mailevents if hasattr(x, 'to') and messageid in x.message_id]
        print mail_from.__dict__

    def find_emails_by_recipients(self, rcptto, mailfrom):
        print mailfrom
        print rcptto
        emails = [x for x in self.mailevents if hasattr(x, 'to') and hasattr(x, 'mailfrom')  
                  and mailfrom in x.mailfrom and rcptto in x.to]

        for email in emails:
            print email.__dict__

    def get_emails_stats(self):
        emails = [x for x in self.mailevents if x.logtype == "mail"]
        most_common_receipients = self.get_most_common_item([x.to for x in emails])
        most_common_senders = self.get_most_common_item([x.mailfrom for x in emails if hasattr(x, 'mailfrom')])
        elapsed_time = self.get_elapsed_time_for_address(most_common_senders)
        print "In %s hours, or %s minutes:" % (elapsed_time["hours"], elapsed_time["minutes"])
        print "Most common email address sent to: %s" % most_common_receipients
        print "Most common email address sent from: %s" % most_common_senders


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
    parser.add_argument('-l', '--logfile', dest='logfile',
                         default='/var/log/maillog')
    parser.add_argument('-n', '--num_results', dest='num_results',
                         default=1, type=int,
                         help='number of results to show')
    parser.add_argument('-o', '--mailoverview',
                        action='store_true',
                        dest='mail_overview',
                        help='overview of senders and receivers')
    parser.add_argument('-f', '--find', dest='find',
                        action='store_true',
                        help="Find emails for address")

    parser.add_argument('-e', '--emailaddress', action='append',
                        dest='email_addresses', help='email address')
    
    parser.add_argument('--rcptto', action='store',
                        dest='recip_email_address', help='recipient email address')

    parser.add_argument('--mailfrom', action='store',
                        dest='to_email_address', help='recipient email address')

    subparsers = parser.add_subparsers(help='spam stats help', dest="submodule")
    parser_spam_stats = subparsers.add_parser('spam', help='spam stats help')
    parser_spam_stats.add_argument('-l', '--logfile', dest="logfile", help='location of log file')
    parser_spam_stats.add_argument('-n', '--num_results', dest="num_results", 
                                    default=1, type=int, help='location of log file')

    #subparsers = parser.add_subparsers(help='Authentication stats', dest="get_auth_stats")
    parser_auth_stats = subparsers.add_parser('auth', help='authentication stats')
    parser_auth_stats.add_argument('-l', '--logfile', dest="logfile", help='location of log file')
    parser_auth_stats.add_argument('-n', '--num_results', dest="num_results", 
                                    default=1, type=int, help='location of log file')

    parser_mail_stats = subparsers.add_parser('mail', help="mail stats")
    parser_mail_stats.add_argument('-l', '--logfile', dest="logfile", help='location of log file')
    parser_mail_stats.add_argument('-n', '--num_results', dest="num_results", 
                                    default=1, type=int, help='location of log file')


    parser_mail_search = subparsers.add_parser('search', help="search for email")
    parser_mail_search.add_argument('-l', '--logfile', dest="logfile", help='location of log file')
    parser_mail_search.add_argument('-f', '--from', dest="mailfrom", help='email address sent from')
    parser_mail_search.add_argument('-t', '--to', dest="to", help='email address sent to')
    parser_mail_search.add_argument('-e', '--emailaddress', dest="emailaddress", help='email address')
    parser_mail_search.add_argument('-n', '--num_results', dest="num_results", 
                                    default=1, type=int, help='location of log file')



    args = parser.parse_args()

    return parser, args

def main():
    parser, args = parse_args()
    num_results = args.num_results 
    if args.submodule:
        if args.submodule == 'spam':
            s = PostfixAmavisStats(args.num_results, args.logfile)
            s.get_spam_stats()
        if args.submodule == 'auth':
            s = PostfixAmavisStats(args.num_results, args.logfile)
            s.get_authentication_stats()
        if args.submodule == 'mail':
            s = PostfixAmavisStats(args.num_results, args.logfile)
            s.get_emails_stats()
        if args.submodule == 'search':
            s = PostfixAmavisStats(args.num_results, args.logfile)
            if args.emailaddress:
                    s.find_emails_for_address(emailaddress)
            elif args.mailfrom and args.to:
                s.find_emails_by_recipients(args.to, args.mailfrom)

    #else:
    #    parser.print_help()




if __name__ == '__main__':
    main()
