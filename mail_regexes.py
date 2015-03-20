import re

get_originating_ip_re = re.compile(
    "\w+\s+\d+\s[0-9:]+\s[\w\.].+ postfix\/smtpd\[\d+\]: (\S+): "
    "client=\S+\[(\S+)\]")
get_subject_and_addrs_re = re.compile(
    "\w+\s+\d+\s[0-9:]+\s[\w\.].+ postfix\/cleanup\[\d+\]: (\S+): "
    "warning: header Subject: (.+) from .+ from=<(\S+)> to=<(\S+)>")

get_relay_and_dsn_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s([\w\.]+) "
                                  "postfix\/\S+\[\d+\]: (\S+): to=<(\S+)>.+ "
                                  "relay=(\S+),.+ status=(\S+) \((.+)\)")
queue_id_removed_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                                 "postfix\/qmgr\[\d+\]: (\S+): removed$")
get_message_id_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                               "postfix\/cleanup\[\d+\]: (\S+): "
                               "message-id=<(\S+)>")
get_from_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                         "postfix\/qmgr\[\d+\]: "
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

get_amavis_spam_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ "
                                "amavis\[\d+\]: \(\S+\) (\S+) (\S+) "
                                "{(\w+),(\w+)}, \[\S+\].*\[(\S+)\] "
                                "<(\S+)> -> <(\S+)>, .+ Message-ID: "
                                "<(\S+)>, .+, Hits: (\S+), size: (\S+), "
                                "queued_as: (\S+), ")

get_successful_sasl_auth_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ "
                                         "postfix\/smtpd\[\d+\]: (\S+): "
                                         "client=(\S+)\[(\S+)\], "
                                         "sasl_method=(\S+), "
                                         "sasl_username=(\S+)")

get_failed_sasl_auth_re = re.compile(
    "(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ postfix\/smtpd\[\d+\]: "
    "(\S+): (\S+)\[(\S+)\]: SASL (.+): (.+)")
