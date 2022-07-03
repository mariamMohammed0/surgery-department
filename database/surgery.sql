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
INSERT INTO `admins` VALUES (1,'Mariam ','female','2001-10-13',1111087653,'ezzat@gmail.com');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,3,5,'2022-07-07',4,'4pm-5pm'),(2,3,1,'2022-06-22',4,'4pm-5pm'),(3,1,5,'2022-06-23',7,'4pm-5pm'),(4,5,7,'2022-06-17',1,'1pm-2pm'),(5,6,5,'2022-06-23',2,'2pm-3pm');
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
INSERT INTO `doc_schedule` VALUES (1,'3pm-4pm',1),(1,'4pm-5pm',2),(8,'8pm-9pm',3),(8,'9pm-10pm',4),(3,'4pm-5pm',5),(3,'11am-12pm',6),(9,'2pm-3pm',7),(4,'6pm-7pm',8),(5,'4pm-5pm',9),(5,'1pm-2pm',10),(6,'2pm-3pm',11),(7,'5pm-6pm',12);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (1,'Amira mohamed','Female',1002767878,'7','amira@gmail.com','1990-10-15',NULL),(3,'Kareem Ahmed','male',100176864,'4','kareem@gmail.com','1970-06-14','static/uploads/PHOTO-2022-06-07-10-50-40_07_06_2022_12_14_04.jpg'),(5,'Maha ahmed','Female',1009876267,'1','maha@gmail.com','1995-02-09',NULL),(6,'Mayar Ehab','Female',1009876365,'2','mayar@gmail.com','1995-12-29','static/uploads/PHOTO-2022-06-07-10-50-39 2_07_06_2022_13_14_53.jpg'),(7,'Hana ahmed','Female',11198762,'6','hana@gmail.com','1992-09-07',NULL),(8,'Peter hany','male',1111876567,'3','peter@gmail.com','1990-06-14',NULL),(9,'Ahmed mohamed','male',1187656,'5','ahmed@gmail.com','1970-06-23',NULL);
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pat_scans`
--

DROP TABLE IF EXISTS `pat_scans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pat_scans` (
  `PatID` int DEFAULT NULL,
  `scan_path` varchar(255) DEFAULT NULL,
  `comments` varchar(255) DEFAULT NULL,
  `DocID` int DEFAULT NULL,
  KEY `PatID` (`PatID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pat_scans`
--

LOCK TABLES `pat_scans` WRITE;
/*!40000 ALTER TABLE `pat_scans` DISABLE KEYS */;
INSERT INTO `pat_scans` VALUES (5,'static/uploads/IMG_9073_07_06_2022_11_59_06.JPG','',3),(1,'static/uploads/IMG_9074_07_06_2022_12_01_14.JPG','',3),(7,'static/uploads/IMG_9068_07_06_2022_12_42_53.JPG','please reply soon',5);
/*!40000 ALTER TABLE `pat_scans` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'Mariam','Female','2001-01-29',11110876,'wael@hotmail.com','WAEL','static/uploads/IMG_9057_07_06_2022_12_00_29.JPG'),(2,'Maria','Female','2001-10-20',11187654,'mariammohamedezzat2010@gmail.com','EZZAT',NULL),(3,'Ali','Male','1990-06-14',111098765,'ali@hotmail.com','AHMED',NULL),(5,'Hana','Female','2002-06-15',1111098765,'ha@hotmail.com','AHMED','static/uploads/IMG_9055_07_06_2022_11_53_12.JPG'),(6,'Fady','Male','2001-09-08',11199881,'fady@hotmail.com','ALI','static/uploads/IMG_9060_07_06_2022_12_26_03.JPG'),(7,'Maye','Female','2001-10-16',11208897,'maye@hotmail.com','Khaled','static/uploads/IMG_9055_07_06_2022_14_21_32.JPG');
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surgery`
--

LOCK TABLES `surgery` WRITE;
/*!40000 ALTER TABLE `surgery` DISABLE KEYS */;
INSERT INTO `surgery` VALUES (1,'Hernia',25000),(2,'Cardio',30000),(3,'Catarct',4000),(4,'LASIK',777),(5,'PRK',5000),(6,'Glaucoma',20000),(7,'Neuro',15000);
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `surgery_schedule`
--

LOCK TABLES `surgery_schedule` WRITE;
/*!40000 ALTER TABLE `surgery_schedule` DISABLE KEYS */;
INSERT INTO `surgery_schedule` VALUES (1,3,1,'2022-06-17','10:00:00'),(2,5,5,'2022-06-23','10:00:00'),(3,5,7,'2022-06-22','10:00:00'),(4,5,7,'2022-07-19','10:00:00');
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
INSERT INTO `users` VALUES ('ahmed@gmail.com','12345',2),('ali@hotmail.com','12345',1),('amira@gmail.com','12345',2),('ezzat@gmail.com','qwertyu',3),('fady@hotmail.com','12345678',1),('ha@hotmail.com','1234567',1),('hana@gmail.com','12345',2),('ka@hotmail.com','1234567',1),('kareem@gmail.com','1234567',2),('maha@gmail.com','12345',2),('mariammohamedezzat2010@gmail.com','12345',1),('mayar@gmail.com','12345',2),('maye@hotmail.com','12345',1),('peter@gmail.com','12345',2),('wael@hotmail.com','12345',1);
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

-- Dump completed on 2022-07-03 18:11:39
