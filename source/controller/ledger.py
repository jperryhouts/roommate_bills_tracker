import os, re, sqlite3
from decimal import Decimal as Dec
from datetime import datetime

class Ledger():
    def __init__ (self, dbpath, account_names):
        self.account_names = account_names
        self.dbpath = dbpath

    def __enter__(self):
        if not os.path.exists(self.dbpath):
            self.db = self.createdb(self.dbpath)
        else:
            self.db = sqlite3.connect(self.dbpath)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def get_account_names (self):
        return sorted(self.account_names)

    def createdb (self, db):
        ledger = sqlite3.connect(db)
        with ledger:
            cur = ledger.cursor()
            cur.execute('CREATE TABLE Transactions\
                    (TransactionID INTEGER PRIMARY KEY ASC, \
                    Date DATE, \
                    WhoFrom TEXT NOT NULL, \
                    WhoTo TEXT NOT NULL, \
                    Amount DECIMAL(5,2) NOT NULL, \
                    Comment TEXT)')
        return ledger

    def insert (self, date, whofrom, whoto, amount, comment):
        with open('../model/log.txt', 'a') as log, self.db as ledger:
            print >>log, '%s Creating record: %s %s %s $%0.2f "%s"'%(datetime.now().isoformat(), \
                    date, whofrom, whoto, float(amount), comment)
            cur = ledger.cursor()
            cur.execute("INSERT INTO Transactions (Date, WhoFrom, WhoTo, Amount, Comment) \
                    VALUES(:date, :whofrom, :whoto, :amount, :comment)",\
                    {'date':date, 'whofrom':whofrom, 'whoto':whoto, 'amount':amount, 'comment':comment})

    def delete (self, entry_id):
        with open('../model/log.txt', 'a') as log, self.db as ledger:
            cur = ledger.cursor()
            cur.execute("SELECT * FROM Transactions WHERE TransactionID=?", (entry_id,))
            date, whofrom, whoto, amount, comment = cur.fetchall()[0][1:6]
            print >>log, '%s Removing record: %s %s %s $%0.2f "%s"'%(datetime.now().isoformat(), \
                    date, whofrom, whoto, float(amount), comment)
            cur.execute("DELETE FROM Transactions WHERE TransactionID=?", (entry_id,))

    def get_all (self):
        with self.db as ledger:
            cur = ledger.cursor()
            cur.execute('SELECT * FROM Transactions')
            return cur.fetchall()

    def get_paid_received (self, who):
        with self.db as ledger:
            cur = ledger.cursor()
            cur.execute("SELECT Amount FROM Transactions WHERE WhoFrom=:who", {'who':who})
            paid = sum([Dec(str(record[0])) for record in cur.fetchall()])
            cur.execute("SELECT Amount FROM Transactions WHERE WhoTo=:who", {'who':who})
            received = sum([Dec(str(record[0])) for record in cur.fetchall()])
            return (paid, received)

    def all_bills (self):
        with self.db as ledger:
            cur = ledger.cursor()
            cur.execute("SELECT Amount from Transactions WHERE WhoTo='BILLS'")
            return sum([Dec(str(record[0])) for record in cur.fetchall()])

    def add_remove_transaction(self, form):
        delentry = form.getvalue('delete', '')
        if not form.getvalue('delete', '') == '':
            self.delete(form.getvalue('delete'))
            return '<div class="success">Transaction successfully deleted.</div>'
        date = form.getvalue('WHEN', '').strip()
        whofrom = form.getvalue('FROM', '').strip()
        whoto = form.getvalue('TO', '').strip()
        amount = form.getvalue('AMOUNT', '').replace('$','').strip()
        comment = form.getvalue('COMMENT', '').strip()
        if date == '' \
                and whofrom == '' \
                and whoto == '' \
                and amount == '' \
                and comment == '':
                    return ''
        if re.match(r'20\d\d-\d\d?-\d\d?', date) == None:
            return '<div class="warning">Error: Date must be in format: YYYY-MM-DD</div>'
        if whofrom == 'NULL' or whoto == 'NULL':
            return '<div class="warning">Error: You must select who money is coming from, and where is is going to.</div>'
        if re.match(r'\d+\.?\d*', amount) == None:
            return '<div class="warning">Error: You must specify a valid amount.</div>'

        self.insert(date, whofrom, whoto, amount, comment)
        return '<div class="success">Transaction successfully recorded.</div>'
    
