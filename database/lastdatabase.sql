-- MySQL dump 10.13  Distrib 8.0.29, for macos12 (x86_64)
--
-- Host: localhost    Database: surgery
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admins`
--

DROP TABLE IF EXISTS `admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admins` (
  `AID` int NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Gender` varchar(6) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `Phone` int DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`AID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admins`
--

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;
INSERT INTO `admins` VALUES (1,'azoza','female','2001-10-13',1111087653,'ezzat@gmail.com');
/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `DID` int DEFAULT NULL,
  `PID` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `surgery` int DEFAULT NULL,
  `time` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (10,6,1,'2022-05-18',4,'11am-12pm'),(11,3,1,'2022-06-15',3,'3pm-4pm'),(12,5,1,'2022-06-10',4,'4pm-5pm'),(13,4,2,'2022-07-15',4,'9pm-10pm'),(14,9,2,'2022-06-15',5,'2pm-3pm'),(15,9,1,'2022-06-15',5,'1pm-2pm');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doc_schedule`
--

DROP TABLE IF EXISTS `doc_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doc_schedule` (
  `DID` int DEFAULT NULL,
  `working_times` varchar(45) DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doc_schedule`
--

LOCK TABLES `doc_schedule` WRITE;
/*!40000 ALTER TABLE `doc_schedule` DISABLE KEYS */;
INSERT INTO `doc_schedule` VALUES (3,'3pm-4pm',1),(3,'4pm-5pm',2),(4,'8pm-9pm',3),(4,'9pm-10pm',4),(5,'4pm-5pm',5),(6,'11am-12pm',6),(7,'2pm-3pm',7),(7,'6pm-7pm',8),(8,'4pm-5pm',9),(9,'1pm-2pm',10),(9,'2pm-3pm',11),(10,'5pm-6pm',12);
/*!40000 ALTER TABLE `doc_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `DID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) DEFAULT NULL,
  `gender` varchar(45) DEFAULT NULL,
  `phone` int DEFAULT NULL,
  `Specialization` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`DID`),
  KEY `speciality_idx` (`Specialization`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (4,'Amira','female',456555654,'4','maramiro@gmail.com','2001-10-15',NULL),(5,'samar','female',568787978,'4',NULL,'1970-10-13',NULL),(6,'sami','male',32424443,'4',NULL,'1989-11-01',NULL),(7,'shadi','male',3545454,'5',NULL,'1960-08-19',NULL),(8,'suzan','female',354545555,'6',NULL,'1991-02-13',NULL),(9,'tarek','male',435555,'5',NULL,'1985-08-10',NULL),(10,'menna','female',435008594,'6',NULL,'1949-06-09',NULL),(11,'ahmed','male',1008765439,'6','ahmed@gmail.com','2001-06-03','static/uploads/pexels-simon-robben-614810_04_06_2022_18_47_12.jpg'),(12,'Hisoka','male',12345678,'4','hisoka@gmail.com','2022-05-31','static/uploads/WhatsApp Image 2022-06-04 at 7.41.28 PM_04_06_2022_19_51_06.jpeg');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `PID` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `Gender` varchar(6) DEFAULT NULL,
  `Birthdate` date DEFAULT NULL,
  `Phone` int DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `last_name` varchar(45) DEFAULT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`PID`),
  KEY `email_idx` (`email`),
  CONSTRAINT `email` FOREIGN KEY (`email`) REFERENCES `users` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'mariam','Female','2001-01-29',1111032686,'mariammeccawi@hotmail.com','wael','static/uploads/slides-1_06_06_2022_02_00_42.jpg'),(2,'damed','Male','2002-05-20',1002673869,'dd@hotmail.com','dedi','static/uploads/photo2_04_06_2022_17_24_44.jpg'),(4,'dodo','Male','2003-10-21',1111850989,'dodo@hotmail.com','toto','static/uploads/pexels-andrea-piacquadio-733872_04_06_2022_21_22_50.jpg'),(5,'fofa','Female','2002-02-02',1111987654,'fofe@hotmail.com','fefe',NULL),(8,'Chrollo','Male','2022-05-29',12345678,'chrollo@gmail.com','LUCILFIER','static/uploads/WhatsApp Image 2022-06-04 at 7.43.34 PM_04_06_2022_19_56_09.jpeg');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surgery`
--

DROP TABLE IF EXISTS `surgery`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surgery` (
  `idSurgery` int NOT NULL AUTO_INCREMENT,
  `Surgery_name` varchar(45) DEFAULT NULL,
  `Surgery_cost` int DEFAULT NULL,
  PRIMARY KEY (`idSurgery`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surgery`
--

LOCK TABLES `surgery` WRITE;
/*!40000 ALTER TABLE `surgery` DISABLE KEYS */;
INSERT INTO `surgery` VALUES (3,'catarct',4000),(4,'LASIK',777),(5,'PRK',5000),(6,'Glaucoma surgery',20000);
/*!40000 ALTER TABLE `surgery` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `surgery_schedule`
--

DROP TABLE IF EXISTS `surgery_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `surgery_schedule` (
  `surg_id` int NOT NULL AUTO_INCREMENT,
  `DID` int DEFAULT NULL,
  `PID` int DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time DEFAULT NULL,
  PRIMARY KEY (`surg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surgery_schedule`
--

LOCK TABLES `surgery_schedule` WRITE;
/*!40000 ALTER TABLE `surgery_schedule` DISABLE KEYS */;
INSERT INTO `surgery_schedule` VALUES (1,4,1,'2022-06-08','10:30:00'),(2,4,2,'2022-06-21','12:00:00'),(3,4,2,'2022-06-08','14:00:00'),(4,4,1,'2022-06-08','12:00:00'),(5,4,1,'2022-06-16','10:00:00');
/*!40000 ALTER TABLE `surgery_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `category` int DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('ahmed@gmail.com','123456789',2),('chrollo@gmail.com','qwertyu',1),('dd@hotmail.com','asdfghj',1),('dodo@hotmail.com','mnbvcxz',1),('ezzat@gmail.com','qwertyu',3),('fofe@hotmail.com','lkjhgfd',1),('hisoka@gmail.com','12345678',2),('hsnnsh_gib@hotmail.com','hannah1991',1),('maramiro@gmail.com','0987654',2),('mariammeccawi@hotmail.com','1234567',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-06-06  4:47:25
