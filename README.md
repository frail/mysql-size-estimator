mysql-size-estimator
===================

mysql-size-estimator is a simple tool to estimate mysql table size for given table schema. It's not 100% accurate nor it could ever be. It's much better to use this tool to give an insight.

The string fields would assume that it would be used fully. Thats why I put "overwrite column" feature; you can always check log

Usages :
===============

directly from db :

    mysql -e 'SHOW CREATE TABLE mysql.user\G' --skip-column-names | awk 'NR > 2' | ./mysql-size-estimator.py -

or from sql file :

    ./mysql-size-estimator.py create1.sql


Important links
===============

The links below are important to get a hold of what this code is trying to do

- http://dev.mysql.com/doc/refman/5.5/en/storage-requirements.html
- http://dev.mysql.com/doc/refman/5.5/en/innodb-physical-record.html
- http://mysqlha.blogspot.com.tr/2009/01/innodb-myisam-and-disk-space_16.html


Contributing
~~~~~~~~~~~~

I would be very happy if you do contribute.

Please make sure you make the code a little less complicated with each commit.
