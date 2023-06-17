-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Temps de generació: 13-06-2023 a les 07:07:25
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
-- Base de dades: `gimnasUT5repas`
--
CREATE DATABASE IF NOT EXISTS `gimnasUT5repas` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `gimnasUT5repas`;

-- --------------------------------------------------------

--
-- Estructura de la taula `clients`
--

CREATE TABLE `clients` (
  `id` int(11) NOT NULL,
  `username` varchar(15) NOT NULL,
  `nom` varchar(30) NOT NULL,
  `llinatges` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefon` varchar(12) NOT NULL,
  `password` char(102) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Bolcament de dades per a la taula `clients`
--

INSERT INTO `clients` (`id`, `username`, `nom`, `llinatges`, `email`, `telefon`, `password`) VALUES
(1, 'amartinez', 'Angel', 'Martinez', 'amartinez@example.com', '666777888', 'pbkdf2:sha256:260000$FmeGDLSwcd69n5QI$6df8f7701a2daa6a0bad1119a3832b585f0ec9d658bb429552e3694a63d3dc25'),
(2, 'sikari', 'Shinji', 'Ikari', 'sikari@example.com', '666222888', 'pbkdf2:sha256:260000$10eZ4touJOL9A0Tl$001ca267fd695e4edaaf4412db0dfe70f4a05b323694045d2c30335614d992c7'),
(3, 'alangley', 'Asuka', 'Langley', 'alangley@example.com', '666333888', 'pbkdf2:sha256:260000$A9FpUwmSPxeZ552p$7037ca1fbbacb6bbb562984a542581c8ce8b641fc21de2fe120fa5b91ea4e2e1'),
(4, 'hkensjin', 'Himura', 'Kenshin', 'hkensjin@example.com', '666444888', 'pbkdf2 :sha256 :260000$FmeGDLSwcd69n5QI$6df8f7701a2daa6a0bad1119a3832b585f0ec9d658bb429552e3694a63d3dc'),
(5, 'SaulGman', 'pepe', 'Goodman', '', '999777555', 'pbkdf2:sha256:260000$92p0bfnAB1JzNLzc$070f91a33e5c30b6f2c2870b6f3ceba2065603577fdb46152994a9a3061ba226');

-- --------------------------------------------------------

--
-- Estructura de la taula `pistes`
--

CREATE TABLE `pistes` (
  `idpista` int(11) NOT NULL,
  `tipo` enum('Coberta','Exterior') NOT NULL,
  `preu` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Bolcament de dades per a la taula `pistes`
--

INSERT INTO `pistes` (`idpista`, `tipo`, `preu`) VALUES
(1, 'Coberta', 12),
(2, 'Exterior', 8);

-- --------------------------------------------------------

--
-- Estructura de la taula `reserves`
--

CREATE TABLE `reserves` (
  `data` datetime NOT NULL,
  `idpista` int(11) NOT NULL,
  `idclient` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Bolcament de dades per a la taula `reserves`
--

INSERT INTO `reserves` (`data`, `idpista`, `idclient`) VALUES
('2023-01-09 21:00:00', 1, 1),
('2023-01-25 15:00:00', 1, 1),
('2023-02-02 16:00:00', 1, 1),
('2023-02-06 15:00:00', 1, 1),
('2023-02-15 15:00:00', 1, 1),
('2023-02-16 15:00:00', 1, 1),
('2023-02-21 16:00:00', 1, 1),
('2023-02-24 19:00:00', 2, 1),
('2023-02-26 19:00:00', 2, 1),
('2023-02-27 19:00:00', 2, 1),
('2023-02-21 15:00:00', 2, 2),
('2023-03-07 15:00:00', 2, 2),
('2023-06-04 15:00:00', 2, 2),
('2023-06-05 15:00:00', 2, 2),
('2023-06-06 15:00:00', 2, 2),
('2023-06-07 15:00:00', 2, 2),
('2023-06-08 15:00:00', 2, 2),
('2023-06-09 15:00:00', 2, 2),
('2023-06-10 15:00:00', 2, 2),
('2023-06-11 15:00:00', 2, 2),
('2023-06-12 15:00:00', 2, 2),
('2023-02-15 17:00:00', 2, 3),
('2022-11-04 17:00:00', 1, 4),
('2022-11-08 16:00:00', 1, 4),
('2022-11-30 17:00:00', 2, 4),
('2023-02-23 19:00:00', 2, 4),
('2022-11-09 16:00:00', 1, 5),
('2023-02-14 21:00:00', 2, 5),
('2023-02-21 17:00:00', 2, 8),
('2023-02-22 17:00:00', 2, 8),
('2023-06-12 15:00:00', 1, 8),
('2023-06-14 19:00:00', 2, 8);

-- --------------------------------------------------------

--
-- Estructura de la taula `usuaris`
--

CREATE TABLE `usuaris` (
  `id` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `nom` varchar(50) DEFAULT NULL,
  `llinatges` varchar(50) DEFAULT NULL,
  `telefon` varchar(50) DEFAULT NULL,
  `diaalta` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Bolcament de dades per a la taula `usuaris`
--

INSERT INTO `usuaris` (`id`, `username`, `password`, `email`, `nom`, `llinatges`, `telefon`, `diaalta`) VALUES
(1, 'jose', 'pbkdf2:sha256:260000$ux2sFlCJ65ZbGJkA$eaf6b612d6324680d24eb3a93ed9e26d8c86c9f0853c1d13e12ffd339a857cb6', 'jose.merinopanades@gmail.com', 'Jose', 'Merino', '333444555', '2022-10-04'),
(2, 'root', 'pbkdf2:sha256:260000$ux2sFlCJ65ZbGJkA$eaf6b612d6324680d24eb3a93ed9e26d8c86c9f0853c1d13e12ffd339a857cb6', 'administrador@paucasesnovescifp.cat', 'Super', 'Jefe', '999111222', '2022-10-05'),
(3, 'user1', 'pbkdf2:sha256:260000$ux2sFlCJ65ZbGJkA$eaf6b612d6324680d24eb3a93ed9e26d8c86c9f0853c1d13e12ffd339a857cb6', 'user1@hotmail.com', 'usuario', 'anonimo', '456456456', '2022-09-15'),
(4, 'administrador', 'pbkdf2:sha256:260000$ux2sFlCJ65ZbGJkA$eaf6b612d6324680d24eb3a93ed9e26d8c86c9f0853c1d13e12ffd339a857cb6', 'jlmerino@sampol.com', 'Pep', 'Mula', '971764476', '2022-11-03'),
(5, 'paucasesnoves', 'pbkdf2:sha256:260000$qpOrJdVM7KGPqfg6$b2d6b3c2a29bbc409ca45fdb1c11e2e28d0e5907816de4121029a0bf5f254391', 'paucases@gmail.com', 'Pau', 'Casesnoves', '123456789', '2022-11-02'),
(6, 'carla', 'pbkdf2:sha256:260000$SeqGC1CkNseMGknP$1f580f23ed73eabb678c8de6563c5da62f7b490faedc353fc075cf8f262cf8fe', 'igansi@gmail.com', 'IGNASI', 'ALZINA AMER', '669000000', '2023-11-29'),
(7, 'gabriel', 'pbkdf2:sha256:260000$MIDoKEVqynStfSeb$c8f02f658b4621d4ac6ba7c8012e35d4b14c5c8792afb140a5a1bfcdbc475b0e', 'biel@gmail.com', 'GABRIEL', 'ALZINA ALOMAR', '669668705', '2023-06-10'),
(8, 'pruna', 'pbkdf2:sha256:260000$lmOf7VEY6SDcZb6j$b92f13d545b7abac86afd5f7d1fde91fad2c8084a2699413543964f3cef67891', 'pruna@gmail.com', 'PRUNA', 'pardal DE MORO', '666666666', '2023-02-15');

--
-- Índexs per a les taules bolcades
--

--
-- Índexs per a la taula `clients`
--
ALTER TABLE `clients`
  ADD PRIMARY KEY (`id`);

--
-- Índexs per a la taula `pistes`
--
ALTER TABLE `pistes`
  ADD PRIMARY KEY (`idpista`);

--
-- Índexs per a la taula `reserves`
--
ALTER TABLE `reserves`
  ADD PRIMARY KEY (`data`,`idpista`),
  ADD KEY `r_idpista` (`idpista`),
  ADD KEY `reserves_ibfk_1` (`idclient`);

--
-- Índexs per a la taula `usuaris`
--
ALTER TABLE `usuaris`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT per les taules bolcades
--

--
-- AUTO_INCREMENT per la taula `clients`
--
ALTER TABLE `clients`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT per la taula `pistes`
--
ALTER TABLE `pistes`
  MODIFY `idpista` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Restriccions per a les taules bolcades
--

--
-- Restriccions per a la taula `reserves`
--
ALTER TABLE `reserves`
  ADD CONSTRAINT `reserves_ibfk_1` FOREIGN KEY (`idclient`) REFERENCES `usuaris` (`id`),
  ADD CONSTRAINT `reserves_ibfk_2` FOREIGN KEY (`idpista`) REFERENCES `pistes` (`idpista`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
