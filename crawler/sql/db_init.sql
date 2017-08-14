--
-- Файл сгенерирован с помощью SQLiteStudio v3.1.1 в Чт июл 20 16:31:59 2017
--
-- Использованная кодировка текста: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: Keywords
DROP TABLE IF EXISTS Keywords;

CREATE TABLE Keywords (
    ID       INTEGER        PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT
                            NOT NULL
                            UNIQUE,
    Name     VARCHAR (2048) NOT NULL,
    PersonID INTEGER        NOT NULL ON CONFLICT ROLLBACK
);


-- Таблица: Pages
DROP TABLE IF EXISTS Pages;

CREATE TABLE Pages (
    ID            INTEGER        PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT
                                 UNIQUE ON CONFLICT ROLLBACK
                                 NOT NULL ON CONFLICT ROLLBACK,
    Url           VARCHAR (2048) NOT NULL ON CONFLICT ROLLBACK,
    SiteID        INTEGER        NOT NULL ON CONFLICT ROLLBACK,
    FoundDeteTime DATETIME       NOT NULL ON CONFLICT ROLLBACK,
    LastScanDate  DATETIME,
    hash_url      VARCHAR (32)
);
# create trigger pages_insert before insert on pages for each row begin set new.url_md5 = md5(new.url); end;
CREATE UNIQUE INDEX unique_url_hash on Pages (hash_url);



-- Таблица: PersonPageRank
DROP TABLE IF EXISTS PersonPageRank;

CREATE TABLE PersonPageRank (
    PersonID INTEGER NOT NULL ON CONFLICT ROLLBACK,
    PageID   INTEGER NOT NULL ON CONFLICT ROLLBACK,
    Rank     INTEGER DEFAULT (0)
);


-- Таблица: Persons
DROP TABLE IF EXISTS Persons;

CREATE TABLE Persons (
    ID   INTEGER        PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT
                        UNIQUE ON CONFLICT ROLLBACK
                        NOT NULL ON CONFLICT ROLLBACK,
    Name VARCHAR (2048) UNIQUE ON CONFLICT ROLLBACK
                        NOT NULL ON CONFLICT ROLLBACK
);


-- Таблица: Sites
DROP TABLE IF EXISTS Sites;

CREATE TABLE Sites (
    ID   INTEGER       PRIMARY KEY ASC ON CONFLICT ROLLBACK AUTOINCREMENT
                       NOT NULL ON CONFLICT ROLLBACK
                       UNIQUE ON CONFLICT ROLLBACK,
    Name VARCHAR (256) UNIQUE ON CONFLICT ROLLBACK
                       NOT NULL ON CONFLICT ROLLBACK
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
