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
htpassword -c /usr/local/etc/apache24/passwords LOGIN (replace LOGIN with the login name)
service apache24 restart
```

<pre>
The patch in the Apache setup step will do the following:
  * Enable mod_cgid
  * Enable mod_include
  * Uncomment ServerAdmin <email address> (manually change this)
  * Set DocumentRoot "/usr/local/www/apache24/view"
  * Uncomment ServerName (manually change this)
  * Add Option Includes
  * Set XBitHack on
  * Enable .htaccess AuthConfig override
  * Setup Authorization
  * Set ScriptAlias to 'controller' directory
  * Enable executing Python scripts in 'controller' directory
</pre>
