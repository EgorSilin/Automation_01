sudo isql-fb

create database "/var/lib/firebird/3.0/data/name_db.fdb" user 'SYSDBA' password 'user@7136498';

SHOW DB;

connect "/var/lib/firebird/3.0/data/name_db.fdb" user 'SYSDBA' password 'user@7136498';

CREATE TABLE FIRST_NAME (id INT NOT NULL PRIMARY KEY, first_name VARCHAR(30) NOT NULL);
CREATE TABLE LAST_NAME (id INT NOT NULL PRIMARY KEY, last_name VARCHAR(30) NOT NULL);

alter table first_name add foreign key (id) references last_name (id) on delete cascade on update cascade;

show tables;


INSERT INTO FIRST_NAME VALUES (1, 'FName1');
INSERT INTO FIRST_NAME VALUES (2, 'FName2');
INSERT INTO FIRST_NAME VALUES (3, 'FName3');
INSERT INTO FIRST_NAME VALUES (4, 'FName4');
INSERT INTO FIRST_NAME VALUES (5, 'FName5');

select * from FIRST_NAME;

INSERT INTO LAST_NAME VALUES (1, 'LName1');
INSERT INTO LAST_NAME VALUES (2, 'LName2');
INSERT INTO LAST_NAME VALUES (3, 'LName3');
INSERT INTO LAST_NAME VALUES (4, 'LName4');
INSERT INTO LAST_NAME VALUES (5, 'LName5');

INSERT INTO LAST_NAME VALUES (6, 'LName6') AND INSERT INTO FIRST_NAME VALUES (6, 'FName6');

select * from LAST_NAME;

COMMIT;
quit;


DROP TABLE FIRST_NAME;
DROP TABLE LAST_NAME;

# Разблокировка базы
gfix  -user "SYSDBA" -password "user@7136498" -online /var/lib/firebird/3.0/data/name_db.fdb
gfix  -user "SYSDBA" -password "user@7136498" -shut -force 0 /var/lib/firebird/3.0/data/name_db.fdb

# Backup
gbak <options> -user <username> -password <password> <source> <destination>

#A regular Restore
gbak -c -v -user SYSDBA -password masterkey c:\backups\warehouse.fbk dbserver:/db/warehouse2.fdb

#Restore to an already existing database (Firebird 2.x)
gbak -r o -v -user SYSDBA -password masterkey c:\backups\warehouse.fbk dbserver:/db/warehouse.fdb

gbak -v -t -user SYSDBA -password "user@7136498" localhost:/var/lib/firebird/3.0/data/name_db.fdb /home/user/Dropbox/JobFinderTasks/1/name_db_dump.fbk
gbak -r o -v -user SYSDBA -password "user@7136498" /home/user/Dropbox/JobFinderTasks/1/name_db_dump.fbk localhost:/var/lib/firebird/3.0/data/name_db.fdb

# Логопас
user=SYSDBA
password=user@7136498