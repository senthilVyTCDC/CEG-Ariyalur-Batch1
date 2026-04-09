-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: localhost    Database: creditcardfraud
-- ------------------------------------------------------
-- Server version	8.0.45

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
-- Table structure for table `merchants`
--

DROP TABLE IF EXISTS `merchants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchants` (
  `merchant_id` int DEFAULT NULL,
  `category` text,
  `location` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchants`
--

LOCK TABLES `merchants` WRITE;
/*!40000 ALTER TABLE `merchants` DISABLE KEYS */;
INSERT INTO `merchants` VALUES (2001,'cash','Kolkata'),(2002,'cash','Hyderabad'),(2003,'cash','Kolkata'),(2004,'cash','Mumbai'),(2005,'cash','Hyderabad'),(2006,'cash','Kolkata'),(2007,'cash','Mumbai'),(2008,'cash','Kolkata'),(2009,'cash','Chennai'),(2010,'cash','Hyderabad'),(2011,'food','Bangalore'),(2012,'grocery','Mumbai'),(2013,'fashion','Kolkata'),(2014,'grocery','Delhi'),(2015,'food','Hyderabad'),(2016,'fashion','Mumbai'),(2017,'fashion','Chennai'),(2018,'food','Delhi'),(2019,'grocery','Kolkata'),(2020,'food','Kolkata'),(2021,'grocery','Delhi'),(2022,'food','Mumbai'),(2023,'travel','Mumbai'),(2024,'fashion','Bangalore'),(2025,'food','Chennai'),(2026,'grocery','Delhi'),(2027,'travel','Hyderabad'),(2028,'electronics','Bangalore'),(2029,'grocery','Hyderabad'),(2030,'food','Bangalore'),(2031,'grocery','Mumbai'),(2032,'fashion','Chennai'),(2033,'travel','Hyderabad'),(2034,'grocery','Delhi'),(2035,'electronics','Delhi'),(2036,'electronics','Hyderabad'),(2037,'electronics','Bangalore'),(2038,'electronics','Mumbai'),(2039,'fashion','Hyderabad'),(2040,'fashion','Chennai'),(2041,'grocery','Bangalore'),(2042,'travel','Kolkata'),(2043,'travel','Kolkata'),(2044,'electronics','Hyderabad'),(2045,'travel','Delhi'),(2046,'fashion','Delhi'),(2047,'food','Delhi'),(2048,'grocery','Hyderabad'),(2049,'grocery','Mumbai'),(2050,'grocery','Kolkata');
/*!40000 ALTER TABLE `merchants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-06  1:23:01
