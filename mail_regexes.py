import re

sending_ip_re = re.compile(
    "\w+\s+\d+\s[0-9:]+\s[\w\.].+ postfix\/smtpd\[\d+\]: (\S+): "
    "client=\S+\[(\S+)\]")
subject_and_from_re = re.compile(
    "\w+\s+\d+\s[0-9:]+\s[\w\.].+ postfix\/cleanup\[\d+\]: (\S+): "
    "warning: header Subject: (.+) from .+ from=<(\S+)> to=<(\S+)>")

destination_and_from_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s([\w\.]+) "
                                  "postfix\/\S+\[\d+\]: (\S+): to=<(\S+)>.+ "
                                  "relay=(\S+),.+ status=(\S+) \((.+)\)")
queue_removed_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                                 "postfix\/qmgr\[\d+\]: (\S+): removed$")
messaged_id_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                               "postfix\/cleanup\[\d+\]: (\S+): "
                               "message-id=<(\S+)>")
get_from_re = re.compile("\w+\s+\d+\s[0-9:]+\s[\w\.].+ "
                         "postfix\/qmgr\[\d+\]: "
                         "(\S+): from=<(\S+)>, size=(\d+)")
rejected_sender_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s([\w\.]+) "
                                        "postfix\/smtpd\[\d+\]: NOQUEUE: "
                                        "reject: RCPT from \S+\[(\S+)\]: "
                                        "(\d\d\d \d\.\d\.\d .+ from=<(\S+)> "
                                        "to=<(\S+)> .+)")

auth_sender_re = re.compile("\w+\s+\d+\s[0-9:].+\s[\w\.]+ "
                                "postfix\/cleanup\[\d+\]: (\S+): "
                                ".+\(Authenticated sender: (\S+)\)\?\?")

amavis_spam_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ "
                                "amavis\[\d+\]: \(\S+\) (\S+) (\S+) "
                                "{(\w+),(\w+)}, \[\S+\].*\[(\S+)\] "
                                "<(\S+)> -> <(\S+)>, .+ Message-ID: "
                                "<(\S+)>, .+, Hits: (\S+), size: (\S+), "
                                "queued_as: (\S+), ")

successful_sasl_re = re.compile("(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ "
                                         "postfix\/smtpd\[\d+\]: (\S+): "
                                         "client=(\S+)\[(\S+)\], "
                                         "sasl_method=(\S+), "
                                         "sasl_username=(\S+)")

failed_sasl_re = re.compile(
    "(\w+\s+\d+\s[0-9:].+)\s[\w\.]+ postfix\/smtpd\[\d+\]: "
    "(\S+): (\S+)\[(\S+)\]: SASL (.+): (.+)")

relay_ip_re = re.compile("\S+\[(\S+)\]")
