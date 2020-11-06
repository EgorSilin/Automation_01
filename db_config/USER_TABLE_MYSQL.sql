mysql

CREATE DATABASE name_db;


USE name_db;

CREATE TABLE FIRST_LAST_NAME (
   id INT NOT NULL,
   first_name VARCHAR(30) NOT NULL,
   last_name VARCHAR(30) NOT NULL,
   PRIMARY KEY ( id )
);


SHOW TABLES;


DESCRIBE FIRST_LAST_NAME;

INSERT INTO FIRST_LAST_NAME
       VALUES (111, 'FName111', 'LName111');


UPDATE FIRST_LAST_NAME
SET first_name = 'FName1113', last_name = 'LName1113'
WHERE id = 111;

DELETE FROM FIRST_LAST_NAME;


SELECT * FROM FIRST_LAST_NAME;

mysqldump name_db > /home/user/Dropbox/JobFinderTasks/1/name_db_dump.sql
mysql name_db < /home/user/Dropbox/JobFinderTasks/1/name_db_dump.sql