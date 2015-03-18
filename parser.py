#!/bin/env python
import re

get_originating_ip_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                                   "postfix\/smtpd\[\d+\]: (\S+): "
                                   "client=\S+\[(\S+)\]")
get_subject_and_addrs_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                                      "postfix\/cleanup\[\d+\]: (\S+): "
                                      "warning: header Subject: (.+) "
                                      "from .+ from=<(\S+)> to=<(\S+)>")
get_relay_and_dsn_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s([\w\.]+) "
                                  "postfix\/\S+\[\d+\]: (\S+): to=<(\S+)>.+ "
                                  "relay=(\S+),.+ status=(\S+) \((.+)\)")
queue_id_removed_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                                 "postfix\/qmgr\[\d+\]: (\S+): removed$")
get_message_id_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                              "postfix\/cleanup\[\d+\]: (\S+): "
                              "message-id=<(\S+)>")
get_from_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ postfix\/qmgr\[\d+\]: "
                         "(\S+): from=<(\S+)>, size=(\d+)")
sender_address_rejected_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s([\w\.]+) "
                                        "postfix\/smtpd\[\d+\]: NOQUEUE: "
                                        "reject: RCPT from \S+\[(\S+)\]: "
                                        "(\d\d\d \d\.\d\.\d .+ from=<(\S+)> "
                                        "to=<(\S+)> .+)")
relay_ip_re = re.compile("\S+\[(\S+)\]")

get_auth_sender_re = re.compile("\w+\s+\d+\s[0-9:].+\s[\w\.]+ "
                                "postfix\/cleanup\[\d+\]: (\S+): "
                                ".+\(Authenticated sender: (\S+)\)\?\?")

get_amavis_spam_re = re.compile("\w+\s+\d+\s[0-9:].+\s[\w\.]+ amavis\[\d+\]: "
                                "\(\S+\) (\S+) (\S+) {(\w+),(\w+)}, "
                                "\[\S+\]:\d+ \[(\S+)\] <(\S+)> -> <(\S+)>, "
                                ".+ Message-ID: <(\S+)>, .+, Hits: (\S+), "
                                "size: (\S+), queued_as: (\S+), ")
get_amavis_spam_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ amavis\[\d+\]: \(\S+\) (\S+) (\S+) {(\w+),(\w+)}, \[\S+\]:\d+ \[(\S+)\] <(\S+)> -> <(\S+)>, .+ Message-ID: <(\S+)>, .+, Hits: (\S+), size: (\S+), queued_as: (\S+), ")



class MailObject (object):
    def __init__(self, localID):
        self.localID = localID


class MailParser(object):
    def __init__(self):
        self.mobjects = []

    def get_relay_info(self, relay):
        m = relay_ip_re.match(relay)
        if m:
            return m.group(1)
        else:
            return relay

    def find_local_id(self, localID):
        o = [o for o in self.mobjects if o.localID == localID]
        if len(o) == 0:
            o = MailObject(localID)
            self.mobjects.append(o)
            return o
        return o[0]

    def get_auth_sender(self, line):
        m = get_auth_sender_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.userID = m.group(2)

    def get_client_info(self, line):
        m = get_originating_ip_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.sending_ip = m.group(2)

    def get_subject(self, line):
        m = get_subject_and_addrs_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.subject = m.group(2)
            o.mailfrom = m.group(3)

    def get_dsn(self, line):
        m = get_relay_and_dsn_re.match(line)
        if m:
            o = self.find_local_id(m.group(3))
            o.destinationIP = self.get_relay_info(m.group(5))
            o.result = m.group(6)
            o.result_detail = m.group(7)
            o.to = m.group(4)
            o.timestamp = m.group(1)
            o.host = m.group(2)
            # relays have no virus or spam scannning
            o.spamResult = "No"
            o.virusResult = "No"
            return o
            #event = self.create_event(o.__dict__)
            # We copy the dict because python passes by reference.
            # So setting o.result again and calling the create_event
            # function would change the old result as well
            #received_event = o.__dict__.copy()
            #received_event["result"] = "received"
            #received_event = self.create_event(received_event)
            #return event + received_event

    def get_message_id(self, line):
        m = get_message_id_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.message_id = m.group(2)

    def get_from(self, line):
        m = get_from_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.mailfrom = m.group(2)
            o.size = m.group(3)

    def sender_addr_rejected(self, line):
        m = sender_address_rejected_re.match(line)
        if m:
            o = MailObject(None)
            o.sending_ip = m.group(3)
            o.result = "failed"
            o.mailfrom = m.group(5)
            o.to = m.group(6)
            o.result_detail = m.group(4)
            o.timestamp = m.group(1)
            o.host = m.group(2)
            return o
            #return self.create_event(o.__dict__)

    def get_removed(self, line):
        m = queue_id_removed_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            self.mobjects.remove(o)

    def get_amavis_spam(self, line):
        m = get_amavis_spam_re.match(line)
        if m:
            o = MailObject(m.group(12))
            o.timestamp = m.group(1)
            o.pass_fail = m.group(2)
            o.mail_type = m.group(3)
            o.tags = [m.group(4), m.group(5)]
            o.sending_ip = m.group(6)
            o.mailfrom = m.group(7)
            o.rcptto = m.group(8)
            o.message_id = m.group(9)
            o.spam_score = m.group(10)
            o.size = m.group(11)
            o.queued_as = m.group(12)
            return o

    def parse(self, line):
        for x in [self.get_client_info, self.get_subject,
                  self.get_dsn, self.get_from, self.get_message_id,
                  self.sender_addr_rejected, self.get_removed,
                  self.get_auth_sender, self.get_amavis_spam]:
            event = x(line)
            if event:
                return event
