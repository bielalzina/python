-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Temps de generació: 15-03-2023 a les 20:26:09
-- Versió del servidor: 10.4.27-MariaDB
-- Versió de PHP: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de dades: `whatspau`
--
CREATE DATABASE IF NOT EXISTS `whatspau` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `whatspau`;

-- --------------------------------------------------------

--
-- Estructura de la taula `estat_missatges_grup`
--

CREATE TABLE `estat_missatges_grup` (
  `id_missatge` int(50) NOT NULL,
  `id_receiver` int(11) NOT NULL,
  `status` enum('send','received','read') CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL DEFAULT 'send'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Bolcament de dades per a la taula `estat_missatges_grup`
--

INSERT INTO `estat_missatges_grup` (`id_missatge`, `id_receiver`, `status`) VALUES
(1, 1, 'send'),
(1, 2, 'send'),
(1, 3, 'send'),
(2, 3, 'send'),
(2, 4, 'send'),
(3, 4, 'send'),
(4, 1, 'send'),
(4, 3, 'send'),
(5, 1, 'send'),
(5, 4, 'send'),
(6, 1, 'send'),
(6, 3, 'send'),
(7, 3, 'send'),
(7, 4, 'send'),
(8, 1, 'send'),
(8, 4, 'send'),
(9, 1, 'send'),
(9, 3, 'send'),
(10, 2, 'read'),
(11, 4, 'send'),
(12, 1, 'send'),
(12, 3, 'send'),
(12, 4, 'read'),
(13, 1, 'send'),
(13, 2, 'send'),
(13, 4, 'read'),
(34, 1, 'send'),
(34, 2, 'send'),
(34, 3, 'send'),
(35, 1, 'send'),
(35, 2, 'send'),
(35, 3, 'send'),
(37, 3, 'send'),
(37, 4, 'send'),
(38, 2, 'read');

-- --------------------------------------------------------

--
-- Estructura de la taula `grups`
--

CREATE TABLE `grups` (
  `id_grup` int(11) NOT NULL,
  `groupname` varchar(50) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Bolcament de dades per a la taula `grups`
--

INSERT INTO `grups` (`id_grup`, `groupname`) VALUES
(1, 'TRAVESSES'),
(2, 'DINARS'),
(3, 'SOPARS');

-- --------------------------------------------------------

--
-- Estructura de la taula `members_grup`
--

CREATE TABLE `members_grup` (
  `id_grup` int(11) NOT NULL,
  `id_member` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Bolcament de dades per a la taula `members_grup`
--

INSERT INTO `members_grup` (`id_grup`, `id_member`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(2, 1),
(2, 3),
(2, 4),
(3, 2),
(3, 4);

-- --------------------------------------------------------

--
-- Estructura de la taula `missatges`
--

CREATE TABLE `missatges` (
  `fecha` datetime NOT NULL,
  `id_sender` int(11) NOT NULL,
  `id_receiver` int(11) NOT NULL,
  `missatge` varchar(250) NOT NULL,
  `status` enum('send','received','read') NOT NULL DEFAULT 'send'
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Bolcament de dades per a la taula `missatges`
--

INSERT INTO `missatges` (`fecha`, `id_sender`, `id_receiver`, `missatge`, `status`) VALUES
('2022-08-30 00:00:00', 1, 2, 'Bon dia Marga', 'read'),
('2022-08-30 00:03:00', 2, 1, 'Bon dia Jose, que volies?', 'received'),
('2022-08-30 00:04:00', 1, 2, 'res', 'send'),
('2022-08-30 00:04:30', 1, 2, 'nomes saludar', 'send'),
('2022-08-30 12:03:00', 2, 1, 'pues vale', 'received'),
('2022-08-30 16:38:05', 1, 2, 'adeu Marga', 'send'),
('2022-11-10 18:37:49', 1, 2, 'adeu Marga', 'send'),
('2022-11-11 10:59:07', 2, 3, 'Ets per aqui?', 'send'),
('2022-11-11 11:59:07', 2, 3, 'No te veig', 'send'),
('2023-03-01 10:59:07', 4, 1, 'Hola', 'send'),
('2023-03-01 11:00:00', 4, 1, 'On ets?', 'send'),
('2023-03-01 11:01:00', 4, 1, 'No te veig', 'send'),
('2023-03-02 11:02:00', 4, 3, 'Pau vens', 'send'),
('2023-03-02 11:03:00', 3, 4, 'Voy', 'read'),
('2023-03-02 11:04:00', 4, 3, 'Perfecte', 'send'),
('2023-03-12 10:53:49', 4, 3, 'Soc el bar', 'send'),
('2023-03-12 11:49:05', 4, 3, 'Faig una xiscla', 'send'),
('2023-03-12 12:06:48', 3, 4, 'Sempre ets al bar', 'read'),
('2023-03-12 12:07:14', 3, 4, 'Ets un perdut', 'read');

-- --------------------------------------------------------

--
-- Estructura de la taula `missatges_grup`
--

CREATE TABLE `missatges_grup` (
  `id_missatge` int(50) NOT NULL,
  `data` datetime NOT NULL,
  `missatge` varchar(250) CHARACTER SET latin1 COLLATE latin1_spanish_ci NOT NULL,
  `id_sender` int(11) NOT NULL,
  `id_receiver_grup` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Bolcament de dades per a la taula `missatges_grup`
--

INSERT INTO `missatges_grup` (`id_missatge`, `data`, `missatge`, `id_sender`, `id_receiver_grup`) VALUES
(1, '2023-03-12 21:04:25', 'Hem de fer una travessa', 4, 1),
(2, '2023-03-12 21:06:22', 'Hem de fer un dinar?', 1, 2),
(3, '2023-03-12 21:06:22', 'Avui sopam d\'amanida', 2, 3),
(4, '2023-03-14 12:17:58', 'En voler', 4, 2),
(5, '2023-03-14 12:21:15', 'Ja feim tard', 3, 2),
(6, '2023-03-14 12:22:07', 'Podem fer una torrada', 4, 2),
(7, '2023-03-14 12:23:49', 'Jo dure el vi i el carbó', 1, 2),
(8, '2023-03-14 12:24:26', 'Jo dure la carn', 3, 2),
(9, '2023-03-14 12:24:55', 'Ido jo posare el lloc', 4, 2),
(10, '2023-03-14 12:55:04', 'Una amanida i un poc de pitera', 4, 3),
(11, '2023-03-14 12:56:02', 'Com tu vulguis', 2, 3),
(12, '2023-03-14 13:03:21', 'Ens veiem avui capvespre i la feimn', 2, 1),
(13, '2023-03-14 13:04:55', 'Quedam a les vuit?', 3, 1),
(34, '2023-03-15 19:26:41', 'A les vuit me va bé, ens veiem a l\'Antonio BAR?', 4, 1),
(35, '2023-03-15 19:29:18', 'Aquesta setmana segur que endevinam tots els resultats', 4, 1),
(37, '2023-03-15 19:32:26', 'Supos que menjarem un bon entrecot', 1, 2),
(38, '2023-03-15 19:35:55', 'Perfecte!!!!', 4, 3);

-- --------------------------------------------------------

--
-- Estructura de la taula `users_base`
--

CREATE TABLE `users_base` (
  `id_user` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Bolcament de dades per a la taula `users_base`
--

INSERT INTO `users_base` (`id_user`, `username`, `password`) VALUES
(1, 'Jose', 'mypassword'),
(2, 'Marga', '123456'),
(3, 'Pau', '654321'),
(4, 'Gabriel', 'Passw@rd'),
(5, 'Victoria', '12345');

--
-- Índexs per a les taules bolcades
--

--
-- Índexs per a la taula `estat_missatges_grup`
--
ALTER TABLE `estat_missatges_grup`
  ADD PRIMARY KEY (`id_missatge`,`id_receiver`),
  ADD KEY `estat_missatges_grup_ibfk_2` (`id_receiver`);

--
-- Índexs per a la taula `grups`
--
ALTER TABLE `grups`
  ADD PRIMARY KEY (`id_grup`);

--
-- Índexs per a la taula `members_grup`
--
ALTER TABLE `members_grup`
  ADD PRIMARY KEY (`id_grup`,`id_member`),
  ADD KEY `members_grup_ibfk_2` (`id_member`);

--
-- Índexs per a la taula `missatges`
--
ALTER TABLE `missatges`
  ADD PRIMARY KEY (`fecha`,`id_sender`),
  ADD KEY `missatges_ibfk_1` (`id_sender`),
  ADD KEY `id_receiver` (`id_receiver`);

--
-- Índexs per a la taula `missatges_grup`
--
ALTER TABLE `missatges_grup`
  ADD PRIMARY KEY (`id_missatge`,`data`),
  ADD KEY `missatges_grup_ibfk_1` (`id_sender`),
  ADD KEY `missatges_grup_ibfk_2` (`id_receiver_grup`);

--
-- Índexs per a la taula `users_base`
--
ALTER TABLE `users_base`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT per les taules bolcades
--

--
-- AUTO_INCREMENT per la taula `grups`
--
ALTER TABLE `grups`
  MODIFY `id_grup` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT per la taula `missatges_grup`
--
ALTER TABLE `missatges_grup`
  MODIFY `id_missatge` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT per la taula `users_base`
--
ALTER TABLE `users_base`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restriccions per a les taules bolcades
--

--
-- Restriccions per a la taula `estat_missatges_grup`
--
ALTER TABLE `estat_missatges_grup`
  ADD CONSTRAINT `estat_missatges_grup_ibfk_1` FOREIGN KEY (`id_missatge`) REFERENCES `missatges_grup` (`id_missatge`),
  ADD CONSTRAINT `estat_missatges_grup_ibfk_2` FOREIGN KEY (`id_receiver`) REFERENCES `users_base` (`id_user`);

--
-- Restriccions per a la taula `members_grup`
--
ALTER TABLE `members_grup`
  ADD CONSTRAINT `members_grup_ibfk_1` FOREIGN KEY (`id_grup`) REFERENCES `grups` (`id_grup`),
  ADD CONSTRAINT `members_grup_ibfk_2` FOREIGN KEY (`id_member`) REFERENCES `users_base` (`id_user`),
  ADD CONSTRAINT `members_grup_ibkf_1` FOREIGN KEY (`id_grup`) REFERENCES `grups` (`id_grup`);

--
-- Restriccions per a la taula `missatges`
--
ALTER TABLE `missatges`
  ADD CONSTRAINT `missatges_ibfk_1` FOREIGN KEY (`id_sender`) REFERENCES `users_base` (`id_user`),
  ADD CONSTRAINT `missatges_ibfk_2` FOREIGN KEY (`id_receiver`) REFERENCES `users_base` (`id_user`);

--
-- Restriccions per a la taula `missatges_grup`
--
ALTER TABLE `missatges_grup`
  ADD CONSTRAINT `missatges_grup_ibfk_1` FOREIGN KEY (`id_sender`) REFERENCES `users_base` (`id_user`),
  ADD CONSTRAINT `missatges_grup_ibfk_2` FOREIGN KEY (`id_receiver_grup`) REFERENCES `grups` (`id_grup`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
