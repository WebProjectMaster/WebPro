-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: webpro
-- ------------------------------------------------------
-- Server version	5.7.16-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add user',2,'add_user'),(5,'Can change user',2,'change_user'),(6,'Can delete user',2,'delete_user'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add permission',4,'add_permission'),(11,'Can change permission',4,'change_permission'),(12,'Can delete permission',4,'delete_permission'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add persons',7,'add_persons'),(20,'Can change persons',7,'change_persons'),(21,'Can delete persons',7,'delete_persons'),(22,'Can add sites',8,'add_sites'),(23,'Can change sites',8,'change_sites'),(24,'Can delete sites',8,'delete_sites'),(25,'Can add person page rank',9,'add_personpagerank'),(26,'Can change person page rank',9,'change_personpagerank'),(27,'Can delete person page rank',9,'delete_personpagerank'),(28,'Can add pages',10,'add_pages'),(29,'Can change pages',10,'change_pages'),(30,'Can delete pages',10,'delete_pages'),(31,'Can add keywords',11,'add_keywords'),(32,'Can change keywords',11,'change_keywords'),(33,'Can delete keywords',11,'delete_keywords'),(34,'Can add Token',12,'add_token'),(35,'Can change Token',12,'change_token'),(36,'Can delete Token',12,'delete_token');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'48474f975022f960bc2afbe49be581e8','2017-07-30 20:49:12.781393',1,'root','','','',1,1,'2017-07-22 23:36:51.774535'),(2,'48474f975022f960bc2afbe49be581e8','2017-08-01 16:52:09.423921',0,'dima','jfj','awalk','wadad@yandex.ru',0,1,'2017-07-24 01:55:37.949785'),(6,'202cb962ac59075b964b07152d234b70','2017-07-24 20:50:39.699103',0,'ddd','awdad','awdad','123213@yandex.ru',0,1,'2017-07-24 20:50:32.227454'),(9,'202cb962ac59075b964b07152d234b70','2017-07-27 23:26:11.369864',0,'dimaroot','wijfjwefop','dima','dabi@yandex.ru',0,1,'2017-07-27 23:25:57.150281'),(10,'202cb962ac59075b964b07152d234b70',NULL,0,'root123','aaa','aaa','aaa@aaa.ru',0,1,'2017-07-27 23:27:28.205053'),(11,'202cb962ac59075b964b07152d234b70','2017-07-27 23:28:50.350378',1,'root1234','aaa','aaa','aaa@aaa.ru',0,1,'2017-07-27 23:28:26.059145'),(12,'202cb962ac59075b964b07152d234b70','2017-07-29 20:49:21.770084',1,'root12345','wijfjwefop','dima','aaa@aaa.ru',1,1,'2017-07-27 23:32:45.108316');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('bdf8d2d8196727d16894c32507a1bbcbba27cdaa','2017-07-31 08:26:48.565618',1);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2017-07-24 19:22:06.536490','1','root',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(2,'2017-07-24 19:33:37.571082','1','root',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(3,'2017-07-24 19:39:40.970126','1','root',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(4,'2017-07-24 19:45:26.561632','1','root',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(5,'2017-07-24 19:56:46.115343','1','root',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(6,'2017-07-24 20:48:18.195193','2','dima',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',2,1),(7,'2017-07-24 20:48:33.191483','3','awdad',3,'',2,1),(8,'2017-07-24 20:48:33.195487','4','awdad23',3,'',2,1),(9,'2017-07-24 20:49:24.429460','5','aaa',2,'[{\"changed\": {\"fields\": [\"username\"]}}]',2,1),(10,'2017-07-24 20:51:35.441517','5','aaa',3,'',2,1),(11,'2017-07-24 21:18:28.201635','8','qqq',3,'',2,1),(12,'2017-07-24 21:18:28.204639','7','Zzz',3,'',2,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(4,'auth','permission'),(2,'auth','user'),(12,'authtoken','token'),(5,'contenttypes','contenttype'),(11,'restapi','keywords'),(10,'restapi','pages'),(9,'restapi','personpagerank'),(7,'restapi','persons'),(8,'restapi','sites'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-07-22 23:32:37.791057'),(2,'auth','0001_initial','2017-07-22 23:32:38.458630'),(3,'admin','0001_initial','2017-07-22 23:32:38.613706'),(4,'admin','0002_logentry_remove_auto_add','2017-07-22 23:32:38.626718'),(5,'contenttypes','0002_remove_content_type_name','2017-07-22 23:32:38.732794'),(6,'auth','0002_alter_permission_name_max_length','2017-07-22 23:32:38.787174'),(7,'auth','0003_alter_user_email_max_length','2017-07-22 23:32:38.853207'),(8,'auth','0004_alter_user_username_opts','2017-07-22 23:32:38.868130'),(9,'auth','0005_alter_user_last_login_null','2017-07-22 23:32:38.924172'),(10,'auth','0006_require_contenttypes_0002','2017-07-22 23:32:38.929161'),(11,'auth','0007_alter_validators_add_error_messages','2017-07-22 23:32:38.943174'),(12,'auth','0008_alter_user_username_max_length','2017-07-22 23:32:39.019171'),(13,'sessions','0001_initial','2017-07-22 23:32:39.060214'),(14,'restapi','0001_initial','2017-07-23 22:29:39.530944'),(15,'authtoken','0001_initial','2017-07-24 00:32:16.111078'),(16,'authtoken','0002_auto_20160226_1747','2017-07-24 00:32:16.224164'),(17,'restapi','0002_auto_20170728_0058','2017-07-27 21:58:15.705589'),(18,'restapi','0003_persons_user','2017-07-27 23:54:46.746848'),(19,'restapi','0004_auto_20170728_0254','2017-07-27 23:54:46.769871'),(20,'restapi','0005_keywords_userid','2017-07-28 12:41:51.252145'),(21,'restapi','0006_auto_20170728_1617','2017-07-28 13:18:04.970484'),(22,'restapi','0007_auto_20170728_1619','2017-07-28 13:19:33.028033');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('o6wn6vab1ad6yoq54pzn6yg586lcqpzb','OWZmN2M0NWYzYjNiMGI3YTQ2ODZjMzNhMmJkYTNmNzczNTBiZWExYTp7Il9hdXRoX3VzZXJfaGFzaCI6IjBiODdhMjU3YjI2YTUxYTg0MzAxMGZlYzgxOWQ0Mzk2OTQxYjQzNTMiLCJfYXV0aF91c2VyX2lkIjoiMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2017-08-15 16:52:09.429924'),('tw3j9d7fds5hg8g840kvb4v119u7x3zv','ZDAzNjAyMjViNjMxNjdmM2RiYzJhNDBhZTcyYzk3ZDc2NGRlMTVlZDp7Il9hdXRoX3VzZXJfaGFzaCI6IjBiODdhMjU3YjI2YTUxYTg0MzAxMGZlYzgxOWQ0Mzk2OTQxYjQzNTMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2017-08-07 20:51:19.781671');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keywords`
--

DROP TABLE IF EXISTS `keywords`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keywords` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(2048) NOT NULL,
  `PersonID` int(11) NOT NULL,
  `username` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `keywords_PersonID_82615095_fk_persons_ID` (`PersonID`),
  KEY `keywords_username_69f8566e_fk_auth_user_id` (`username`),
  CONSTRAINT `keywords_PersonID_82615095_fk_persons_ID` FOREIGN KEY (`PersonID`) REFERENCES `persons` (`ID`),
  CONSTRAINT `keywords_username_69f8566e_fk_auth_user_id` FOREIGN KEY (`username`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keywords`
--

LOCK TABLES `keywords` WRITE;
/*!40000 ALTER TABLE `keywords` DISABLE KEYS */;
INSERT INTO `keywords` VALUES (3,'afwfwf',2,12),(4,'afwfwf',2,12);
/*!40000 ALTER TABLE `keywords` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pages`
--

DROP TABLE IF EXISTS `pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pages` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Url` varchar(128) NOT NULL,
  `FoundDateTime` datetime(6) NOT NULL,
  `LastScanDate` datetime(6) DEFAULT NULL,
  `SiteID` int(11) NOT NULL,
  `Hash_url` varchar(32) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Hash_url` (`Hash_url`),
  KEY `pages_SiteID_98e9f259_fk_sites_ID` (`SiteID`),
  CONSTRAINT `pages_SiteID_98e9f259_fk_sites_ID` FOREIGN KEY (`SiteID`) REFERENCES `sites` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pages`
--

LOCK TABLES `pages` WRITE;
/*!40000 ALTER TABLE `pages` DISABLE KEYS */;
/*!40000 ALTER TABLE `pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person_page_rank`
--

DROP TABLE IF EXISTS `person_page_rank`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person_page_rank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Rank` int(11) NOT NULL,
  `PageID` int(11) NOT NULL,
  `PersonID` int(11) NOT NULL,
  `Scan_date_datetime` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `person_page_rank_PageID_d0ea7ac6_fk_pages_ID` (`PageID`),
  KEY `person_page_rank_PersonID_e5138c65_fk_persons_ID` (`PersonID`),
  CONSTRAINT `person_page_rank_PageID_d0ea7ac6_fk_pages_ID` FOREIGN KEY (`PageID`) REFERENCES `pages` (`ID`),
  CONSTRAINT `person_page_rank_PersonID_e5138c65_fk_persons_ID` FOREIGN KEY (`PersonID`) REFERENCES `persons` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person_page_rank`
--

LOCK TABLES `person_page_rank` WRITE;
/*!40000 ALTER TABLE `person_page_rank` DISABLE KEYS */;
/*!40000 ALTER TABLE `person_page_rank` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persons`
--

DROP TABLE IF EXISTS `persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `persons` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(2048) NOT NULL,
  `username` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `persons_username_51a96efb` (`username`),
  CONSTRAINT `persons_username_51a96efb_fk_auth_user_id` FOREIGN KEY (`username`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persons`
--

LOCK TABLES `persons` WRITE;
/*!40000 ALTER TABLE `persons` DISABLE KEYS */;
INSERT INTO `persons` VALUES (2,'nikita',1),(3,'nikita',1),(4,'Nik',1),(5,'lol',1),(6,'123',12),(7,'kto-to',12),(8,'Python',2);
/*!40000 ALTER TABLE `persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sites`
--

DROP TABLE IF EXISTS `sites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sites` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(256) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sites`
--

LOCK TABLES `sites` WRITE;
/*!40000 ALTER TABLE `sites` DISABLE KEYS */;
INSERT INTO `sites` VALUES (1,'server.com'),(2,'server2.com');
/*!40000 ALTER TABLE `sites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'webpro'
--

--
-- Dumping routines for database 'webpro'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-08-02 21:26:24
