-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 04, 2024 at 11:31 AM
-- Server version: 10.11.9-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `u882885499_recipes`
--

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `usable` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `usable`) VALUES
(1, 'salt', 1),
(2, 'pepper', 1),
(3, 'cayenne', 1),
(4, 'vanilla beans', 1),
(5, 'vanilla extract', 1),
(6, 'peppercorns', 1),
(7, 'oats', 1),
(8, 'milk', 1),
(9, 'water', 1),
(10, 'rice', 1),
(11, 'pinto beans', 1),
(12, 'olive oil', 1),
(13, 'vegetable oil', 1),
(14, 'canola oil', 1),
(15, 'ground beef', 1),
(16, 'chicken stock', 1),
(17, 'beef stock', 1),
(18, 'vegetable stock', 1),
(19, 'tomato sauce', 1),
(20, 'tomato paste', 1),
(21, 'marinara sauce', 1),
(22, 'kidney beans', 1),
(23, 'spaghetti', 1),
(24, 'linguine', 1),
(25, 'penne', 1),
(26, 'lentils', 1),
(27, 'split peas', 1),
(28, 'bread crumbs', 1),
(29, 'potato', 1),
(30, 'carrot', 1),
(31, 'celery', 1),
(32, 'onion', 1),
(33, 'garlic', 1),
(34, 'vinegar', 1),
(35, 'soy sauce', 1),
(36, 'worcestshire sauce', 1),
(37, 'hot sauce', 1),
(38, 'dried basil', 1),
(39, 'basil', 1),
(40, 'bay leaves', 1),
(41, 'crushed red pepper flakes', 1),
(42, 'curry powder', 1),
(43, 'chili powder', 1),
(44, 'cumin', 1),
(45, 'cinnamon', 1),
(46, 'garlic powder', 1),
(47, 'onion powder', 1),
(48, 'oregeno', 1),
(49, 'paprika', 1),
(50, 'parsley', 1),
(51, 'dried parsley', 1),
(52, 'eggs', 1),
(53, 'butter', 1),
(54, 'ketchup', 1),
(55, 'mustard', 1),
(56, 'mayonnaise', 1),
(57, 'parmesan cheese', 1),
(58, 'cheddar cheese', 1),
(59, 'american cheese', 1),
(60, 'colby cheese', 1),
(61, 'bleu cheese', 1),
(62, 'swiss cheese', 1),
(63, 'corn', 1),
(64, 'spinach', 1),
(65, 'chicken breasts', 1),
(66, 'lemons', 1),
(67, 'fresh ginger', 1),
(68, 'shallots', 1),
(69, 'capers', 1),
(70, 'canned chiles', 1),
(71, 'prepared horseradish', 1),
(72, 'anchovy paste', 1),
(73, 'almond extract', 1),
(74, 'kosher salt', 1),
(75, 'cornstarch', 1),
(76, 'confectioner\'s sugar', 1),
(77, 'sugar', 1),
(78, 'honey', 1),
(79, 'brown sugar', 1),
(80, 'flour', 1),
(81, 'buttermilk', 1),
(82, 'whole milk', 1),
(83, 'nutmeg', 1),
(84, 'challah', 1),
(85, 'powdered sugar', 1),
(86, 'maple sugar', 1),
(87, 'banana', 1),
(89, 'peaches', 1),
(90, 'white cake mix', 1),
(91, 'tortillas', 1),
(92, 'shredded cheese', 1),
(93, 'cooking spray', 1),
(94, 'center cut pork chops', 1),
(95, 'Italian seasoned breadcrumbs', 1),
(97, 'pork tenderloin', 1),
(98, 'fresh sage', 1),
(99, 'prosciutto', 1),
(100, 'condensed cream of mushroom soup', 1),
(101, 'frozen tater tots', 1);

-- --------------------------------------------------------

--
-- Table structure for table `recipe`
--

CREATE TABLE `recipe` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `viewable` int(11) NOT NULL DEFAULT 0,
  `creator` int(10) UNSIGNED NOT NULL,
  `image` varchar(32) NOT NULL,
  `instructions` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipe`
--

INSERT INTO `recipe` (`id`, `name`, `viewable`, `creator`, `image`, `instructions`) VALUES
(2, 'peach cobbler', 1, 6, 'image_2.png', 'instructions_2.txt'),
(3, 'Air Fryer Quesadillas', 0, 6, 'image_3.png', 'instructions_3.txt'),
(4, '3-ingredient baked pork chops', 1, 1, 'image_4.png', 'instructions_4.txt'),
(5, 'Prosciutto-Wrapped Pork Tenderloin with Crisp', 1, 6, 'image_5.png', 'instructions_5.txt'),
(6, 'Tater Tot Casserole', 1, 1, 'image_6.png', 'instructions_6.txt');

-- --------------------------------------------------------

--
-- Table structure for table `recipe_ing`
--

CREATE TABLE `recipe_ing` (
  `recipe_id` int(11) NOT NULL,
  `ingredient_id` int(11) NOT NULL,
  `quantity` float UNSIGNED NOT NULL DEFAULT 0,
  `units` int(10) UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipe_ing`
--

INSERT INTO `recipe_ing` (`recipe_id`, `ingredient_id`, `quantity`, `units`) VALUES
(2, 53, 0.5, 7),
(2, 77, 0.5, 7),
(2, 89, 8, 7),
(2, 90, 15.25, 4),
(2, 93, 0, 11),
(3, 91, 2, 11),
(3, 92, 0.5, 7),
(3, 93, 0, 11),
(4, 1, 1, 1),
(4, 2, 1, 1),
(4, 52, 2, 11),
(4, 93, 0, 11),
(4, 94, 24, 4),
(4, 95, 1, 7),
(5, 1, 1, 1),
(5, 2, 1, 1),
(5, 12, 1, 6),
(5, 97, 1, 10),
(5, 98, 1, 2),
(5, 99, 5, 4),
(6, 1, 1, 1),
(6, 2, 1, 1),
(6, 15, 0.5, 10),
(6, 92, 0.75, 10),
(6, 100, 1, 11),
(6, 101, 2, 10);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `name` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(45) NOT NULL,
  `auth` int(10) UNSIGNED NOT NULL DEFAULT 0,
  `id` int(10) UNSIGNED NOT NULL,
  `uuid` varchar(32) NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`name`, `password`, `email`, `auth`, `id`, `uuid`) VALUES
('James', '$argon2id$v=19$m=65536,t=3,p=4$DeEcQ0iJ0XoPQYgxRmjt/Q$yLUj1QkDCsBytqNnB3jZmEBNB8xneyGuLrYCU9kscgw', 'jnauro1@students.towson.edu', 1, 1, 'N'),
('John', 'abc123', 'etaylor5@students.towson.edu', 1, 2, 'N'),
('James1', '$argon2id$v=19$m=65536,t=3,p=4$L0XoHWOMEWKM0ZpTCuG8lw$QhURmet+qkSHU4Eq3K6gTivTb3x8ln36888iuzEgUNc', 'naurotj@gmail.com', 1, 6, 'N');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `recipe`
--
ALTER TABLE `recipe`
  ADD PRIMARY KEY (`id`),
  ADD KEY `creator_idx` (`creator`);

--
-- Indexes for table `recipe_ing`
--
ALTER TABLE `recipe_ing`
  ADD PRIMARY KEY (`recipe_id`,`ingredient_id`),
  ADD KEY `ingredient_id_idx` (`ingredient_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `recipe`
--
ALTER TABLE `recipe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `recipe`
--
ALTER TABLE `recipe`
  ADD CONSTRAINT `creator` FOREIGN KEY (`creator`) REFERENCES `user` (`id`);

--
-- Constraints for table `recipe_ing`
--
ALTER TABLE `recipe_ing`
  ADD CONSTRAINT `ingredient_id` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`),
  ADD CONSTRAINT `recipe_id` FOREIGN KEY (`recipe_id`) REFERENCES `recipe` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
