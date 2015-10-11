# -*- coding: UTF-8 -*-

import StringIO
from decimal import Decimal as Dec

def showtransactions (ledger):
    output = StringIO.StringIO()
    output.write('<table>\n')
    output.write('<caption>Transactions</caption>\n')
    output.write('  <tr>\
            <th class="date">Date</th>\
            <th class="name">From</th>\
            <th class="name">To</th>\
            <th class="currency">Amount</th>\
            <th>Comment</th>\
            <th class="delete_column"></th>\
            </tr>\n')
    for (transaction_id, date, whofrom, whoto, amount, comment) in ledger.get_all():
        output.write('  <tr>\n')
        for col in (date, whofrom, whoto, amount, comment):
            output.write('    <td>'+str(col)+'</td>\n')
        output.write('    <td class="deletebutton"><form class="deletebutton" method="post"><input type="hidden" name="delete" value="'+str(transaction_id)+'"/><input class="deletebutton" type="submit" value="X"/></form></td>\n')
        output.write('  </tr>\n')
    output.write('</table>\n')
    return output.getvalue()

def showdebts (ledger):
    output = StringIO.StringIO()
    total_bills = ledger.all_bills()
    n_roommates = len(ledger.get_account_names())
    bills_per_person = Dec(total_bills) / Dec(n_roommates)
    one_cent = Dec('0.01')
    output.write('<table>\n')
    output.write('<caption>Total Expenses: ${0:.2f} (${1:.2f} / each)</caption>\n'.format(total_bills, bills_per_person))
    output.write('  <tr>\
            <th class="date">Name</th>\
            <th>Total paid</th>\
            <th>Total owed</th></tr>\n')
    for name in ledger.get_account_names():
        paid, received = ledger.get_paid_received(name)
        owed = (paid-received)-bills_per_person
        money_class = 'the_black' if owed >= Dec('0.00') else 'the_red'
        output.write('  <tr>\n')
        output.write('    <td>'+name+'</td>\n')
        output.write('    <td>'+str(paid-received)+'</td>\n')
        output.write('    <td class="{}">'.format(money_class)+str(owed.quantize(one_cent))+'</td>\n')
        output.write('  </tr>\n')
    output.write('</table>\n')
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
