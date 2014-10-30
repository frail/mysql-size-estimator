mysql-size-estimator
===================

mysql-size-estimator is a simple tool to estimate mysql table size for given table schema. It's not 100% accurate nor it could ever be. It's much better to use this tool to give an insight.

The string fields would assume that it would be used fully. 

Usages :
===============

## Simple usages 

or from sql file :

    ./mysql-size-estimator.py create1.sql
    
if you don't have a create script use dummy feature

    ./mysql-size-estimator.py dummy -c "id INT" -c "user_id INT" -c "name VARCHAR(10) CHARACTER SET latin1" -i "PRIMARY KEY id" -i "KEY idx_name (name)"
    
if you have specific row counts to do the estimation you can write them aswell
 
     ./mysql-size-estimator.py dummy -c "id INT" -r 1000000 -r 14000000 -r 1700000

## Advanced usages

pull data directly from db :

    mysql -e 'SHOW CREATE TABLE mysql.user\G' --skip-column-names | awk 'NR > 2' | ./mysql-size-estimator.py -

check out what would change if you add/change an index (names should be unique) : 
     
     ... | ./mysql-size-estimator.py - -i "KEY idx_category(category, created_at)"

if the results seems absurd check out string fields and re-arrange their size on fly. or even change their data type.

    ... | ./mysql-size-estimator.py - -c "text1 VARCHAR(10)" -c "text2 TEXT(100)"



Important links
===============

- http://dev.mysql.com/doc/refman/5.5/en/storage-requirements.html
- http://dev.mysql.com/doc/refman/5.5/en/innodb-physical-record.html
- http://mysqlha.blogspot.com.tr/2009/01/innodb-myisam-and-disk-space_16.html
- http://blog.jcole.us/2013/01/07/the-physical-structure-of-innodb-index-pages/
- http://blog.jcole.us/2013/01/10/the-physical-structure-of-records-in-innodb/
- http://blog.jcole.us/2013/01/10/btree-index-structures-in-innodb/


Contributing
~~~~~~~~~~~~

I would be very happy if you do contribute.

Please make sure you make the code a little less complicated with each commit.
