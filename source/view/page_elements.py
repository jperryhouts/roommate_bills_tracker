# -*- coding: UTF-8 -*-
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

import StringIO
from decimal import Decimal as Dec
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def showtransactions (ledger):
    output = StringIO.StringIO()
    all_transactions = ledger.get_all()
    all_transactions.reverse()
    for i, (transaction_id, date, whofrom, whoto, amount, comment) in enumerate(all_transactions):
        amount = locale.currency(amount)
        output.write('  <tr>\n')
        output.write('    <td class="date">'+str(date)+'</td>\n')
        output.write('    <td class="name">'+str(whofrom)+'</td>\n')
        output.write('    <td class="name">'+str(whoto)+'</td>\n')
        output.write('    <td class="currency">'+str(amount)+'</td>\n')
        output.write('    <td>'+str(comment)+'</td>\n')
        output.write('    <td class="submit">')
        if i < 5:
            # Only allow the most recent transactions to be deleted
            output.write('<form method="post">\n')
            output.write('        <input type="hidden" name="delete" value="')
            output.write(transaction_id)
            output.write('"/>\n')
            output.write('        <input type="submit" value="X"/>\n')
            output.write('    </form>')
        output.write('</td>\n')
        output.write('  </tr>\n')
    return output.getvalue()

def totals_caption (ledger):
    total_bills = ledger.all_bills()
    n_roommates = len(ledger.get_account_names())
    bills_per_person = Dec(total_bills) / Dec(n_roommates)
    return 'Expenses (Net amount paid to \'BILLS\'): ${0:.2f} (${1:.2f} / each)'.format(total_bills, bills_per_person)

def get_bills_per_person (ledger):
    total_bills = ledger.all_bills()
    n_roommates = len(ledger.get_account_names())
    bills_per_person = Dec(total_bills) / Dec(n_roommates)
    return '${0:.2f}'.format(bills_per_person)

def showdebts (ledger):
    output = StringIO.StringIO()
    total_bills = ledger.all_bills()
    n_roommates = len(ledger.get_account_names())
    bills_per_person = Dec(total_bills) / Dec(n_roommates)
    one_cent = Dec('0.01')
    for name in ledger.get_account_names():
        paid, received = ledger.get_paid_received(name)
        owes = bills_per_person-(paid-received)
        money_class = 'the_black' if owes < Dec('0.01') else 'the_red'
        output.write('  <tr>\n')
        output.write('    <td>'+name+'</td>\n')
        output.write('    <td>'+locale.currency(paid-received)+'</td>\n')
        output.write('    <td class="{}">'.format(money_class)+locale.currency(owes.quantize(one_cent))+'</td>\n')
        output.write('  </tr>\n')
    return output.getvalue()

def roommate_dropdown(account_names, include_bills):
    output = StringIO.StringIO()
    output.write('<select name="{}">\n'.format('TO' if include_bills else 'FROM'))
    output.write('  <option value="NULL">--</option>\n')
    for name in account_names:
        output.write('  <option value="{0}">{0}</option>\n'.format(name))
    if include_bills:
        output.write('  <option value="BILLS">BILLS</option>\n')
    output.write('</select>\n')
    return output.getvalue()
