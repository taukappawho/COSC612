CREATE DATABASE  IF NOT EXISTS `recipes` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `recipes`;
-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: recipes
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `ingredients`
--

DROP TABLE IF EXISTS `ingredients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredients` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredients`
--

LOCK TABLES `ingredients` WRITE;
/*!40000 ALTER TABLE `ingredients` DISABLE KEYS */;
INSERT INTO `ingredients` VALUES (1,'salt'),(2,'pepper'),(3,'cayenne'),(4,'vanilla beans'),(5,'vanilla extract'),(6,'peppercorns'),(7,'oats'),(8,'milk'),(9,'water'),(10,'rice'),(11,'pinto beans'),(12,'olive oil'),(13,'vegetable oil'),(14,'canola oil'),(15,'ground beef'),(16,'chicken stock'),(17,'beef stock'),(18,'vegetable stock'),(19,'tomato sauce'),(20,'tomato paste'),(21,'marinara sauce'),(22,'kidney beans'),(23,'spaghetti'),(24,'linguine'),(25,'penne'),(26,'lentils'),(27,'split peas'),(28,'bread crumbs'),(29,'potato'),(30,'carrot'),(31,'celery'),(32,'onion'),(33,'garlic'),(34,'vinegar'),(35,'soy sauce'),(36,'worcestshire sauce'),(37,'hot sauce'),(38,'dried basil'),(39,'basil'),(40,'bay leaves'),(41,'crushed red pepper flakes'),(42,'curry powder'),(43,'chili powder'),(44,'cumin'),(45,'cinnamon'),(46,'garlic powder'),(47,'onion powder'),(48,'oregeno'),(49,'paprika'),(50,'parsley'),(51,'dried parsley'),(52,'eggs'),(53,'butter'),(54,'ketchup'),(55,'mustard'),(56,'mayonnaise'),(57,'parmesan cheese'),(58,'cheddar cheese'),(59,'american cheese'),(60,'colby cheese'),(61,'bleu cheese'),(62,'swiss cheese'),(63,'corn'),(64,'spinach'),(65,'chicken breasts'),(66,'lemons'),(67,'fresh ginger'),(68,'shallots'),(69,'capers'),(70,'canned chiles'),(71,'prepared horseradish'),(72,'anchovy paste'),(73,'almond extract'),(74,'kosher salt'),(75,'cornstarch'),(76,'confectioner\'s sugar'),(77,'sugar'),(78,'honey'),(79,'brown sugar'),(80,'flour'),(81,'buttermilk'),(82,'whole milk'),(83,'nutmeg'),(84,'challah'),(85,'powdered sugar'),(86,'maple sugar'),(87,'banana');
/*!40000 ALTER TABLE `ingredients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe`
--

DROP TABLE IF EXISTS `recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `viewable` int NOT NULL DEFAULT '0',
  `creator` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `creator_idx` (`creator`),
  CONSTRAINT `creator` FOREIGN KEY (`creator`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe`
--

LOCK TABLES `recipe` WRITE;
/*!40000 ALTER TABLE `recipe` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recipe_ing`
--

DROP TABLE IF EXISTS `recipe_ing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recipe_ing` (
  `recipe_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `quantity` float unsigned NOT NULL DEFAULT '0',
  `units` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`recipe_id`,`ingredient_id`),
  KEY `ingredient_id_idx` (`ingredient_id`),
  CONSTRAINT `ingredient_id` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`),
  CONSTRAINT `recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recipe_ing`
--

LOCK TABLES `recipe_ing` WRITE;
/*!40000 ALTER TABLE `recipe_ing` DISABLE KEYS */;
/*!40000 ALTER TABLE `recipe_ing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `name` varchar(20) NOT NULL,
  `password` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `auth` int unsigned NOT NULL DEFAULT '0',
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('James','xyzzy','jnauro1@students.towson.edu',1,1),('John','abc123','etaylor5@students.towson.edu',1,2);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-20  5:24:20
