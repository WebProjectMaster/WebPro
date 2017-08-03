import pytest
import settings
import logging
import database
import MySQLdb

def executeScriptsFromFile(filename, db):
    # Open and read the file as a single buffer
    fd = open(filename, mode = 'r', encoding='utf-8')
    sqlFile = fd.read()
    fd.close()
    # all SQL commands (split on ';')
    sqlCommands = sqlFile.split(';')
    c = db.cursor()
    # Execute every command from the input file
    c.execute('SET NAMES `utf8`')
    for command in sqlCommands:
        # This will skip and report errors
        # For example, if the tables do not yet exist, this will skip over
        # the DROP TABLE commands
        try:
            c.execute(command)
            # logging.info('executeScriptsFromFile command: %s', command)
        except Exception as msg:
            logging.error("Command skipped: ", msg)
    c.close()

@pytest.fixture
def test_db():
    database.db = MySQLdb.connect(**settings.TEST_DATABASE)
    return database.db

def clean_test_db():
    database.db = MySQLdb.connect(**settings.TEST_DATABASE)
    db = database.db
    executeScriptsFromFile("./sql/db_init_mysql.sql", db)
    executeScriptsFromFile("./sql/db_load_sites.sql", db)
    executeScriptsFromFile("./sql/db_load_persons.sql", db)
    executeScriptsFromFile("./sql/db_load_keywords.sql", db)
    executeScriptsFromFile("./sql/db_load_pages.sql", db)
    return db