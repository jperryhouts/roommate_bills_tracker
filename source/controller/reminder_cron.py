#!/usr/bin/env python

"""
This file is part of Bill-Tracker.

Bill-Tracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Bill-Tracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Bill-Tracker.  If not, see <http://www.gnu.org/licenses/>.
"""

## Sends email reminders
import json, smtplib, sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from os.path import dirname, realpath

srcdir = realpath(dirname(realpath(__file__))+'/..')

sys.path.insert(0,srcdir+'/view')
import page_elements
from ledger import Ledger

if __name__ == '__main__':
    with open(srcdir+'/model/settings.json') as settingsfile:
        settings = json.load(settingsfile)

    with Ledger(srcdir+'/model/ledger.db', settings['roommate_names']) as ledger, \
            open(srcdir+'/view/style/styles.css','r') as cssfile:
        text = '''
Friendly monthly reminder that bills are still a thing.
You can view the current state of things at
%s
        '''%settings['URI']

        html = '''
<html>
  <head>
    <style>
      {css}
    </style>
  </head>
  <body>

    <div class="content">
      Friendly monthly reminder that bills are still a thing.<br/>
      You can view the current state of things at
      <a href="{uri}">{uri}</a>
    </div>
    <div class="content">
      <table>
        <caption>{totals_caption}</caption>
        <tr>
          <th class="date">Name</th>
          <th>Net paid (Paid - Recvd.)</th>
          <th>Owes ({bills_per_person} - Net paid)</th>
        </tr>

        {debts_table}

      </table>
    </div>
  </body>
</html>
        '''.format(css=cssfile.read(), \
                   uri=settings['URI'], \
                   totals_caption=page_elements.totals_caption(ledger), \
                   bills_per_person=page_elements.get_bills_per_person(ledger), \
                   debts_table=page_elements.showdebts(ledger))

        msg = MIMEMultipart('alternative')
        msg['Subject'] = settings['reminder_subject']
        msg['From'] = 'bills@%s'%settings['domain']
        msg['To'] = ','.join(settings['email_addresses'])
        text_part = MIMEText(text, 'plain')
        html_part = MIMEText(html, 'html')

        msg.attach(text_part)
        msg.attach(html_part)

        s = smtplib.SMTP('localhost')
        s.sendmail('bills@%s'%settings['domain'], settings['email_addresses'], msg.as_string())
        s.quit()
