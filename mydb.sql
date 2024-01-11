
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";



CREATE TABLE `parent` (
  `id_parent` int NOT NULL AUTO_INCREMENT,
  `email` varchar(45) NOT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(45) NOT NULL,
  `koordinat_lattitude` float NOT NULL,
  `koordinat_longtitude` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

INSERT INTO `parent` (`email`, `username`, `password`, `koordinat_lattitude`, `koordinat_longtitude`) VALUES
('kasihsayangibu@gmail.com', 'raze', 'cihuy', -6.13556, 106.177);



CREATE TABLE `parent_has_tracker` (
  `Parent_id_parent` int NOT NULL,
  `Tracker_id_tracker` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


CREATE TABLE `tracker` (
  `id_tracker` int NOT NULL,
  `nama_anak` varchar(45) DEFAULT NULL,
  `lokasi` varchar(45) DEFAULT NULL,
  `koordinat_lattitude` float NOT NULL,
  `koordinat_longtitude` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


INSERT INTO `tracker` (`id_tracker`, `nama_anak`, `lokasi`, `koordinat_lattitude`, `koordinat_longtitude`) VALUES
(105220000, 'Asep', 'lokasi_asep', -6.22486, 106.98);


ALTER TABLE `parent`
  ADD PRIMARY KEY (`id_parent`);

ALTER TABLE `parent_has_tracker`
  ADD PRIMARY KEY (`Parent_id_parent`,`Tracker_id_tracker`),
  ADD KEY `fk_Parent_has_Tracker_Tracker1_idx` (`Tracker_id_tracker`),
  ADD KEY `fk_Parent_has_Tracker_Parent_idx` (`Parent_id_parent`);

ALTER TABLE `tracker`
  ADD PRIMARY KEY (`id_tracker`);

ALTER TABLE `parent_has_tracker`
  ADD CONSTRAINT `fk_Parent_has_Tracker_Parent` FOREIGN KEY (`Parent_id_parent`) REFERENCES `parent` (`id_parent`),
  ADD CONSTRAINT `fk_Parent_has_Tracker_Tracker1` FOREIGN KEY (`Tracker_id_tracker`) REFERENCES `tracker` (`id_tracker`);
COMMIT;
