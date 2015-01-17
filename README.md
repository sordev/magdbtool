# MagDBTool

This is my first ever python coding. Meant to make my work flow little bit easier.

##Usage

Put this file on parellel folder of magento root. So it can detect magento's configuration file like this ../www/app/etc/local.xml or you can change default to something else

After setting up you can run tool like this
```sh
$ python tools.py -export
```

##Commands

	-export "Will export DB based on local.xml"
	-truncate "Will export > drop > create db"
    -import "Will export > drop > create > import DB with given sql should be exported From this tool"
	-todev, -tolocal and -tolive "Will change base url to dev or local based on DB name"
	-cleardata "Will clean all data including products, attribues, logs, caches"

I recommend to use this carefully, on your own risk and take backup all the time. Currently working with magento CE1.9.1.0 EE1.14.1.0
