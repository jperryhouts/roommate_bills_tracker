#!/usr/local/bin/python2
# -*- coding: UTF-8 -*-

import cgitb, sys
cgitb.enable()
sys.path.insert(0, '../controller')
import cgi, datetime, json, StringIO
from html5print import HTMLBeautifier
from decimal import Decimal as Dec
from ledger import Ledger
import page_elements

if __name__ == '__main__':
    settings = json.load(open('../model/settings.json'))
    ledger = Ledger('../model/ledger.db', settings['roommate_names'])

    html = '''
           <!DOCTYPE html>
           <html>
           <head>
               <title>Cannon Ct. Bills</title>
               <link rel="stylesheet" href="style/styles.css">
           </head>
           
           <body>
               <a class="right" href="https://github.com/jperryhouts/roommate_bills_tracker">Source Code</a>
               {warnings}

               <div class="content">
                   <table>
                       <caption>{totals_caption}</caption>
                       <tr>
                           <th class="date">Name</th>
                           <th>Total paid</th>
                           <th>Total owed</th>
                       </tr>

                       {debts_table}

                   </table>
               </div>

               <div class="content">
                   <p>
                        <table>
                            <caption>Transactions</caption>
                            <tr>
                                <th class="date">Date</th>
                                <th class="name">From</th>
                                <th class="name">To</th>
                                <th class="currency">Amount</th>
                                <th>Comment</th>
                                <th class="submit"></th>
                            </tr>

                           {transactions_table}

                        </table>
                   </p>

                   <p>
                       <form method="post">
                           <table>
                               <tr>
                                   <th class="date"><input type="text" name="WHEN" value="{current_date}" /></th>
                                   <th class="name">{whofrom_dropdown}</th>
                                   <th class="name">{whoto_dropdown}</th>
                                   <th class="currency"><input type="text" name="AMOUNT" /></th>
                                   <th><input type="text" name="COMMENT" /></th>
                                   <th class="submit"><input type="submit" value="+" /></th>
                               </tr>
                           </table>
                       </form>
                   </p>
               </div>
           </body>
           </html>'''.format(warnings=ledger.add_remove_transaction(cgi.FieldStorage()), \
                   totals_caption=page_elements.totals_caption(ledger), \
                   debts_table=page_elements.showdebts(ledger), \
                   transactions_table=page_elements.showtransactions(ledger), \
                   current_date=datetime.datetime.now().isoformat()[:10], \
                   whofrom_dropdown=page_elements.roommate_dropdown(ledger.get_account_names(), False), \
                   whoto_dropdown=page_elements.roommate_dropdown(ledger.get_account_names(), True))

    print('Content-Type: text/html;charset=utf-8')
    print('')
    print(HTMLBeautifier.beautify(html))
    ledger.close()
