#!/bin/env python
import re
from mail_regexes import *


class MailObject (object):
    def __init__(self, localID):
        self.localID = localID


class MailParser(object):
    def __init__(self):
        self.mobjects = []

    def dest_ip_info(self, relay):
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
        m = auth_sender_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.userID = m.group(2)

    def get_client_info(self, line):
        m = sending_ip_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.sending_ip = m.group(2)

    def get_subject(self, line):
        m = subject_and_from_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            o.subject = m.group(2)
            o.mailfrom = m.group(3)

    def get_dsn(self, line):
        m = destination_and_from_re.match(line)
        if m:
            o = self.find_local_id(m.group(3))
            o.destinationIP = self.dest_ip_info(m.group(5))
            o.result = m.group(6)
            o.result_detail = m.group(7)
            o.to = m.group(4)
            o.timestamp = m.group(1)
            o.host = m.group(2)
            # relays have no virus or spam scannning
            o.spamResult = "No"
            o.virusResult = "No"
            o.logtype = "mail"

            return o

    def get_message_id(self, line):
        m = messaged_id_re.match(line)
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
        m = rejected_sender_re.match(line)
        if m:
            o = MailObject(None)
            o.sending_ip = m.group(3)
            o.result = "failed"
            o.mailfrom = m.group(5)
            o.to = m.group(6)
            o.result_detail = m.group(4)
            o.timestamp = m.group(1)
            o.host = m.group(2)
            o.logtype = "mail"
            return o

    def get_removed(self, line):
        m = queue_removed_re.match(line)
        if m:
            o = self.find_local_id(m.group(1))
            self.mobjects.remove(o)

    def get_amavis_spam(self, line):
        m = amavis_spam_re.match(line)
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
            o.logtype = "amavis"
            return o

    def get_successful_sasl_auth(self, line):
        m = successful_sasl_re.match(line)
        if m:
            o = MailObject(m.group(2))
            o.timestamp = m.group(1)
            o.sending_ip = m.group(4)
            o.sasl_type = m.group(5)
            o.sasl_username = m.group(6)
            o.logtype = "successful_authentication"
            return o

    def get_failed_sasl_auth(self, line):
        m = failed_sasl_re.match(line)
        if m:
            o = MailObject(None)
            o.timestamp = m.group(1)
            o.sending_ip = m.group(4)
            o.message = m.group(5)
            o.detail = m.group(6)
            o.logtype = "failed_authentication"
            return o


    def parse(self, line):
        for x in [self.get_client_info, self.get_subject,
                  self.get_dsn, self.get_from, self.get_message_id,
                  self.sender_addr_rejected, self.get_removed,
                  self.get_auth_sender, self.get_amavis_spam,
                  self.get_successful_sasl_auth,
                  self.get_failed_sasl_auth]:
            event = x(line)
            if event:
                return event
