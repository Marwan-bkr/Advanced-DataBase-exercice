# Projet Base de données avancées

## 1\. Préparation de la base de données : création, remplissage et contraintes d’intégrités

### 1\. Créer la base de données

CREATE DATABASE locauto;

### Import des données via Phpmyadmin car Workbench créé des erreurs. 

### 3\. Vérifier les données et compléter/corriger les données

1. #### SET les PKs en premier pour pouvoir faire les modifications qu’on veut par la suite

   ALTER TABLE client ADD PRIMARY KEY (CodeC);

   

   ALTER TABLE proprietaire ADD PRIMARY KEY (CodeP);

   

   ALTER TABLE location ADD COLUMN CodeL INT AUTO\_INCREMENT PRIMARY KEY;

   

   ALTER TABLE voiture ADD PRIMARY KEY (immat);

   

2. #### verification des emails au bon format ou NULL

   #### ALTER TABLE proprietaire ADD CONSTRAINT CHK\_propemail CHECK (email LIKE '%@%.%' OR email \= NULL); 

   #### Il serait intéressant de mettre en place un trigger qui avant une insertion vérifie si le nouvel email est conforme au format email.

3. #### Modification des tailles des columns parce qu'à l’import elles ont été configuré au max des données actuelles

   ALTER TABLE client 

   MODIFY COLUMN Nom VARCHAR(15), 

   MODIFY COLUMN Prenom VARCHAR(15), 

   MODIFY COLUMN Permis VARCHAR(10), 

   MODIFY COLUMN Adresse VARCHAR(25), 

   MODIFY COLUMN Ville VARCHAR(15), 

   MODIFY COLUMN CodeC VARCHAR(5);

   

   SELECT LENGTH(TRIM(note)) FROM location WHERE LENGTH(TRIM(note)) \> 0;

   ALTER TABLE location MODIFY COLUMN CodeC VARCHAR(5),

   MODIFY COLUMN villed VARCHAR(15),

   MODIFY COLUMN villea VARCHAR(15),

   MODIFY COLUMN dated date,

   MODIFY COLUMN datef date,

   DROP COLUMN note,

   ADD COLUMN note DECIMAL(4,2),

   MODIFY COLUMN avis VARCHAR(140);

   ALTER TABLE proprietaire

   MODIFY COLUMN codeP VARCHAR(4),

   MODIFY COLUMN Pseudo VARCHAR(15),

   MODIFY COLUMN ville VARCHAR(15),

   MODIFY COLUMN anneeI INTEGER;

   ALTER TABLE proprietaire

   MODIFY COLUMN anneeI YEAR;

   ALTER TABLE voiture

   MODIFY COLUMN modele VARCHAR(10),

   MODIFY COLUMN marque VARCHAR(10),

   MODIFY COLUMN Categorie VARCHAR(10),

   MODIFY COLUMN achatA INTEGER,

   MODIFY COLUMN prixJ DECIMAL(5,2),

   MODIFY COLUMN codeP VARCHAR(4);

   ALTER TABLE voiture

   MODIFY COLUMN achatA YEAR;

4. #### Supprimer les lignes complètement vides de chaque table 

   SET SQL\_SAFE\_UPDATES \= 0;

   DELETE FROM client WHERE

   (colonne1 IS NULL OR TRIM(colonne1) \= '')

   AND (colonne2 IS NULL OR TRIM(colonne2) \= '');

   SET SQL\_SAFE\_UPDATES \= 1;

5. #### Pseudo proprietaire UPDATE to implement NOT NULL et UNIQUE

   SET @AI :\= 0;

   UPDATE proprietaire p

   JOIN (

      SELECT CodeP FROM proprietaire WHERE Pseudo \= (

   SELECT Pseudo FROM proprietaire GROUP BY Pseudo HAVING COUNT(\*)\>1

   ) ) AS temp ON temp.CodeP\=p.CodeP

   SET p.Pseudo \= CONCAT(p.Pseudo,(@AI :\= @AI\+1));

   ALTER TABLE proprietaire

   MODIFY COLUMN Pseudo VARCHAR(15) NOT NULL UNIQUE;

   

6. #### la datef (fin de location) est à mettre à jour par requête sql : datef \= datef \+ valeurs entre 0 et 100 (rand()). Attention : il faut mettre à jour la durée (datef – dated en nombre de jours).

			  
En créant la colonne dureeTS au format DATETIME j’ouvre le stockage de l’information de la durée de location à des précisions futures comme le nombre d’heure précis, s’il ne correspond pas à des jours complet. 

ALTER TABLE location  
MODIFY COLUMN CodeC VARCHAR(5),  
MODIFY COLUMN villed VARCHAR(15),  
MODIFY COLUMN villea VARCHAR(15),  
MODIFY COLUMN dated DATETIME NOT NULL,  
MODIFY COLUMN datef DATETIME NOT NULL,  
MODIFY COLUMN km int NOT NULL,  
DROP COLUMN note,  
ADD COLUMN note DECIMAL(4,2),  
MODIFY COLUMN avis VARCHAR(140),  
ADD COLUMN dureeTS DATETIME;  
SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE location l  
SET l.dureeTS \=  '1000-01-01 00:00:00' \+ INTERVAL l.duree DAY;  
SET SQL\_SAFE\_UPDATES \= 1;  
ALTER TABLE location  
MODIFY COLUMN dureeTS DATETIME;  
SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE location l  
SET l.datef \=  DATE\_ADD(l.dated, INTERVAL TIMESTAMPDIFF(SECOND, '1000-01-01 00:00:00', dureeTS) SECOND ) ;  
SET SQL\_SAFE\_UPDATES \= 1;  
CREATE TRIGGER update\_dureeTS  
BEFORE INSERT ON location  
FOR EACH ROW  
  SET NEW.dureeTS \= DATE\_ADD('1000-01-01 00:00:00', INTERVAL NEW.duree DAY);

### 3\. Ajouter les contraintes qui vous semble nécessaires pour préserver l’intégrité de cette base de données (clés, référencement, unicité, valeur ….)

ALTER TABLE location  
ADD FOREIGN KEY (CodeC) REFERENCES client(CodeC);  
ALTER TABLE location  
ADD FOREIGN KEY (immat) REFERENCES voiture(immat);  
ALTER TABLE voiture  
ADD FOREIGN KEY (codeP) REFERENCES proprietaire(codeP);

### 4\. Vérifier vos contraintes.

	  
INSERT INTO location  
(CodeC, immat, annee, mois, numloc, km, villed, villea, dated, datef, avis, note, duree)  
VALUES  
('XXXXX', 'XXXXXXX', 2024, 11, 'L001', NULL, 'Lyon', 'Paris', '2024-11-02', '2024-11-05', NULL, NULL, '1000-01-02 00:00:00');

INSERT INTO location  
(codeP, Pseudo, email, ville, anneeI)  
VALUES  
('XXXXX', 'XXXXXXX', 'blabla', 'Lyon', 2006);

INSERT INTO voiture  
(Immat, modele, marque, Categorie, couleur, places, achatA, compteur, prixJ, codeP)  
VALUES  
('XXXXX', 'XXXXXXX', 'Audi', 'Monospace', 'Noir', 6, 2006, 120000, '25', 'P26');

## 2\. Vues

### 1\. Créer une vue V\_Client contenant : le code, le prénom et le nom des clients, l’âge, la somme des KM de location (baptisée distance).

CREATE VIEW V\_Client AS  
SELECT a.CodeC, a.Prenom, a.Nom, a.age, b.distance FROM  
   client a,  
   (SELECT CodeC, SUM(km) AS distance FROM location GROUP BY CodeC) b  
WHERE a.CodeC\=b.Codec;

###  	2.Essayer de mettre à jour le nom d’un client à travers la vue V\_Client.

SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE v\_client  
SET Nom \= 'Lazard'  
WHERE Nom\='Juniot';  
SET SQL\_SAFE\_UPDATES \= 1;

### Essayer ensuite de mettre à jour le champ « distance » d’un client. Que se passe-t-il à chaque action ?

SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE v\_client  
SET distance \= 60000  
WHERE distance\=144;  
SET SQL\_SAFE\_UPDATES \= 1;

C’est impossible, car la colonne distance est le résultat d’une somme. Il est, alors, impossible de déterminer comment répartir la distance mise à jour à travers les différentes cellules composant la somme.

###  	3\. Créer une vue V\_Client55 qui ne contient que les clients âgés de plus de 55 ans.

	  
CREATE VIEW V\_Client55 AS SELECT CodeC, Prenom, Nom FROM  
   client  
   WHERE age\>55;

### 4\. Insérer dans cette vue un nouveau client âgé de 50\. Essayer ensuite de retrouver ce client au moyen de la vue V\_Client55 puis au moyen de la table Client.

	  
SET SQL\_SAFE\_UPDATES \= 0;  
INSERT INTO V\_Client55  
(CodeC, Prenom, Nom, age)  
VALUES  
('C979', 'Thierry', 'Fontaine', 50);  
SET SQL\_SAFE\_UPDATES \= 1;  
SELECT \* FROM v\_client55 WHERE CodeC\='C979';  
SELECT \* FROM client WHERE CodeC\='C979';  
Le nouveau client a bien été inséré via v\_client55, mais n’est pas visible par celle-ci grâce à ses conditions. Il est retrouvable via client.

## 3\. Droits d’accès

### 1\. Ajouter une nouvelle table « ACESS » pour le contrôle d’accès (login, password, user\_id, access\_level). Le niveau d’accès peut prendre la valeur suivante : L(lecture), E(écriture), U(update), D(delete) ou T(total), le champs user\_id est à incrémenter automatiquement.

CREATE TABLE ACCESS (  
user\_id INT AUTO\_INCREMENT PRIMARY KEY,  
login VARCHAR(100),  
password VARCHAR(100),  
access\_level ENUM('L', 'E', 'U', 'D', 'T') NOT NULL  
);

### 2\. Remplir la table ACCESS avec les clients : login \=\> nom.prenom et password \=\> généré automatiquement (fonction Md5). La valeur par défaut pour l’attribut access\_level est « L ». Ajouter les propriétaires avec comme login « email » et comme access\_level « E ».

Il serait intéressant de demander lors de leur prochain connexion de remplir un prénom aux client qui ne l’ont pas renseigné et de mettre en place un trigger qui met à jour la cellule login quand les colonnes nom et prenom sont modifiées.

INSERT INTO ACCESS  
(login, password, access\_level)  
SELECT CONCAT(Nom,'.',Prenom), MD5(RAND(10)), 'L' FROM client ;  
INSERT INTO ACCESS  
(login, password, access\_level)  
SELECT email, MD5(RAND(10)), 'E' FROM proprietaire ;

### 3\. Créer plusieurs utilisateurs (vous pouvez utiliser la fonctionnalité ADD account sur Workbench) :

#### a. Avec des droits de lectures limités sur quelques tables.

CREATE USER 'visitor'@'localhost' IDENTIFIED BY 'visitor';  
GRANT SELECT ON locauto.location  
TO 'visitor'@'localhost';  
GRANT SELECT ON locauto.voiture  
TO 'visitor'@'localhost';

#### b. Avec des droits de modifications (insert et update) sur quelques tables.

CREATE USER 'userP'@'localhost' IDENTIFIED BY 'userP';  
GRANT SELECT, INSERT, UPDATE ON locauto.client  
TO 'userP'@'localhost';  
GRANT SELECT, INSERT, UPDATE ON locauto.proprietaire  
TO 'userP'@'localhost';  
GRANT SELECT, INSERT, UPDATE ON locauto.voiture  
TO 'userP'@'localhost';

#### c. Avec la totalité des droits. Ce dernier aura le droit de partager ses droits.

CREATE USER 'admin'@'localhost' IDENTIFIED BY 'admin';  
GRANT ALL PRIVILEGES ON locauto.\*  
TO 'admin'@'localhost';

### 4\. Se connecter avec chaque utilisateur et vérifier les opérations : SELECT, INSERT, UPDATE et DELETE.

SELECT \* FROM client;  
INSERT INTO proprietaire (codeP, Pseudo, email, ville, anneeI) VALUES ('C989', 'MonsieurPhi', 'monsieurPhi', 'Meaux', 2025);  
UPDATE ACCESS SET access\_level \= 'T' WHERE user\_id\=1;  
DELETE FROM ACCESS WHERE user\_id\=2;

En se connectant avec chaque utilisateur et en executant ces différentes requêtes, les droits bloquent bien l’execution des requêtes.

## 4\. Accès concurrents

### 1\. Proposer un use case dans lequel vous générez un problème de mise à jour perdue.

		  
	Le niveau d’isloation doit être read uncommited.

1\. N’importe quelle session  
SELECT km FROM location WHERE CodeL \= 1;  
		Output : 37

		2\. Session root  
SET @km \= 0;  
SELECT km into @km FROM location WHERE CodeL \= 1;

		3\. Session admin  
SET @km \= 0;  
SELECT km into @km FROM location WHERE CodeL \= 1;  
		  
		4\. Session root  
UPDATE location SET km \= @km \+ 800 WHERE CodeL\=1;

		5\. Session admin  
UPDATE location SET km \= @km \+ 120 WHERE CodeL\=1;

		6\. N’importe quel session  
SELECT km FROM location WHERE CodeL \= 1;  
		Output : 157

###  	2\. Même question que (1) mais pour une lecture sale.

		  
	Le niveau d’isolation doit être read repeatable au maximum

1\. N’importe quelle session  
SELECT km FROM location WHERE CodeL \= 3;  
		Output : 70

		2\. Session root  
SET @km \= 0;  
SELECT km into @km FROM location WHERE CodeL \= 3;  
UPDATE location SET km \= @km \+ 800 WHERE CodeL\=3;

		3\. Session admin  
SET @km \= 0;  
SELECT km into @km FROM location WHERE CodeL \= 3;  
		  
		4\. Session root  
		En condition réel :   
ROLLBACK;  
		  
		Dans les conditions de l’exercice :  
UPDATE location SET km \= @km \- 800 WHERE CodeL\=3;

		5\. Session admin  
UPDATE location SET km \= @km \+ 120 WHERE CodeL\=3;

		6\. N’importe quel session  
SELECT km FROM location WHERE CodeL \= 3;  
		Output : 920

### 3\. Étudier la requête « SELECT FOR UPDATE » et proposer un exemple de son utilisation.

La requête SELECT FOR UPDATE permet de poser un verrou jusqu’à la fin de la transaction sur les cellules concernées, et ce, peu importe le niveau d’isolation en vigueur.

SET autocommit \= 0;  
SELECT km FROM location WHERE CodeL\=5 FOR UPDATE;  
UPDATE location SET km\=1000 WHERE CodeL\=5;  
COMMIT;  
SET autocommit \= 1;

## 5\. PL/SQL & Trigger

### 1\. Nous souhaitons analyser les locations et attribuer des notes automatiques selon la durée et les kilomètres parcourus. Certaines notes doivent rester nulles si les données sont incomplètes. Proposer une procédure (ex. si KM\>1000 et durée \>  50jours \=\> note 5, … si durée \=1 jour, laisser la note à NULL).

SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE location  
SET note \= CASE  
   WHEN km \> 500 OR dureeTS \> '1000-03-17 00:00:00' THEN 5  
   WHEN km \> 400 OR dureeTS \> '1000-02-20 00:00:00' THEN 4  
   WHEN km \> 300 OR dureeTS \> '1000-02-10 00:00:00' THEN 3  
   WHEN km \> 200 OR dureeTS \> '1000-01-21 00:00:00' THEN 2  
   WHEN km \> 100 OR dureeTS \> '1000-01-11 00:00:00' THEN 1  
   ELSE NULL  
END;  
SET SQL\_SAFE\_UPDATES \= 1;

CREATE TRIGGER note\_creation\_insert  
BEFORE INSERT ON location  
FOR EACH ROW  
SET new.note \= CASE  
  WHEN new.km \> 500 OR new.dureeTS \> '1000-03-17 00:00:00' THEN 5  
  WHEN new.km \> 400 OR new.dureeTS \> '1000-02-20 00:00:00' THEN 4  
  WHEN new.km \> 300 OR new.dureeTS \> '1000-02-10 00:00:00' THEN 3  
  WHEN new.km \> 200 OR new.dureeTS \> '1000-01-21 00:00:00' THEN 2  
  WHEN new.km \> 100 OR new.dureeTS \> '1000-01-11 00:00:00' THEN 1  
  ELSE NULL  
END;

CREATE TRIGGER note\_creation\_update  
BEFORE UPDATE ON location  
FOR EACH ROW  
SET new.note \= CASE  
  WHEN new.km \> 500 OR new.dureeTS \> '1000-03-17 00:00:00' THEN 5  
  WHEN new.km \> 400 OR new.dureeTS \> '1000-02-20 00:00:00' THEN 4  
  WHEN new.km \> 300 OR new.dureeTS \> '1000-02-10 00:00:00' THEN 3  
  WHEN new.km \> 200 OR new.dureeTS \> '1000-01-21 00:00:00' THEN 2  
  WHEN new.km \> 100 OR new.dureeTS \> '1000-01-11 00:00:00' THEN 1  
  ELSE NULL  
END;

### 2\. Compléter la procédure ou créer une autre procédure pour mettre à jour le champs « avis ». Par exemple : si la note est \>=4, l’avis sera « très satisfait », … si la note est « null », l’avis sera « non évalué ».

SET SQL\_SAFE\_UPDATES \= 0;  
UPDATE location  
SET avis \= CASE  
   WHEN note \> 4 THEN "Très bien"  
   WHEN note \> 3 THEN "Bien"  
   WHEN note \> 2 THEN "Moyen"  
   WHEN note \> 1 THEN "Médiocre"  
   WHEN note \> 0 THEN "Nul"  
   ELSE NULL  
END;  
SET SQL\_SAFE\_UPDATES \= 1;

CREATE TRIGGER avis\_creation\_insert  
BEFORE INSERT ON location  
FOR EACH ROW  
SET new.avis \= CASE  
  WHEN new.note \> 4 THEN "Très bien"  
  WHEN new.note \> 3 THEN "Bien"  
  WHEN new.note \> 2 THEN "Moyen"  
  WHEN new.note \> 1 THEN "Médiocre"  
  WHEN new.note \> 0 THEN "Nul"  
  ELSE NULL  
END;

CREATE TRIGGER avis\_creation\_update  
BEFORE UPDATE ON location  
FOR EACH ROW  
SET new.avis \= CASE  
  WHEN new.note \> 4 THEN "Très bien"  
  WHEN new.note \> 3 THEN "Bien"  
  WHEN new.note \> 2 THEN "Moyen"  
  WHEN new.note \> 1 THEN "Médiocre"  
  WHEN new.note \> 0 THEN "Nul"  
  ELSE NULL  
END;

### 3\. Ajouter une procédure qui permet d’analyser les locations pour un client donné en paramètre. Par exemple : il faut calculer la durée totale de location, nombre de véhicules différents loués, la moyenne des notes.

DELIMITER //

CREATE PROCEDURE analyse\_client  
(  
IN CodeCParam VARCHAR(4),  
OUT avgnote FLOAT,  
OUT countloc INT,  
OUT totkm INT,  
OUT totduree INT,  
OUT nbvoit INT  
)  
BEGIN  
   SELECT AVG(note) INTO avgnote FROM location WHERE CodeC\= CodeCParam;  
   SELECT COUNT(CodeC) INTO countloc FROM location WHERE CodeC\= CodeCParam;  
   SELECT SUM(km) INTO totkm FROM location WHERE CodeC\= CodeCParam;  
   SELECT SUM(duree \- '1000-01-02 00:00:00') INTO totduree FROM location WHERE CodeC\= CodeCParam;  
   SELECT COUNT(DISTINCT(immat)) INTO nbvoit FROM location WHERE CodeC\= CodeCParam;  
END//

DELIMITER ;

SET @avgnote \= 0.00;  
SET @countloc \= 0;  
SET @totkm \= 0;  
SET @totduree \= 0;  
SET @nbvoit \= 0;  
CALL analyse\_client('C654', @avgnote, @countloc, @totkm, @totduree, @nbvoit);  
SELECT 'C654' AS CodeC, @avgnote, @countloc, @totkm, @totduree, @nbvoit;

### 4\. Une voiture peut avoir plusieurs états (disponible, en réparation, en location, …). Proposer une solution pour vérifier l’état d’une voiture avant la location et après le retour de location (ajouter la colonne « etat » dans la table voiture).

ALTER TABLE voiture  
ADD COLUMN etat ENUM('disponible','en reparation','en location','pas retournée');

DELIMITER //  
CREATE PROCEDURE check\_availability(  
  IN demandimmat VARCHAR(6),  
  OUT availability VARCHAR(25)  
)  
BEGIN  
  SET @immatstate \= NULL;  
  SELECT availability INTO @immatstate FROM voiture WHERE immat\=demandimmat;  
  SET availability \= CASE  
      WHEN @immatstate \= NULL THEN 'A vérifier'  
      WHEN @immatstate \= 'disponible' THEN 'Location disponible'  
      WHEN @immatstate \= 'en reparation' THEN 'Indisponible'  
      WHEN @immatstate \= 'en location' THEN 'Indisponible'  
      WHEN @immatstate \= 'pas retournée' THEN 'Indisponible'  
      ELSE 'A vérifier'  
END;  
END;//

SET @immat \= '23AA46';  
SET @response \= NULL;  
CALL check\_availability(@immat, @response);  
SELECT @response;

   
J’utilise une table de la question suivante dans l’event créé ci-dessous.

SET GLOBAL event\_scheduler \= ON;  
CREATE EVENT checkreturn  
ON SCHEDULE EVERY 1 DAY  
DO  
  SELECT a.immat, b.etat AS notreturned FROM location a JOIN voiture b ON a.immat\=b.immat WHERE a.datef\=CURRENT\_DATE();  
  INSERT INTO voitstatehistory (immat, etat, date)  
   SELECT a.immat, b.etat, CURRENT\_DATE() AS notreturned FROM location a JOIN voiture b ON a.immat\=b.immat WHERE a.datef\=CURRENT\_DATE();

### 5\. Proposer une solution automatique pour gérer l’historique de changement d’état d’une voiture.

CREATE TABLE voitstatehistory (  
   immat VARCHAR(6) NOT NULL,  
   etat enum('disponible','en reparation','en location','pas retournée'),  
   date DATETIME  
);

CREATE TRIGGER upd\_voitstatehistory  
AFTER UPDATE ON voiture  
FOR EACH ROW  
   INSERT INTO voitstatehistory (immat, state, date)  
   VALUES (new.immat, new.etat, CURRENT\_DATE);

## 6\. Application & data visualisation

### 1\. Proposer une application (ex. Python) permettant de se connecter à la base de données et d’exécuter des opérations CRUD (5 opérations par type).

J’ai choisi d’utiliser le Python avec l’IDE Spyder. Voici les 20 requêtes. Un fichier executable au nom de app&[viz.py](http://viz.py) se trouve dans le même dossier.

create \= \["CREATE TABLE locaux ( local\_id INT AUTO\_INCREMENT PRIMARY KEY, adresse VARCHAR(150));",  
         "CREATE TABLE employe ( employe\_id INT AUTO\_INCREMENT PRIMARY KEY, nom VARCHAR(25), prenom VARCHAR(25), local\_id INT, FOREIGN KEY (local\_id) REFERENCES locaux(local\_id));",  
         "INSERT INTO locaux (adresse) SELECT DISTINCT(villed) FROM location ;",  
         "INSERT INTO proprietaire (CodeP, Pseudo, email, ville, anneeI) VALUES ('P333', 'Xavier', 'xavierjobs@hotmail.fr', 'Hyeres', '2025');",  
         "INSERT INTO ACCESS (login, password, access\_level) VALUES ('Xavier.', MD5(RAND(10)), 'U');"  
         \]

read \= \["SELECT CodeP FROM proprietaire WHERE ville \= 'Paris';",  
         "SELECT COUNT(CodeL) FROM location;",  
         "SELECT COUNT(DISTINCT(villed)) FROM location;",  
         "SHOW TABLES FROM locauto;",  
         "SHOW COLUMNS FROM client;"  
         \]

update \= \["SET SQL\_SAFE\_UPDATES \= 0;",  
         "UPDATE location SET duree \= 1 WHERE duree \= 0;",  
         "UPDATE location SET villed \= 'Lyon' WHERE villed \= 'lyon';",  
         "UPDATE proprietaire SET Pseudo \= 'Marcel BIRSCH' WHERE Pseudo='Marcel3';",  
         "UPDATE client SET age \= 58 WHERE Prenom='Vincent' AND Nom='Cassel';",  
         "ALTER TABLE voitstatehistory MODIFY COLUMN immat VARCHAR(6) NOT NULL;",  
         "SET SQL\_SAFE\_UPDATES \= 1;"  
         \]

delete \= \["DELETE FROM location WHERE immat IS NULL;",  
         "ALTER TABLE location DROP COLUMN numloc;",  
         "ALTER TABLE location DROP COLUMN mois;",  
         "ALTER TABLE location DROP COLUMN annee;",  
         "DROP TABLE employe;"  
         \]

### 2\. Proposer 5 visuels différents.

df \= pd.read\_sql\_query("SELECT AVG(prixJ) AS meanPrix, marque FROM voiture GROUP BY marque ORDER BY meanPrix DESC;", mydb)  
figure1 \= px.histogram(df, x\='marque', y\='meanPrix', title\="Prix journalier moyen par marque")  
figure1.show()

df \= pd.read\_sql\_query("SELECT SUM(CodeL) AS nbloc, dated FROM location GROUP BY dated;", mydb)  
figure2 \= px.histogram(df, x\='dated', y\='nbloc', title\="Nombre de location par an")  
figure2.show()

df \= pd.read\_sql\_query("SELECT SUM(km) AS sumkm, YEAR(dated) AS year FROM location GROUP BY YEAR(dated);", mydb)  
figure3 \= px.histogram(df, x\='year', y\='sumkm', title\="Nombre de km par an")  
figure3.show()

df \= pd.read\_sql\_query("SELECT villed, SUM(CodeL) AS villedcount FROM location GROUP BY villed ORDER BY villedcount DESC;", mydb)  
figure4 \= px.histogram(df, x\='villed', y\='villedcount', title\="Top des villes de départ")  
figure4.show()

df \= pd.read\_sql\_query("SELECT villea, SUM(CodeL) AS villeacount FROM location GROUP BY villea ORDER BY villeacount DESC;", mydb)  
figure5 \= px.histogram(df, x\='villea', y\='villeacount', title\="Top des villes d'arrivée")  
figure5.show()

