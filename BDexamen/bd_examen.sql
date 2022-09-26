-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         8.0.20 - MySQL Community Server - GPL
-- SO del servidor:              Win64
-- HeidiSQL Versión:             12.1.0.6537
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para bd_examen
CREATE DATABASE IF NOT EXISTS `bd_examen` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `bd_examen`;

-- Volcando estructura para tabla bd_examen.curso
CREATE TABLE IF NOT EXISTS `curso` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `creditos` int NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla bd_examen.curso: ~5 rows (aproximadamente)
INSERT INTO `curso` (`codigo`, `creditos`, `nombre`, `create_date`) VALUES
	(1, 4, 'redes', '2022-09-26 17:27:04'),
	(2, 3, 'Mineria', '2022-09-26 17:28:29'),
	(3, 4, 'Telecominacion', '2022-09-26 20:14:57'),
	(4, 2, 'Cloud Computing', '2022-09-26 20:21:41'),
	(5, 5, 'Topografia', '2022-09-26 20:32:10');

-- Volcando estructura para tabla bd_examen.escuela
CREATE TABLE IF NOT EXISTS `escuela` (
  `codigo` int NOT NULL AUTO_INCREMENT,
  `duracion` int NOT NULL,
  `nombre` varchar(120) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla bd_examen.escuela: ~4 rows (aproximadamente)
INSERT INTO `escuela` (`codigo`, `duracion`, `nombre`, `create_date`) VALUES
	(1, 10, 'ingenieria minas', '2022-09-26 17:26:52'),
	(2, 10, 'Ingniera Agroindustrial', '2022-09-26 20:14:30'),
	(3, 10, 'Ingenieria de Sistemas y informatica ', '2022-09-26 20:21:07'),
	(4, 10, 'Ingenieria Civil', '2022-09-26 20:31:52');

-- Volcando estructura para tabla bd_examen.estudiante
CREATE TABLE IF NOT EXISTS `estudiante` (
  `dni` varchar(8) NOT NULL,
  `nombres` varchar(120) NOT NULL,
  `apellidos` varchar(200) NOT NULL,
  `FeNacimiento` varchar(200) NOT NULL,
  `sexo` varchar(10) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `cod_escuela` int DEFAULT NULL,
  PRIMARY KEY (`dni`),
  KEY `cod_escuela` (`cod_escuela`),
  CONSTRAINT `estudiante_ibfk_1` FOREIGN KEY (`cod_escuela`) REFERENCES `escuela` (`codigo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla bd_examen.estudiante: ~4 rows (aproximadamente)
INSERT INTO `estudiante` (`dni`, `nombres`, `apellidos`, `FeNacimiento`, `sexo`, `create_date`, `cod_escuela`) VALUES
	('61116115', 'Luis', 'Vargas', '2022-08-10', 'Masculino', '2022-09-26 20:15:32', 2),
	('71958460', 'Joel', 'Zegarra', '2022-09-13', 'Masculino', '2022-09-26 20:22:33', 3),
	('72958460', 'Anali', 'Pinedo', '2022-08-28', 'Femenino', '2022-09-26 20:33:32', 4),
	('74528160', 'Edison', 'Ñahui', '2022-09-01', 'Masculino', '2022-09-26 17:27:25', 2);

-- Volcando estructura para tabla bd_examen.matricula
CREATE TABLE IF NOT EXISTS `matricula` (
  `id` int NOT NULL AUTO_INCREMENT,
  `create_date` datetime DEFAULT NULL,
  `cod_curso` int DEFAULT NULL,
  `dni` varchar(8) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `cod_curso` (`cod_curso`),
  KEY `dni` (`dni`),
  CONSTRAINT `matricula_ibfk_1` FOREIGN KEY (`cod_curso`) REFERENCES `curso` (`codigo`),
  CONSTRAINT `matricula_ibfk_2` FOREIGN KEY (`dni`) REFERENCES `estudiante` (`dni`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Volcando datos para la tabla bd_examen.matricula: ~3 rows (aproximadamente)
INSERT INTO `matricula` (`id`, `create_date`, `cod_curso`, `dni`) VALUES
	(2, '2022-09-26 17:29:07', 1, '74528160'),
	(3, '2022-09-26 20:17:15', 5, '61116115'),
	(4, '2022-09-26 20:38:13', 4, '71958460');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
