Server software for tracking who paid which bill, and who owes
how much money to whom.

![alt tag](https://raw.githubusercontent.com/jperryhouts/roommate_bills_tracker/master/Screenshot.png)

```
git clone https://github.com/jperryhouts/roommate_bills_tracker.git
cd roommate_bills_tracker

# Install bill-tracker
rsync -av --delete --exclude "model" source/ /usr/local/www/apache24/

# Configure
mkdir -p /usr/local/www/apache24/model
cp source/model/settings.json.sample /usr/local/www/apache24/model/settings.json
edit /usr/local/www/apache24/model/settings.json

# Setup Apache:
patch /usr/local/etc/apache24/httpd.conf doc/httpd.conf.patch
htpassword -c /usr/local/etc/apache24/passwords 1065
service apache24 restart
```
