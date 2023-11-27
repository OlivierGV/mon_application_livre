/* Créer la database et l'utiliser */
DROP DATABASE travail_pratique;
CREATE DATABASE travail_pratique
	CHARACTER SET = 'utf8mb4' 
	COLLATE = 'utf8mb4_unicode_ci';

USE travail_pratique;

/* Mon user */
DROP USER IF EXISTS 'lebeauolivier'@'&';
CREATE USER IF NOT EXISTS 'lebeauolivier'@'%' IDENTIFIED BY '123';

GRANT SELECT ON travail_pratique.* TO 'lebeauolivier'@'%';

FLUSH PRIVILEGES;

/* Créer les tables */
CREATE TABLE IF NOT EXISTS livre (
	id INTEGER AUTO_INCREMENT NOT NULL,
	nom VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
	);

CREATE TABLE IF NOT EXISTS chapitre (
	id INTEGER AUTO_INCREMENT NOT NULL,
	no_chapitre VARCHAR(255) NOT NULL,
	texte TEXT NOT NULL,
	id_livre INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_livre) REFERENCES livre(id)
	);

CREATE TABLE IF NOT EXISTS lien_chapitre (
	id INTEGER AUTO_INCREMENT NOT NULL,
	no_chapitre_origine VARCHAR(255) NOT NULL,
	no_chapitre_destination VARCHAR(255) NOT NULL,
	id_livre INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_livre) REFERENCES livre(id)
	);
	
CREATE TABLE IF NOT EXISTS personnage (
	id INTEGER AUTO_INCREMENT NOT NULL,
	nom VARCHAR(255) NOT NULL,
	endurance INTEGER NOT NULL DEFAULT 20,
	habilete INTEGER NOT NULL DEFAULT 10,
	PRIMARY KEY (id)
	);

CREATE TABLE IF NOT EXISTS partie (
	id INTEGER AUTO_INCREMENT NOT NULL,
	chapitre_sauvegarde VARCHAR(255),
	id_livre INTEGER NOT NULL,
	id_personnage INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_livre) REFERENCES livre(id),
	FOREIGN KEY (id_personnage) REFERENCES personnage(id)
	);

CREATE TABLE IF NOT EXISTS sac_a_dos (
	id INTEGER AUTO_INCREMENT,
	objets TEXT NULL DEFAULT '',
	repas TEXT NULL DEFAULT '',
	objets_speciaux TEXT NULL DEFAULT '',
	bourse INTEGER NOT NULL DEFAULT 0 CHECK (bourse <= 50),
	id_personnage INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_personnage) REFERENCES personnage(id)
	);

CREATE TABLE IF NOT EXISTS arme (
	id INTEGER AUTO_INCREMENT NOT NULL,
	nom VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
	);

CREATE TABLE IF NOT EXISTS discipline_kai (
	id INTEGER AUTO_INCREMENT NOT NULL,
	nom VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
	);

CREATE TABLE IF NOT EXISTS personnage_arme (
	id INTEGER AUTO_INCREMENT NOT NULL,
	id_arme INTEGER NOT NULL,
	id_personnage INTEGER NOT NULL,
	PRIMARY KEY (id),
	FOREIGN KEY (id_personnage) REFERENCES personnage(id),
	FOREIGN KEY (id_arme) REFERENCES arme(id)
	);
	
CREATE TABLE IF NOT EXISTS personnage_kai (
	id INTEGER AUTO_INCREMENT NOT NULL,
	id_kai INTEGER NOT NULL,
	id_personnage INTEGER NOT NULL,
	notes TEXT NOT NULL DEFAULT '',
	PRIMARY KEY (id),
	FOREIGN KEY (id_personnage) REFERENCES personnage(id),
	FOREIGN KEY (id_kai) REFERENCES discipline_kai(id)
	);

/* Contraintes */
ALTER TABLE sac_a_dos
	ADD CONSTRAINT verifier_limite_bourse
	CHECK (bourse <= 50);

/* Fonctions, procédures et déclencheurs */
/* Vérifier que le personnage ne peut dépasser 50 dans la bourse */
DELIMITER $$

CREATE TRIGGER IF NOT EXISTS verifier_bourse
    BEFORE UPDATE
    ON sac_a_dos FOR EACH ROW
    BEGIN
        IF NEW.bourse <= 50 THEN 
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'La bourse du personnage ne peut dépasser 50.';
           	SET NEW.bourse = 50;
        END IF;
    END $$


DELIMITER ;
/* Vérifier que le personnage n'a que 2 armes */
DELIMITER $$

CREATE TRIGGER IF NOT EXISTS verifier_arme
    BEFORE INSERT
    ON personnage_arme FOR EACH ROW
    BEGIN
	   	DECLARE qt_arme INT;
	    SET qt_arme = (SELECT COUNT(*) FROM personnage_arme WHERE id_personnage = NEW.id_personnage);
        IF qt_arme >= 2 THEN 
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Vous avez déjà atteint la limite de 2 armes.';
        END IF;
    END $$


DELIMITER ;
/* Vérifier que le personnage n'a que 5 disciplines kai */
DELIMITER $$

CREATE TRIGGER IF NOT EXISTS verifier_kai
    BEFORE INSERT
    ON personnage_kai FOR EACH ROW
    BEGIN
	   	DECLARE qt_kai INT;
	    SET qt_kai = (SELECT COUNT(*) FROM personnage_kai WHERE id_personnage = NEW.id_personnage);
        IF qt_kai >= 5 THEN 
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Vous avez déjà atteint la limite de 5 disciplines kai.';
        END IF;
    END $$


DELIMITER ;