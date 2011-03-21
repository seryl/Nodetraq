import urllib
import urllib2
import json
from lxml import etree
from lxml.html.soupparser import fromstring

class NagiosReader(object):
    username = 'nagios_username'
    password = 'nagios_password'

    def get_nagios_page(self, nagiosurl):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, nagiosurl, self.username, self.password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
        pagehandle = urllib2.urlopen(nagiosurl)

        data = pagehandle.read()
        root = fromstring(data)
        return root

    def parse_downtimes(self):
        nagiosurl = 'https://nagios1.yourdomain/nagios/cgi-bin/extinfo.cgi?type=6'
        base_xpath = '//tr[@class="downtimeEven"]'

        col_mapping = [
            'Host Name', 'Entry Time',
            'Author', 'Comment',
            'Start Time', 'End Time',
            'Type', 'Duration',
            'Downtime ID', 'Trigger ID'
            ]

        # Iterate through the unlabeled rows
        root = self.get_nagios_page(nagiosurl)
        total_rows = len(root.xpath(base_xpath))
        downtime_list = []
        for i in xrange(total_rows):
            downtime = {}
            for current, col in enumerate(
                    root.xpath(base_xpath)[i].getchildren()):
                if current == 0:
                    col = col.getchildren()[0]
                elif current == len(col_mapping):
                    break
                downtime[col_mapping[current]] = col.text

            downtime_list.append(downtime)
        return downtime_list

