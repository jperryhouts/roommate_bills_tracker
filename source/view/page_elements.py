# -*- coding: UTF-8 -*-

import StringIO
from decimal import Decimal as Dec
import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def showtransactions (ledger):
    output = StringIO.StringIO()
    for (transaction_id, date, whofrom, whoto, amount, comment) in ledger.get_all():
        amount = locale.currency(amount)
        output.write('  <tr>\n')
        for col in (date, whofrom, whoto, amount, comment):
            output.write('    <td>'+str(col)+'</td>\n')
        output.write('    <td><form method="post">\n')
        output.write('        <input type="hidden" name="delete" value="')
        output.write(transaction_id)
        output.write('"/>\n')
        output.write('        <input type="submit" value="X"/>\n')
        output.write('    </form></td>\n')
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
        money_class = 'the_black' if owes < Dec('0.00') else 'the_red'
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
