CREATE DATABASE  IF NOT EXISTS `growit` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `growit`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: localhost    Database: growit
-- ------------------------------------------------------
-- Server version	5.7.15

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
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add register',1,'add_register'),(2,'Can change register',1,'change_register'),(3,'Can delete register',1,'delete_register'),(4,'Can add register status',2,'add_registerstatus'),(5,'Can change register status',2,'change_registerstatus'),(6,'Can delete register status',2,'delete_registerstatus'),(7,'Can add email template',3,'add_emailtemplate'),(8,'Can change email template',3,'change_emailtemplate'),(9,'Can delete email template',3,'delete_emailtemplate'),(10,'Can add notification status',4,'add_notificationstatus'),(11,'Can change notification status',4,'change_notificationstatus'),(12,'Can delete notification status',4,'delete_notificationstatus'),(13,'Can add notification type',5,'add_notificationtype'),(14,'Can change notification type',5,'change_notificationtype'),(15,'Can delete notification type',5,'delete_notificationtype'),(16,'Can add notification',6,'add_notification'),(17,'Can change notification',6,'change_notification'),(18,'Can delete notification',6,'delete_notification'),(19,'Can add role',7,'add_role'),(20,'Can change role',7,'change_role'),(21,'Can delete role',7,'delete_role'),(22,'Can add user status',8,'add_userstatus'),(23,'Can change user status',8,'change_userstatus'),(24,'Can delete user status',8,'delete_userstatus'),(25,'Can add email address',9,'add_emailaddress'),(26,'Can change email address',9,'change_emailaddress'),(27,'Can delete email address',9,'delete_emailaddress'),(28,'Can add email address status',10,'add_emailaddressstatus'),(29,'Can change email address status',10,'change_emailaddressstatus'),(30,'Can delete email address status',10,'delete_emailaddressstatus'),(31,'Can add login status',11,'add_loginstatus'),(32,'Can change login status',11,'change_loginstatus'),(33,'Can delete login status',11,'delete_loginstatus'),(34,'Can add name',12,'add_name'),(35,'Can change name',12,'change_name'),(36,'Can delete name',12,'delete_name'),(37,'Can add name type',13,'add_nametype'),(38,'Can change name type',13,'change_nametype'),(39,'Can delete name type',13,'delete_nametype'),(40,'Can add password status',14,'add_passwordstatus'),(41,'Can change password status',14,'change_passwordstatus'),(42,'Can delete password status',14,'delete_passwordstatus'),(43,'Can add password reset',15,'add_passwordreset'),(44,'Can change password reset',15,'change_passwordreset'),(45,'Can delete password reset',15,'delete_passwordreset'),(46,'Can add password reset status',16,'add_passwordresetstatus'),(47,'Can change password reset status',16,'change_passwordresetstatus'),(48,'Can delete password reset status',16,'delete_passwordresetstatus'),(49,'Can add custom user',17,'add_customuser'),(50,'Can change custom user',17,'change_customuser'),(51,'Can delete custom user',17,'delete_customuser'),(52,'Can add user login',18,'add_userlogin'),(53,'Can change user login',18,'change_userlogin'),(54,'Can delete user login',18,'delete_userlogin'),(55,'Can add Token',19,'add_token'),(56,'Can change Token',19,'change_token'),(57,'Can delete Token',19,'delete_token'),(58,'Can add log entry',20,'add_logentry'),(59,'Can change log entry',20,'change_logentry'),(60,'Can delete log entry',20,'delete_logentry'),(61,'Can add permission',21,'add_permission'),(62,'Can change permission',21,'change_permission'),(63,'Can delete permission',21,'delete_permission'),(64,'Can add group',22,'add_group'),(65,'Can change group',22,'change_group'),(66,'Can delete group',22,'delete_group'),(67,'Can add content type',23,'add_contenttype'),(68,'Can change content type',23,'change_contenttype'),(69,'Can delete content type',23,'delete_contenttype'),(70,'Can add session',24,'add_session'),(71,'Can change session',24,'change_session'),(72,'Can delete session',24,'delete_session');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-12 14:45:27
