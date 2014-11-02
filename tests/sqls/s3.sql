CREATE TABLE sample.taceledger (
`runno` INT(10) unsigned not null default '0',
`doc_no` DECIMAL(6,0) unsigned NOT null ,
`doc_date` DATE,
`gl` DECIMAL(4,0) unsigned not null ,
`slcode` VARCHAR(6) not null ,
`tr` VARCHAR(1) not null ,
`cr_db` VARCHAR(1) not null,
`amount` DECIMAL(13,2) unsigned not null ,
`revcode` DECIMAL(4,0) unsigned not null ,
`narration` VARCHAR(30) not null,
cramt DECIMAL(13,2) unsigned not null,

`indi` VARCHAR(1) not null ,

`dbamt` DECIMAL(13,2) unsigned not null,
`acctype` VARCHAR(1) not null,
PRIMARY KEY (`runno`)
)ENGINE=InnoDB;