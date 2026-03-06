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
-- Table structure for table `merchant`
--

DROP TABLE IF EXISTS `merchant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `merchant` (
  `merchant_id` int NOT NULL AUTO_INCREMENT,
  `merchant_name` varchar(100) NOT NULL,
  `category` varchar(50) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`merchant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `merchant`
--

LOCK TABLES `merchant` WRITE;
/*!40000 ALTER TABLE `merchant` DISABLE KEYS */;
INSERT INTO `merchant` VALUES (1,'Stewart, Fisher and Walker','Grocery','Maysland'),(2,'Kelly, Middleton and Middleton','Clothing','Lake Samuelstad'),(3,'Collins-Smith','Travel','North Jamesshire'),(4,'Matthews-Stewart','Electronics','Guerraland'),(5,'Bowers Ltd','Grocery','Warnertown'),(6,'Davis-Wong','Electronics','Bryantview'),(7,'Oneal, Williams and Santiago','Travel','Pamelaport'),(8,'Atkins-Bryant','Food','New Joelstad'),(9,'Smith, Robles and Horn','Grocery','Seanhaven'),(10,'Snyder, Sosa and Andrade','Grocery','Mcconnellland'),(11,'Padilla, Armstrong and Allison','Clothing','Williamsville'),(12,'Rodriguez Ltd','Travel','West Taylor'),(13,'Yates Inc','Travel','West Davidview'),(14,'Freeman-Kennedy','Electronics','Rachelville'),(15,'Ramsey Ltd','Clothing','Bonillaland'),(16,'Johnson-Spencer','Clothing','Hollystad'),(17,'Evans-Brown','Travel','Bradleystad'),(18,'Hensley LLC','Travel','Popeberg'),(19,'Holder PLC','Clothing','Lake Matthewview'),(20,'Kirk-Villanueva','Travel','Lake Saraville'),(21,'Mckenzie-Oconnor','Grocery','New Paula'),(22,'Lin, Wall and Bartlett','Grocery','East Amanda'),(23,'Cruz LLC','Clothing','Lake Heather'),(24,'Long-Morris','Travel','Lake Elizabeth'),(25,'Ruiz PLC','Grocery','Courtneyfurt'),(26,'Morrison PLC','Clothing','North Jasonhaven'),(27,'Ortiz LLC','Food','Richardburgh'),(28,'Robinson-Miranda','Food','Katherineburgh'),(29,'Washington PLC','Clothing','Laurashire'),(30,'Andrade-Bishop','Grocery','North Melissa'),(31,'Leon, Wiggins and Reyes','Electronics','New Jacquelinemouth'),(32,'Fuentes-Wright','Electronics','West Trevorburgh'),(33,'Freeman Group','Food','New Ericland'),(34,'Lyons-Smith','Food','Thompsontown'),(35,'Mcclain PLC','Food','Hillville'),(36,'Hamilton-Stewart','Food','Deborahborough'),(37,'Miller, Hoover and Palmer','Travel','Lake Joelberg'),(38,'Ochoa Ltd','Travel','Port Katherinefurt'),(39,'Young Ltd','Grocery','New Juliafurt'),(40,'Lewis, Long and Montgomery','Electronics','South Joanna'),(41,'Thompson, Martinez and Arias','Clothing','Nicholasburgh'),(42,'Cabrera LLC','Travel','Lake Karen'),(43,'Pollard-Powell','Clothing','South Jennifer'),(44,'Fritz-Anderson','Electronics','West Philliptown'),(45,'Rodriguez Group','Clothing','Josephport'),(46,'Guzman, Jimenez and Moore','Food','Danielfort'),(47,'Clark LLC','Electronics','Lake Jeffrey'),(48,'Drake Group','Clothing','Jamesburgh'),(49,'Fernandez Inc','Food','Wallaceview'),(50,'Watkins-Smith','Travel','Bradleystad'),(51,'Ford-Patel','Travel','Lake Deborahbury'),(52,'Miller Ltd','Electronics','Williamsmouth'),(53,'Lee PLC','Electronics','Holmesland'),(54,'Reynolds Group','Food','Ritterborough'),(55,'Turner-Ware','Electronics','East Dianeville'),(56,'Green, Maxwell and Foster','Food','Huntstad'),(57,'Rice Ltd','Grocery','Nguyenton'),(58,'Farrell and Sons','Clothing','Anneside'),(59,'Baker, Robinson and Jones','Electronics','Ellisshire'),(60,'Perez-Ortiz','Food','Johnfurt'),(61,'Wells, Orozco and Shaw','Clothing','North Jose'),(62,'Martinez LLC','Travel','Cannonville'),(63,'Norton, Sanchez and Murray','Food','Douglasfurt'),(64,'Lee, Parks and Howard','Food','Brianstad'),(65,'Grimes PLC','Grocery','Deannachester'),(66,'Soto-Freeman','Grocery','Lake James'),(67,'Duncan-Ballard','Clothing','East Deborahhaven'),(68,'Singleton, Palmer and David','Clothing','Watsonmouth'),(69,'Zimmerman-Freeman','Electronics','Smithshire'),(70,'Hart and Sons','Clothing','Guerreroville'),(71,'Jones LLC','Grocery','Conleyshire'),(72,'Bowers-Herrera','Grocery','Smithland'),(73,'Kennedy-Randall','Grocery','Dominguezchester'),(74,'Gordon Ltd','Travel','Lake Traceyhaven'),(75,'Nelson LLC','Travel','New Patriciaburgh'),(76,'Ortiz-Burns','Grocery','Barnesshire'),(77,'Hoover Group','Grocery','Christopherport'),(78,'Washington PLC','Electronics','Ericafurt'),(79,'Holloway-Mccormick','Food','West Thomasberg'),(80,'Gray-Ward','Travel','Port David'),(81,'Mclean, Gilmore and Henderson','Travel','East Ravenport'),(82,'Hatfield-Nielsen','Travel','Swansonshire'),(83,'Campbell-Beck','Clothing','Clarkberg'),(84,'Kennedy Inc','Grocery','Phillipborough'),(85,'Knight-Stephens','Food','Kevinstad'),(86,'Navarro-Liu','Electronics','Port Adamtown'),(87,'Murray-Jenkins','Travel','West Martin'),(88,'Carrillo-Wright','Travel','Campbellville'),(89,'Barnett-Tucker','Electronics','Matthewstad'),(90,'Brown-Bailey','Food','Harrisshire'),(91,'Young and Sons','Travel','Riverahaven'),(92,'Rice, Romero and Lopez','Electronics','Dustinton'),(93,'Soto PLC','Travel','Livingstonport'),(94,'Powell, Moreno and Walsh','Food','Arianashire'),(95,'Alvarez-Wallace','Food','East Tiffanystad'),(96,'Holloway-Fisher','Clothing','Juliemouth'),(97,'Smith-Martinez','Food','Jamieton'),(98,'Gordon-Porter','Travel','West Anna'),(99,'Hart-Blair','Travel','Lake Jennifermouth'),(100,'Mitchell Group','Grocery','East Michaelstad');
/*!40000 ALTER TABLE `merchant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-25 11:58:47
