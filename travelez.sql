-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2024 at 10:55 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `travelez`
--

-- --------------------------------------------------------

--
-- Table structure for table `destinations`
--

CREATE TABLE `destinations` (
  `destination_id` int(11) NOT NULL,
  `destination_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `destinations`
--

INSERT INTO `destinations` (`destination_id`, `destination_name`) VALUES
(1, 'Ahangama'),
(2, 'Ambalangoda'),
(3, 'Ampara'),
(4, 'Anuradhapura'),
(5, 'ArugamBay'),
(6, 'Bentota'),
(7, 'Beruwala'),
(8, 'Colombo'),
(9, 'Deniyaya'),
(10, 'Ella'),
(11, 'Embilipitiya'),
(12, 'Galle'),
(13, 'Habarana'),
(14, 'Haputale'),
(15, 'Hikkaduwa'),
(16, 'Jaffna'),
(17, 'Kalametiya'),
(18, 'Kalkudah'),
(19, 'Kalutara'),
(20, 'Kandy'),
(21, 'Katukitula'),
(22, 'Koslanda'),
(23, 'Mirissa'),
(24, 'Negombo'),
(25, 'Nilaveli'),
(26, 'NuwaraEliya'),
(27, 'Peradeniya'),
(28, 'Pinnawala'),
(29, 'Polonnaruwa'),
(30, 'Pussellawa'),
(31, 'Saliyapura'),
(32, 'Sigiriya'),
(33, 'Tissamaharama'),
(34, 'Trincomalee'),
(35, 'Unawatuna'),
(36, 'Weligatta');

-- --------------------------------------------------------

--
-- Table structure for table `profile_review`
--

CREATE TABLE `profile_review` (
  `review_id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `destination` varchar(50) DEFAULT NULL,
  `review` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `profile_review`
--

INSERT INTO `profile_review` (`review_id`, `username`, `destination`, `review`) VALUES
(1, 'liams', 'Ahangama', 'Ahangama is a beautiful coastal town with stunning beaches and great surf spots. The locals are friendly, and the food is amazing.'),
(2, 'emmaj', 'Ambalangoda', 'Ambalangoda is famous for its traditional mask-making industry. The town has a rich cultural heritage and vibrant markets.'),
(3, 'noahw', 'Ampara', 'Ampara is a peaceful and scenic destination, perfect for nature lovers. The wildlife sanctuaries and national parks are must-visit attractions.'),
(4, 'isabellab', 'Anuradhapura', 'Anuradhapura is a UNESCO World Heritage site known for its ancient ruins and sacred Buddhist sites. The historical significance of this city is awe-inspiring.'),
(5, 'williamj', 'ArugamBay', 'Arugam Bay is a paradise for surfers, with some of the best waves in the world. The laid-back vibe and stunning sunsets make it a must-visit destination.'),
(6, 'jamesm', 'Beruwala', 'Beruwala is a charming coastal town with golden sandy beaches and clear blue waters. The seafood here is delicious, and the sunsets are breathtaking.'),
(7, 'charlottey', 'Colombo', 'Colombo is the vibrant capital city of Sri Lanka, offering a mix of modern amenities and cultural attractions. From bustling markets to historic landmarks, theres always something to explore.'),
(8, 'tharusha', 'Ella', 'Ella is a picturesque hill station surrounded by tea plantations and misty mountains. The views from Ella Rock and Little Adams Peak are simply breathtaking.'),
(9, 'danielc', 'Embilipitiya', 'Embilipitiya is a quaint town located on the banks of the Walawe River. Its a great base for exploring nearby national parks like Udawalawe and Yala.'),
(10, 'oliviarod', 'Galle', 'Galle is a charming coastal city with a rich colonial history. The UNESCO-listed Galle Fort is a major attraction, offering stunning views of the ocean and historic architecture.'),
(11, 'ethan123', 'Habarana', 'Habarana is a gateway to Sri Lanka\'s cultural triangle, with easy access to ancient cities like Sigiriya and Polonnaruwa. The area is also known for its wildlife safaris and birdwatching.'),
(12, 'avag', 'Haputale', 'Haputale is a hill station nestled amidst misty mountains and lush tea estates. The scenic train ride from Haputale to Ella is a must-do experience for nature lovers.'),
(13, 'loganp', 'Hikkaduwa', 'Hikkaduwa is a vibrant beach town known for its coral reefs and vibrant marine life. It\'s a paradise for snorkeling and diving enthusiasts.'),
(14, 'miat', 'Jaffna', 'Jaffna is a cultural melting pot with a rich history and heritage. The Jaffna Fort and Nallur Kandaswamy Temple are must-visit attractions.'),
(15, 'johndoe123', 'Kalametiya', 'Kalametiya is a coastal sanctuary renowned for its birdlife and mangrove forests. It\'s a peaceful retreat away from the hustle and bustle of city life.'),
(16, 'emilysmith23', 'Kalkudah', 'Kalkudah is a hidden gem on Sri Lanka\'s east coast, known for its pristine beaches and crystal-clear waters. It\'s perfect for a relaxing beach getaway.'),
(19, 'mariag', 'Katukitula', 'Katukitula is a tranquil village surrounded by scenic landscapes and tea estates. It\'s a great place to experience the authentic charm of rural Sri Lanka.');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `firstName` varchar(50) DEFAULT NULL,
  `lastName` varchar(50) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `AddressLine1` varchar(200) DEFAULT NULL,
  `AddressLine2` varchar(200) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `country` varchar(50) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `confirmPassword` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`firstName`, `lastName`, `username`, `email`, `phone`, `AddressLine1`, `AddressLine2`, `city`, `country`, `password`, `confirmPassword`) VALUES
('Arfadh', 'Iqbal', 'arfadhI', 'arfadh@gmail.com', '+44 20 1234 5678', '456 Elm Avenue', 'Suite 200', 'Springfield', 'Canada', 'password123', 'password123'),
('Ava', 'Gonzalez', 'avag', 'ava.gonzalez@yahoo.com', '+34 91 5678 9012', '876 Cedar Avenue', 'Suite 900', 'Madrid', 'Spain', 'passwordXYZ', 'passwordXYZ'),
('Charlotte', 'Young', 'charlottey', 'charlotte.young@icloud.com', '+82 2 7890 1234', '876 Pine Street', 'Suite 900', 'Seoul', 'South Korea', 'secureXYZ', 'secureXYZ'),
('Daniel', 'Clark', 'danielc', 'daniel.clark@icloud.com', '+61 2 3456 7890', '789 Pine Avenue', 'Apt 601', 'Sydney', 'Australia', 'passwordABC', 'passwordABC'),
('David', 'Johnson', 'david123', 'david.johnson@icloud.com', '+61 2 9876 5432', '789 Oak Street', 'Suite 300', 'Sydney', 'Australia', 'secure123', 'secure123'),
('Emma', 'Johnson', 'emmaj', 'emma.johnson@gmail.com', '+44 20 1234 5678', '456 Oak Street', 'Suite 300', 'Manchester', 'United Kingdom', 'test123', 'test123'),
('Ethan', 'Hernandez', 'ethan123', 'ethan.hernandez@yahoo.com', '+81 3 4567 8901', '753 Oak Street', 'Apt 801', 'Tokyo', 'Japan', 'testABC', 'testABC'),
('Isabella', 'Brown', 'isabellab', 'isabella.brown@gmail.com', '+1 (234) 567-8901', '987 Cedar Avenue', 'Suite 500', 'Los Angeles', 'United States', 'test456', 'test456'),
('James', 'Martinez', 'jamesm', 'james.martinez@yahoo.com', '+61 3 6789 0123', '654 Oak Avenue', 'Apt 800', 'Melbourne', 'Australia', 'testABC', 'testABC'),
('Liam', 'Smith', 'liams', 'liam.smith@example.com', '+1 (123) 456-7890', '123 Maple Avenue', 'Apt 200', 'Toronto', 'Canada', 'password123', 'password123'),
('Logan', 'Perez', 'loganp', 'logan.perez@gmail.com', '+61 3 6789 0123', '987 Elm Street', 'Apt 1001', 'Sydney', 'Australia', 'secureXYZ', 'secureXYZ'),
('Maria', 'Garcia', 'maria123', 'maria.garcia@yahoo.com', '+34 91 234 5678', '987 Maple Lane', 'Apt 301', 'Madrid', 'Spain', 'password456', 'password456'),
('Mia', 'Torres', 'miat', 'mia.torres@example.com', '+82 2 7890 1234', '210 Pine Road', 'Suite 1100', 'Seoul', 'South Korea', 'testXYZ', 'testXYZ'),
('Michael', 'Brown', 'michaelbrown', 'michael.brown@gmail.com', '+61 3 8765 4321', '210 Cedar Street', 'Suite 400', 'Sydney', 'Australia', 'test456', 'test456'),
('Neri', 'Meneripitiyage', 'neriM', 'neri@gmail.com', '+1 (123) 456-7890', '123 Main Street', 'Apt 101', 'Anytown', 'United States', 'neri123', 'neri123'),
('Noah', 'Williams', 'noahw', 'noah.williams@gmail.com', '+61 2 3456 7890', '789 Pine Road', 'Apt 400', 'Sydney', 'Australia', 'secure456', 'secure456'),
('Olivia', 'Rodriguez', 'oliviarod', 'olivia.rodriguez@icloud.com', '+1 (234) 567-8901', '654 Maple Road', 'Suite 700', 'New York', 'United States', 'secure123', 'secure123'),
('Sarah', 'Lee', 'sarahlee', 'sarah.lee@icloud.com', '+82 2 3456 7890', '753 Oak Lane', 'Apt 501', 'Seoul', 'South Korea', 'secure789', 'secure789'),
('Sophia', 'Garcia', 'sophiag', 'sophia.garcia@.yahoo.com', '+34 91 5678 9012', '753 Maple Road', 'Suite 700', 'Barcelona', 'Spain', 'passwordABC', 'passwordABC'),
('Tharusha', 'Fernando', 'tharushaF', 'tharusha@gmail.com', '+1 (987) 654-3210', '321 Oak Street', 'Apt 401', 'Los Angeles', 'United States', 't123', 't123'),
('Thenuki', 'Janmaweera', 'thenukiJ', 'thenuki@gmail.com', '+44 20 9876 5432', '456 Elm Street', 'Suite 500', 'London', 'United Kingdom', 'tabc', 'tabc'),
('William', 'Jones', 'williamj', 'william.jones@gmail.com', '+81 3 4567 8901', '210 Elm Street', 'Apt 600', 'Tokyo', 'Japan', 'secure789', 'secure789');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `destinations`
--
ALTER TABLE `destinations`
  ADD PRIMARY KEY (`destination_id`);

--
-- Indexes for table `profile_review`
--
ALTER TABLE `profile_review`
  ADD PRIMARY KEY (`review_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `destinations`
--
ALTER TABLE `destinations`
  MODIFY `destination_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT for table `profile_review`
--
ALTER TABLE `profile_review`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
