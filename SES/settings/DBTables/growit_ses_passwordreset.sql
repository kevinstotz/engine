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
-- Table structure for table `ses_passwordreset`
--

DROP TABLE IF EXISTS `ses_passwordreset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ses_passwordreset` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Authorization_Code` varchar(20) NOT NULL,
  `Inserted` datetime(6) NOT NULL,
  `Status_Id_id` int(11) NOT NULL,
  `User_Id_id` int(11) NOT NULL,
  `Clicked` datetime(6) NOT NULL,
  PRIMARY KEY (`Id`),
  KEY `SES_passwordreset_Status_Id_id_a11d1772_fk_SES_passw` (`Status_Id_id`),
  KEY `SES_passwordreset_User_Id_id_aef51cff_fk_SES_customuser_Id` (`User_Id_id`),
  CONSTRAINT `SES_passwordreset_Status_Id_id_a11d1772_fk_SES_passw` FOREIGN KEY (`Status_Id_id`) REFERENCES `ses_passwordresetstatus` (`Id`),
  CONSTRAINT `SES_passwordreset_User_Id_id_aef51cff_fk_SES_customuser_Id` FOREIGN KEY (`User_Id_id`) REFERENCES `ses_customuser` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ses_passwordreset`
--

LOCK TABLES `ses_passwordreset` WRITE;
/*!40000 ALTER TABLE `ses_passwordreset` DISABLE KEYS */;
/*!40000 ALTER TABLE `ses_passwordreset` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-12 14:47:08
