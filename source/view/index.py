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
                   {debts_table}
               </div>

               <div class="content">
                   <p>
                       {transactions_table}
                   </p>

                   <p>
                       <form method="post">
                           <table>
                               <tr>
                                   <td class="date"><input type="text" name="WHEN" value="{current_date}" /></td>
                                   <td class="name">{whofrom_dropdown}</td>
                                   <td class="name">{whoto_dropdown}</td>
                                   <td class="currency"><input type="text" name="AMOUNT" /></td>
                                   <td><input type="text" name="COMMENT" /></td>
                               </tr>
                           </table>
                           <input class="submit_button" type="submit" value="Add" />
                       </form>
                   </p>
               </div>
           </body>
           </html>'''.format(warnings=ledger.add_remove_transaction(cgi.FieldStorage()), \
                   debts_table=page_elements.showdebts(ledger), \
                   transactions_table=page_elements.showtransactions(ledger), \
                   current_date=datetime.datetime.now().isoformat()[:10], \
                   whofrom_dropdown=page_elements.roommate_dropdown(ledger.get_account_names(), False), \
                   whoto_dropdown=page_elements.roommate_dropdown(ledger.get_account_names(), True))

    print('Content-Type: text/html;charset=utf-8')
    print('')
    print(HTMLBeautifier.beautify(html))
    ledger.close()
