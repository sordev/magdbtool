import sys, os.path, subprocess as subp, datetime as dt, os, time, re
#import xml.etree.ElementTree as et
#xml processor
from xml.dom import minidom
#mysql
#import MySQLdb as mysql

#vars
localxml = '../www/app/etc/local.xml'

#set your development base domain here will be used like DATABASENAME.DEVDOMAIN subdomain structure
devdomain = ''

#use this different for every project
baselocal = ''
basedev = ''
baselive = ''

print("Hello Dev")
args = sys.argv

if(len(args) == 1):
	print('Available commands')
	print('-export "Will export DB based on local.xml"')
	print('-truncate "Will export > drop > create db"')
	print('-import "Will export > drop > create > import DB with given sql should be exported From this tool"')
	print('-todev, -tolocal and -tolive "Will change base url to dev or local based on DB name"')
	print('-cleardata "Will clean all data including products, attribues, logs, caches"')

#get all data first
if (os.path.exists(localxml)):
	xmldata = minidom.parse(localxml)
	#getting first occurence
	u = xmldata.getElementsByTagName('username')[0].firstChild.nodeValue
	p = xmldata.getElementsByTagName('password')[0].firstChild.nodeValue
	db = xmldata.getElementsByTagName('dbname')[0].firstChild.nodeValue
	h = xmldata.getElementsByTagName('host')[0].firstChild.nodeValue
	start()
else:
	print('Can\'t find local.xml')
	exit

#export function 
def export():
	filestamp = time.strftime('%Y-%m-%d-%I-%M')
	exportcmd = 'mysqldump -u '+u+' -p'+p+' '+db+' > '+db+'-'+filestamp+'.sql'
	print('Exporting Database '+db+'')
	#subp.call(export)
	os.popen(exportcmd)
	print('Database backup done')
        
#truncate function
def truncate():
	proot = input("MySQL root pass: ")
			
	if (os.path.exists('truncate-'+db+'.sql') != True):
			with open('truncate-'+db+'.sql','w+') as file:
					file.write('DROP DATABASE '+db+';\n')
					file.write('CREATE DATABASE '+db+';')
	if (proot):
			truncatecmd = 'mysql -u root -p'+proot+' '+db+' < truncate-'+db+'.sql'
	else:
			truncatecmd = 'mysql -u root '+db+' < truncate-'+db+'.sql'
	print('Truncating '+db+'')
	os.popen(truncatecmd)
        
#importdb function
def importdb():
	selre = re.compile(db+'-\d*-\d*-\d*-\d*-\d*.sql')
	for arg in args:
		seldbobj = selre.match(arg)
	seldb = seldbobj.group()
	if (seldb):
		print(seldb)
	else:
		print('Input SQL file')
	importcmd = 'mysql -u '+u+' -p'+p+' '+db+' < '+seldb
	print('Importing '+db+'')
	os.popen(importcmd)

#base changer
def basechange(where):
	if (where == 'dev'):
		if (len(basedev)==0):
			base = "http://"+db+"."+devdomain+"/"
		else:
			base = "http://"+basedev+"/"
			
	elif (where == 'local'):
		base = "http://"+db+".local/"
	elif (where == 'live'):
		base ="http://"+baselive+"/"
	changesql = 'to-'+where+'-'+db+'.sql'
	if (os.path.exists(changesql) != True):
			with open(changesql,'w+') as file:
					file.write("use "+db+";\n"+
							   "update core_config_data set value = '"+base+"' where path = 'web/unsecure/base_url';\n"+
							   "update core_config_data set value = '"+base+"' where path = 'web/secure/base_url';\n")
	print('Changing base to '+base)
	changecmd = 'mysql -u '+u+' -p'+p+' '+db+' < '+changesql
	os.popen(changecmd)                        

def start():
	if ("-export" in args):
			export()

	if ("-truncate" in args):
			#export before drop and create
			export()
			truncate()

	if ("-import" in args):
			#export current db before import
			export()
			#truncate before import
			truncate()
			importdb()
			
	if ("-todev" in args):
			basechange('dev')

	if ("-tolocal" in args):
			basechange('local')
			
	if ("-tolocal" in args):
			basechange('live')

	if ("-cleardata" in args):
		#backup before do anything
		#export()
		
		cleardatasql = 'cleardata-'+db+'.sql'
		if (os.path.exists(cleardatasql) != True):
			with open(cleardatasql,'w+') as file:
				file.write("SET FOREIGN_KEY_CHECKS = 0;\n"+
					# deleting all products
					"TRUNCATE TABLE `catalog_product_bundle_option`;\n"+
					"TRUNCATE TABLE `catalog_product_bundle_option_value`;\n"+
					"TRUNCATE TABLE `catalog_product_bundle_selection`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_datetime`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_decimal`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_gallery`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_int`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_media_gallery`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_media_gallery_value`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_text`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_tier_price`;\n"+
					"TRUNCATE TABLE `catalog_product_entity_varchar`;\n"+
					"TRUNCATE TABLE `catalog_product_option`;\n"+
					"TRUNCATE TABLE `catalog_product_option_price`;\n"+
					"TRUNCATE TABLE `catalog_product_option_title`;\n"+
					"TRUNCATE TABLE `catalog_product_option_type_price`;\n"+
					"TRUNCATE TABLE `catalog_product_option_type_title`;\n"+
					"TRUNCATE TABLE `catalog_product_option_type_value`;\n"+
					"TRUNCATE TABLE `catalog_product_super_attribute`;\n"+
					"TRUNCATE TABLE `catalog_product_super_attribute_label`;\n"+
					"TRUNCATE TABLE `catalog_product_super_attribute_pricing`;\n"+
					"TRUNCATE TABLE `catalog_product_super_link`;\n"+
					"TRUNCATE TABLE `catalog_product_enabled_index`;\n"+
					"TRUNCATE TABLE `catalog_product_website`;\n"+
					"TRUNCATE TABLE `catalog_product_entity`;\n"+

					#cleaning things
					"TRUNCATE TABLE `cataloginventory_stock`;\n"+
					"TRUNCATE TABLE `cataloginventory_stock_item`;\n"+
					"TRUNCATE TABLE `cataloginventory_stock_status`;\n"+
					"TRUNCATE TABLE `core_cache`;\n"+
					"TRUNCATE TABLE `core_cache_option`;\n"+
					"TRUNCATE TABLE `core_cache_tag`;\n"+
					"TRUNCATE TABLE `core_session`;\n"+

					#cleaning logs
					"TRUNCATE TABLE `log_customer`;\n"+
					"TRUNCATE TABLE `log_quote`;\n"+
					"TRUNCATE TABLE `log_summary`;\n"+
					"TRUNCATE TABLE `log_summary_type`;\n"+
					"TRUNCATE TABLE `log_url`;\n"+
					"TRUNCATE TABLE `log_url_info`;\n"+
					"TRUNCATE TABLE `log_visitor`;\n"+
					"TRUNCATE TABLE `log_visitor_info`;\n"+
					"TRUNCATE TABLE `log_visitor_online`;\n"+

					#url-write
					"TRUNCATE TABLE `core_url_rewrite`;\n"+

					# Enterprise specific
					#"TRUNCATE TABLE `enterprise_logging_event`;\n"+
					#"TRUNCATE TABLE `enterprise_logging_event_changes`;\n"+
					"TRUNCATE TABLE `index_event`;\n"+
					"TRUNCATE TABLE `index_process_event`;\n"+
					"TRUNCATE TABLE `report_event`;\n"+
					"TRUNCATE TABLE `report_viewed_product_index`;\n"+
					"TRUNCATE TABLE `dataflow_batch_export`;\n"+
					"TRUNCATE TABLE `dataflow_batch_import`;\n"+
					# TODO might there be more don't truncate or check before
					#"TRUNCATE TABLE `catalog_product_flat_1`;\n"+
					#"TRUNCATE TABLE `catalog_category_flat_store_1`;\n"+

					"insert into `cataloginventory_stock`(`stock_id`,`stock_name`) values (1,'Default');\n"+
					"ALTER TABLE `catalog_product_entity` AUTO_INCREMENT =1;\n"+

					"SET FOREIGN_KEY_CHECKS = 1;\n"+
					#clean the count in cat
					"DELETE FROM `catalog_category_product` where product_id NOT IN (SELECT entity_id FROM (catalog_product_entity));\n"+
					#deleting all attribute created after installation
					"DELETE FROM `eav_attribute` WHERE `attribute_id` > 133;")
		print('Cleaning DATA')
		cleardatacmd = 'mysql -u '+u+' -p'+p+' '+db+' < '+cleardatasql
		os.popen(cleardatacmd)
