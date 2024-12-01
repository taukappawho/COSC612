-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Dec 01, 2024 at 06:13 PM
-- Server version: 10.11.10-MariaDB
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
(95, 'italian seasoned breadcrumbs', 1),
(97, 'pork tenderloin', 1),
(98, 'fresh sage', 1),
(99, 'prosciutto', 1),
(100, 'condensed cream of mushroom soup', 1),
(101, 'frozen tater tots', 1),
(135, 'english mufiin', 1),
(136, 'marinara', 1),
(137, 'mozzarella', 1),
(148, 'salmon', 0),
(149, 'light brown sugar', 0),
(150, 'dijon mustard', 0),
(151, 'old bay', 1),
(152, 'ribeye', 1);

-- --------------------------------------------------------

--
-- Table structure for table `recipe`
--

CREATE TABLE `recipe` (
  `id` int(11) NOT NULL,
  `name` varchar(45) NOT NULL,
  `viewable` int(11) NOT NULL DEFAULT 0,
  `creator` int(10) UNSIGNED NOT NULL,
  `instructions` varchar(2000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `recipe`
--

INSERT INTO `recipe` (`id`, `name`, `viewable`, `creator`, `instructions`) VALUES
(2, 'peach cobbler', 1, 6, 'Combine peaches and sugar in a medium bowl. Stir well and let stand for 5 minutes.\r\n\r\nLiberally spray a slow cooker with cooking spray.\r\n\r\nStir peaches once more and add to the prepared slow cooker. Sprinkle cake mix evenly over the peaches; don\'t stir. Distribute butter pieces evenly over cake mix.\r\n\r\nCover and cook on High until cake is golden and bubbly around the edges, about 3Â½ hours. Turn off slow cooker and let stand 15 minutes before serving.'),
(3, 'Air Fryer Quesadillas', 1, 13, 'Heat tortillas in the microwave until pliable, about 15 seconds.\r\n\r\nPlace 1/4 cup cheese on one half of each tortilla; fold other half of tortilla over cheese. Place in  air fryer. Spray with non-stick cooking spray. \r\n\r\nSet temperature to 375 degrees F (190 degrees C). Place quesadillas in the basket of the air fryer, and cook until golden brown, 4 to 6 minutes. Flip quesadillas, press down with a spatula, and air fry an additional 2 to 3 minutes.'),
(4, '3-ingredient baked pork chops', 1, 1, 'Preheat the oven to 400 degrees F (200 degrees C). Whisk eggs in a shallow dish. Sprinkle pork chops with salt and pepper, if desired. Dip pork chops in eggs, and allow excess to drip off. Coat pork chops in breadcrumbs.\r\n\r\nPlace pork chops on a baking rack lightly coated with cooking spray; set rack in a rimmed baking sheet.\r\n\r\nBake in the preheated oven until a thermometer inserted in thickest portion registers 145 degrees F (63 degrees C), 20 to 25 minutes. Let rest 5 minutes before serving.'),
(5, 'Prosciutto-Wrapped Pork Tenderloin with Crisp', 1, 6, 'Preheat oven to 350 degrees F (175 degrees C).\r\n\r\nLightly season pork with salt and black pepper. Arrange about 6 sage leaves over tenderloin. Wrap prosciutto around tenderloin and sage, overlapping prosciutto slightly; wrap in plastic wrap and refrigerate to allow prosciutto to set on pork tenderloin, 5 to 10 minutes. Remove plastic wrap.\r\n\r\nHeat olive oil in a skillet over medium heat. Fry wrapped tenderloin in the hot oil until prosciutto is crispy and lightly browned on all sides, 8 to 10 minutes. Transfer wrapped tenderloin to a baking dish, reserving oil in the skillet.\r\n\r\nBake tenderloin in the preheated oven until pork is cooked through, about 20 minutes. An instant-read thermometer inserted into the center should read at least 145 degrees F (63 degrees C).\r\n\r\nHeat reserved oil in the skillet over medium heat; fry remaining sage leaves until crispy, adding more oil as needed, about 5 minutes.\r\n\r\nSlice tenderloin and serve with crispy sage leaves.'),
(6, 'Tater Tot Casserole', 1, 1, 'Here\'s a very brief overview of what you can expect when you make tater tot casserole at home:\r\n\r\n1. Cook the ground beef, then stir in the soup and seasonings.\r\n2. Transfer the beef to a baking dish. Top with tater tots, then the cheese.\r\n3. Bake until the tots are golden brown.'),
(54, 'English Muffin Pizza Snacks', 0, 13, 'Heat oven to 400°F. Place muffin halves cut-side-up on a parchment-lined baking sheet; brush muffin halves generously with butter.\r\n\r\nBake until lightly toasted, about 10 minutes.\r\n\r\nLayer on marinara and mozzarella and bake until melted, 6 to 8 minutes.\r\n\r\nSprinkle on some sea salt and dried oregano and basil leaves before serving.'),
(56, 'Salmon with Brown Sugar Glaze', 0, 13, 'Preheat the oven broiler and set an oven rack about 6 inches from the heat source. Grease the rack of a broiler pan with cooking spray.\r\n\r\nSeason salmon with salt and pepper, then place on the prepared broiler pan. Whisk together brown sugar and mustard in a small bowl; spoon mixture evenly over salmon.\r\n\r\nCook under the preheated broiler until fish flakes easily with a fork, 10 to 15 minutes.'),
(57, 'Pesto Cheesy Chicken Rolls', 0, 13, 'Preheat the oven to 350 degrees F (175 degrees C). Spray a baking dish with cooking spray.\r\n\r\nSpread 2 to 3 tablespoons of the pesto sauce onto each flattened chicken breast. Place one slice of cheese over the pesto. Roll up tightly, and secure with toothpicks. Place in a lightly greased baking dish.\r\n\r\nBake uncovered for 45 to 50 minutes in the preheated oven, until chicken is nicely browned and juices run clear.');

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
(5, 97, 1, 9),
(5, 98, 1, 2),
(5, 99, 5, 4),
(6, 1, 1, 1),
(6, 2, 1, 1),
(6, 15, 0.5, 9),
(6, 92, 0.75, 9),
(6, 100, 1, 11),
(6, 101, 2, 9),
(54, 1, 1, 1),
(54, 39, 1, 2),
(54, 48, 1, 1),
(54, 53, 1, 5),
(54, 135, 1, 0),
(54, 136, 2, 6),
(54, 137, 2, 0),
(56, 1, 1, 1),
(56, 2, 2, 1),
(56, 93, 1, 1),
(56, 148, 24, 4),
(56, 149, 0.25, 7),
(56, 150, 2, 6),
(57, 39, 1, 2),
(57, 65, 4, 11),
(57, 93, 1, 1),
(57, 137, 4, 0);

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
('James', '$argon2id$v=19$m=65536,t=3,p=4$DeEcQ0iJ0XoPQYgxRmjt/Q$yLUj1QkDCsBytqNnB3jZmEBNB8xneyGuLrYCU9kscgw', 'jnauro1@students.towson.edu', 2, 1, 'N'),
('John', 'abc123', 'etaylor5@students.towson.edu', 2, 2, 'N'),
('James1', '$argon2id$v=19$m=65536,t=3,p=4$L0XoHWOMEWKM0ZpTCuG8lw$QhURmet+qkSHU4Eq3K6gTivTb3x8ln36888iuzEgUNc', 'naurotj@gmail.com1', 2, 6, 'N'),
(' Bhuvan', '$argon2id$v=19$m=65536,t=3,p=4$Y0zJmbPW2lvrvde6977Xug$gf2pd246R6JSYsYM6D/1C7GEs/6MeIqaGyR0Y/ohFCU', 'bhuvansaireddyseelam@gmail.com', 1, 8, 'N'),
('James0', '$argon2id$v=19$m=65536,t=3,p=4$JUSoVUppzXkvZWxtrdVaKw$rJuhMB77afM8SWvEM5r4srF8WI1mcww3FtPWVVG4byA', 'naurotj@gmail.com', 1, 13, 'N');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=153;

--
-- AUTO_INCREMENT for table `recipe`
--
ALTER TABLE `recipe`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

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
