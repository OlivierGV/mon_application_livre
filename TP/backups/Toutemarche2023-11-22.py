##################################################################
## Mes importations ##############################################
##################################################################

import sys
import mysql.connector
from PyQt5.QtWidgets import *
# Importer la classe Ui_MainWindow du fichier demo.py
from monui import Ui_MainWindow

cnx = mysql.connector.connect(
    user ='root', 
    password = '',
    host ='localhost',
    database ='travail_pratique')

##################################################################
## Mes fonctions externes ########################################
##################################################################

## Dernière Update : 2023-11-22 11:42
## État : Fonctionnel
def montrer_les_livres(self):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT nom FROM livre"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # REMPLIR
    les_livres = [resultat['nom'] for resultat in resultats]
    self.comboBox_livre.clear()
    self.comboBox_livre.addItems(map(str, les_livres))

def ecraser_une_sauvegarde(self):
    cursor = cnx.cursor(dictionary=True)
    # PERSONNAGE ACTIF
    nom_personnage_actif = trouver_personnage(self)
    id_personnage_actif = trouver_id_personnage(self, nom_personnage_actif)

    # SQL
    
    query = f"SELECT id FROM partie WHERE id_personnage = {id_personnage_actif} ORDER BY id ASC;"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # REMPLIR
    les_sauvegardes = [resultat['id'] for resultat in resultats]
    self.comboBox_choisir_sauvegarde_ecraser.clear()
    self.comboBox_choisir_sauvegarde_ecraser.addItems(map(str, les_sauvegardes))

    cursor.close()

def nouvelle_sauvegarde(self):
    #récupérer chapitre
    id_chapitre = self.label_titre_chapitre.text()

    #récupérer personnage
    personnage = self.label_personnage.text()
    if(personnage == '**Personnage**'):
        personnage = 'Salazzar Serpentard'
    id_personnage = trouver_id_personnage(self, personnage)

    #récupérer livre
    livre = self.label_titre_livre.text()
    if(livre == '**Titre livre**'):
        livre = 'Les Maîtres des Ténèbres'
    id_livre = trouver_id_livre(self, livre)

    #insérer dans la table
    try:
        inserer_sauvegarde_partie(id_chapitre, id_personnage, id_livre)
    #confirmer la save
    except Exception as e:
        msg = QMessageBox()
        msg.setWindowTitle("Problème de sauvegarde")
        msg.setText("Erreur : " + e)
        msg.exec_()
        print('chapitre : ' + id_chapitre)
        print('livre: ' + id_livre)
        print('id_personnage: ' + id_personnage)

def inserer_sauvegarde_partie(id_chapitre, id_livre, id_personnage):
    cursor = cnx.cursor(dictionary=True)

    query = f"INSERT INTO partie VALUES (DEFAULT, '{id_chapitre}', '{id_livre}', '{id_personnage}');"

    try:
        cursor.execute(query)
        cnx.commit()
    except Exception as e:
        print(f"Échec : {e}")

    cursor.close()

## Dernière Update : 2023-11-22 11:42
## État : Fonctionnel
def trouver_personnage(self):
    cursor = cnx.cursor(dictionary=True)

    query = "SELECT nom FROM personnage LIMIT 1;"

    cursor.execute(query)

    resultat = cursor.fetchone()

    if(resultat):
        self.label_personnage.setText(resultat['nom'])
        return resultat['nom']
    
    cursor.close()

## Dernière Update : 2023-11-22 11:43
## État : Fonctionnel
def trouver_livre(self):

    cursor = cnx.cursor(dictionary=True)

    query = "SELECT nom FROM livre LIMIT 1;"

    cursor.execute(query)

    resultat = cursor.fetchone()

    if(resultat):
        self.label_titre_livre.setText(resultat['nom'])
        return resultat['nom']
    cursor.close()

def remplir_textbox(self):
    
    cursor = cnx.cursor(dictionary=True)
    # récupérer le chapitre actuelle
    chapitre_actuel = self.label_titre_chapitre.text()
    if(chapitre_actuel == '**chapitre**'):
        self.label_titre_chapitre.setText("Avertir le roi")
        self.textEdit_texte.setPlainText('Au nord du royaume du Sommerlund, il est de tradition depuis des siècles d\'envoyer les fils des Seigneurs de la Guerre au monastère Kaï. C\'est là qu\'on leur enseigne l\'art et la science de leurs nobles ancêtres. Les Moines Kaï sont de grands maîtres dans l\'art qu\'ils enseignent. Pour transmettre leurs connaissances, ils doivent faire subir à leurs disciples de rudes épreuves au cours de leur apprentissage, mais ces derniers ne s\'en plaignent jamais. Ils leur témoignent au contraire amour et respect, sachant très bien qu\'ils quitteront un jour le monastère en possédant tous les secrets de la tradition Kaï: ils pourront alors rentrer chez eux, l\'esprit et le corps formés aux techniques de la guerre. Profondément attachés à leur patrie, ils seront ainsi prêts à la défendre contre le danger constant qui la menace : la soif de conquête des Maîtres des Ténèbres venus de l\'ouest. Au temps jadis, à l\'époque de la Lune Noire, les Maîtres des Ténèbres menèrent une guerre sans merci contre le royaume du Sommerlund. Ce fut une longue et douloureuse épreuve de force à l\'issue de laquelle les guerriers du Sommerlund remportèrent la victoire lors de la grande bataille de Maaken. Le roi Ulnar et ses alliés de Durenor anéantirent l\'armée des Maîtres des Ténèbres dans le défilé de Moytura et précipitèrent l\'ennemi au fond de la gorge de Maaken. Vashna, le plus puissant parmi les Maîtres des Ténèbres, périt d\'un coup mortel que le roi Ulnar lui porta de sa puissante épée, l\'Epée du Soleil, que l\'on désigne généralement sous le nom de «Glaive de Sommer». Depuis ce temps, les Maîtres des Ténèbres ont juré de prendre leur revanche sur le royaume du Sommerlund et la Maison d\'Ulnar. Lorsque l\'aube se lève sur le premier jour de votre aventure, tous les Seigneurs Kaï sont présents au monastère : on doit, en effet, célébrer aujourd\'hui même la grande fête de Fehmarn et l\'on se prépare tôt le matin aux réjouissances. Mais soudain, un immense nuage noir s\'élève au ciel d\'occident: d\'énormes   créatures aux ailes sombres emplissent les nues en si grand nombre que le soleil semble s\'éteindre. Cette invasion porte la marque des Maîtres des Ténèbres. Les ennemis jurés du Royaume du Sommerlund passent une nouvelle fois à l\'attaque : la guerre a recommencé. En ce matin fatal, Loup Silencieux (c\'est le nom qui vous a été donné par les Moines Kaï) est allé chercher du bois dans la forêt : c\'est la corvée qu\'on vous a assignée pour vous punir de votre inattention en classe. Or, sur le chemin du retour, vous apercevez tout à coup ce gigantesque nuage de créatures noires qui fond sur le monastère et semble l\'engloutir aussitôt. Vous laissez tomber votre bois à terre et vous vous précipitez sur le lieu de la bataille. Mais les monstres noirs ont obscurci le soleil et il fait à présent si sombre que vous trébuchez contre une racine en tombant tête la première. Dans votre chute, vous heurtez violemment du front une branche basse qui vous assomme. Une fraction de seconde avant de perdre connaissance, vous avez cependant le temps de saisir du regard un terrifiant spectacle: les murs du monastère Kaï sont en train de s\'écrouler sur eux-mêmes dans un fracas de tonnerre. Vous ne reprenez conscience qu\'au bout de plusieurs heures et, les larmes aux yeux, vous contemplez avec horreur le tas de ruines que l\'ennemi a laissé derrière lui. Les Guerriers Kaï ont été ensevelis sous les décombres et il ne reste plus aucun survivant parmi vos compagnons. Avec une infinie douleur, vous levez alors votre visage vers le ciel, à nouveau clair, et vous faites le serment de venger la mort des Moines et des Seigneurs Kaï. Vous ferez payer leur crime aux Maîtres des Ténèbres ! Votre tâche d\'ailleurs commence à l\'instant même : il vous faut, en effet, gagner la capitale du royaume pour prévenir le Roi en personne de l\'effroyable péril qui menace le pays ; car maintenant, l\'ennemi est en marche, et si vous n\'agissez pas à temps, votre patrie tombera sous son joug. Vous êtes le dernier des Seigneurs Kaï et le sort de votre peuple repose désormais entre vos seules mains: le Loup Silencieux est devenu Loup Solitaire et les envahisseurs feront tout pour vous empêcher d\'atteindre le Palais du Roi...')
        chapitre_actuel = 1
    else:
        # récupérer les lien_chapitre avec ce chapitre
        query = f"SELECT texte FROM chapitre WHERE no_chapitre = {chapitre_actuel};"
        cursor.execute(query)

        # Récupérer le résultat de la requête
        resultat = cursor.fetchone()

        # Vérifier si le résultat est non nul avant de l'afficher
        if resultat:
            self.textEdit_texte.setPlainText(resultat['texte'])
        else:
            self.textEdit_texte.setPlainText("Aucun texte trouvé pour ce chapitre.")
    cursor.close()

## Dernière Update : 2022-11-22 11:40
## État : Fonctionnel
def remplir_combobox_textbox_chapitre(self):
    
    cursor = cnx.cursor(dictionary=True)
    # récupérer le chapitre actuelle
    chapitre_actuel = self.label_titre_chapitre.text()
    if(chapitre_actuel == "Avertir le roi"):
        self.comboBox_choisir_chapitre.clear()
        self.comboBox_choisir_chapitre.addItems(['1'])
    else:
        # récupérer les lien_chapitre avec ce chapitre
        query = f"SELECT no_chapitre_destination FROM lien_chapitre WHERE no_chapitre_origine = {chapitre_actuel};"
        cursor.execute(query)

        # récupérer les éléments de la colonne no_chapitre_destination
        resultats = cursor.fetchall()
        if(resultats):
            chapitres_destination = [resultat['no_chapitre_destination'] for resultat in resultats]
            # afficher ces liens_chapitre dans le combo box
            self.comboBox_choisir_chapitre.clear()
            self.comboBox_choisir_chapitre.addItems(map(str, chapitres_destination))
        else:
            # Si aucun chapitre, demander de terminer l'aventure
            self.comboBox_choisir_chapitre.clear()
            self.comboBox_choisir_chapitre.addItems(['Terminer l\'histoire.'])
        
        remplir_textbox(self)

    cursor.close()

def remplir_armes(self):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT nom FROM arme;"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # REMPLIR
    les_armes = [resultat['nom'] for resultat in resultats]
    self.comboBox_arme1.clear()
    self.comboBox_arme1.addItems(map(str, les_armes))
    self.comboBox_arme2.clear()
    self.comboBox_arme2.addItems(map(str, les_armes))

    cursor.close()

def remplir_disciplines(self):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT nom FROM discipline_kai;"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # REMPLIR
    les_kai = [resultat['nom'] for resultat in resultats]
    self.comboBox_kai1.clear()
    self.comboBox_kai1.addItems(map(str, les_kai))
    self.comboBox_kai2.clear()
    self.comboBox_kai2.addItems(map(str, les_kai))
    self.comboBox_kai3.clear()
    self.comboBox_kai3.addItems(map(str, les_kai))
    self.comboBox_kai4.clear()
    self.comboBox_kai4.addItems(map(str, les_kai))
    self.comboBox_kai5.clear()
    self.comboBox_kai5.addItems(map(str, les_kai))

    cursor.close()

## Dernière Update : 2023-11-22 11:38
## État : Fonctionnel
def remplir_disciplines_armes_creation(self):
    remplir_armes(self)
    remplir_disciplines(self)

def insert_personnage(personnage, endurance, habilete):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"INSERT INTO personnage VALUES (DEFAULT, '{personnage}', {endurance}, {habilete});"
    try:
        cursor.execute(query)
        cnx.commit()
    except Exception as e:
        print(f"Échec : {e}")

    cursor.close()

def trouver_id_personnage(self, personnage):
    nom_du_personnage = personnage
    print(nom_du_personnage)
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT id FROM personnage WHERE nom = '{personnage}' LIMIT 1;"
    cursor.execute(query)
    resultat = cursor.fetchone()
    #return resultat['id']
    return resultat['id']

def trouver_id_livre(self, livre):
    cursor = cnx.cursor(dictionary=True)
    # SQL
    
    query = f"SELECT id FROM livre WHERE nom = '{livre}' LIMIT 1;"
    cursor.execute(query)
    resultat = cursor.fetchone()
    return resultat['id']
    cursor.close()

def insert_sac_a_dos(personnage_id, obj, repas, obj_spe):
    cursor = cnx.cursor(dictionary=True)
    # SQL
    print(personnage_id)
    print(obj)
    print(repas)
    print(obj_spe)
    
    query = f"INSERT INTO sac_a_dos VALUES (DEFAULT, 'abc', 'abc', 'abc', DEFAULT, {personnage_id});"
    try:
        cursor.execute(query)
        cnx.commit()
    except Exception as e:
        print(f"Échec : {e}")

    cursor.close()

def insert_perso_kai(personnage_id, id_kai):
    cursor = cnx.cursor(dictionary=True)
    # SQL
    
    query = f"INSERT INTO personnage_kai VALUES (DEFAULT, {id_kai}, {personnage_id}, DEFAULT);"
    try:
        cursor.execute(query)
        cnx.commit()
        print("Succès kai")
    except Exception as e:
        print(f"Échec : {e}")

    cursor.close()

def insert_perso_arme(personnage_id, id_arme):
    cursor = cnx.cursor(dictionary=True)
    # SQL
    
    query = f"INSERT INTO personnage_arme VALUES (DEFAULT, {id_arme}, {personnage_id});"
    try:
        cursor.execute(query)
        cnx.commit()
        print("Succès arme")
    except Exception as e:
        print("echec arme")
        print(f"Échec : {e}")

    cursor.close()

def trouver_id_kai(nom_kai):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT id FROM discipline_kai WHERE nom = '{nom_kai}' LIMIT 1;"
    cursor.execute(query)
    resultat = cursor.fetchone()
    return resultat['id']
    cursor.close()

def trouver_id_arme(nom_arme):
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT id FROM arme WHERE nom = '{nom_arme}' LIMIT 1;"
    cursor.execute(query)
    resultat = cursor.fetchone()
    return resultat['id']

    cursor.close()

###########
## TO DO ##
###########
def remplir_inventaire(self):
    # PERSONNAGE
    personnage = trouver_personnage(self)
    id_personnage = trouver_id_personnage(self, personnage)

    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT objets, repas, objets_speciaux, bourse FROM sac_a_dos WHERE id_personnage = {id_personnage} LIMIT 1;"
    cursor.execute(query)
    resultats = cursor.fetchone()

    # REMPLIR
    self.plainTextEdit_objets_inv.setPlainText(resultats['objets'])
    self.plainTextEdit_repas_inv.setPlainText(resultats['repas'])
    self.plainTextEdit_objspe_inv.setPlainText(resultats['objets_speciaux'])
    self.spinBox_bourse.setValue(resultats['bourse'])

    cursor.close()

def remplir_endurance_habilete(self):
    cursor = cnx.cursor(dictionary=True)
    # PERSONNAGE
    personnage = trouver_personnage(self)
    id_personnage = trouver_id_personnage(self, personnage)

    # SQL
    
    query = f"SELECT endurance, habilete FROM personnage WHERE id = {id_personnage} LIMIT 1;"
    cursor.execute(query)
    resultats = cursor.fetchone()

    # REMPLIR
    print(resultats['endurance'])
    print(resultats['habilete'])
    self.label_endurance.setText("EN - " + str(resultats['endurance']))
    self.label_habilete.setText("HA - " + str(resultats['habilete']))

    cursor.close()

def remplir_kai_personnage(self):
    # PERSONNAGE
    personnage = trouver_personnage(self)
    id_personnage = trouver_id_personnage(self, personnage)
    print(id_personnage)
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT discipline_kai.nom FROM personnage_kai INNER JOIN discipline_kai ON personnage_kai.id_kai = discipline_kai.id WHERE personnage_kai.id_personnage = {id_personnage};"
    cursor.execute(query)
    resultats = cursor.fetchall()
    print(resultats)

    # REMPLIR
    les_kai = [resultat['nom'] for resultat in resultats]
    self.comboBox_inv_kai.clear()
    self.comboBox_inv_kai.addItems(map(str, les_kai))

    cursor.close()

def remplir_arme_personnage(self):
    # PERSONNAGE
    personnage = trouver_personnage(self)
    id_personnage = trouver_id_personnage(self, personnage)
    print(id_personnage)
    # SQL
    cursor = cnx.cursor(dictionary=True)
    query = f"SELECT arme.nom FROM personnage_arme INNER JOIN arme ON personnage_arme.id_arme = arme.id WHERE personnage_arme.id_personnage = {id_personnage};"
    cursor.execute(query)
    resultats = cursor.fetchall()
    print(resultats)

    # REMPLIR
    mes_armes = [resultat['nom'] for resultat in resultats]
    self.comboBox_inv_arme.clear()
    self.comboBox_inv_arme.addItems(map(str, mes_armes))

    cursor.close()

## Dernière Update : 2023-11-22 12:00
## État : L'id du personnage est mauvais
def montrer_les_sauvegardes(self):
    cursor = cnx.cursor(dictionary=True)
    # PERSONNAGE ACTIF
    nom_personnage_actif = trouver_personnage(self)
    id_personnage_actif = trouver_id_personnage(self, nom_personnage_actif)

    # SQL
    
    query = f"SELECT id FROM partie WHERE id_personnage = {id_personnage_actif} ORDER BY id DESC;"
    cursor.execute(query)
    resultats = cursor.fetchall()

    # REMPLIR
    les_sauvegardes = [resultat['id'] for resultat in resultats]
    self.comboBox_sauvegardes_actives.clear()
    self.comboBox_sauvegardes_actives.addItems(map(str, les_sauvegardes))

    cursor.close()

##################################################################
## Mon application ###############################################
##################################################################

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        # initialiser la fenêtre
        self.setupUi(self)

        # Remplir les combo-box au démarrage
        remplir_combobox_textbox_chapitre(self)
        remplir_disciplines_armes_creation(self)

        # Remplir les informations de la barre latérale gauche
        trouver_personnage(self)
        trouver_livre(self)
        montrer_les_livres(self)

        # TO DO #
        montrer_les_sauvegardes(self)
        ecraser_une_sauvegarde(self)

        remplir_inventaire(self)
        remplir_endurance_habilete(self)
        remplir_kai_personnage(self)
        remplir_arme_personnage(self)

    ##################################################################
    ## Mes fonctions internes ########################################
    ##################################################################

    # Loader une save
    def charger_sauvegarde(self):
        #prendre, depuis le comboxbox numero save, le ID de la save
        id_partie = self.comboBox_sauvegardes_actives.currentText()
        #prendre, de cette partie précise (trouvée avec ID), le chapitre en cours
        cursor = cnx.cursor(dictionary=True)
        query = f"SELECT chapitre_sauvegarde FROM partie WHERE id = {id_partie} LIMIT 1;"
        cursor.execute(query)
        resultat = cursor.fetchone()
        mon_chapitre = resultat['chapitre_sauvegarde']
        #insérer le chapitre en cours dans "destination_chapitre"
        if(self.comboBox_choisir_chapitre.currentText() != 'Terminer l\'histoire.'):
            self.label_titre_chapitre.setText(mon_chapitre)
            remplir_combobox_textbox_chapitre(self)

    def ecraser_sauvegarde(self):
        #prendre l'id de la save dans le combobox
        id_save = self.comboBox_choisir_sauvegarde_ecraser.currentText()
        #prendre l'id du chapitre actuelle
        id_chapitre = self.label_titre_chapitre.text()
        #updater le tout
        cursor = cnx.cursor(dictionary=True)
        query = f"UPDATE partie SET chapitre_sauvegarde = '{id_chapitre}' WHERE id = '{id_save}';"
        try:
            cursor.execute(query)
            cnx.commit()
        except Exception as e:
            print(f"Échec : {e}")
        

    # Pouvoir quitter l'application
    def quitter_application(self):
        self.close()
        msg = QMessageBox()
        msg.setWindowTitle("Cordialement")
        msg.setText("Vos stats ont été sauvegardés, merci d'avoir joué.")
        msg.exec_()
        nouvelle_sauvegarde(self)

    # Un événement en fonction de l'option choisi dans un comboBox
    def aller_vers_chapitre(self):
        destination_chapitre = self.comboBox_choisir_chapitre.currentText()
        if(self.comboBox_choisir_chapitre.currentText() != 'Terminer l\'histoire.'):
            self.label_titre_chapitre.setText(destination_chapitre)
            remplir_combobox_textbox_chapitre(self)
        else:
            self.close()
            msg = QMessageBox()
            msg.setWindowTitle("Cordialement")
            msg.setText("Vos stats ont été sauvegardés, merci d'avoir joué.")
            msg.exec_()

    def sauvegarder_etat_partie(self):
        nouvelle_sauvegarde(self)
        montrer_les_sauvegardes(self)


    def creer_personnage(self):
        # Mettre chacune des valeurs dans des variables
        personnage = self.plainTextEdit_creer_personnage.toPlainText()
        if(personnage == ""):
            personnage = "Nom null"
        endurance = self.spinBox_endurance.value()
        habilete = self.spinBox_habilete.value()
        objets = self.plainTextEdit_objet.toPlainText()
        if(objets == ""):
            objets = "Aucun objet"
        repas = self.plainTextEdit_repas.toPlainText()
        if(repas == ""):
            repas = "Aucun repas"
        objets_spe = self.plainTextEdit_objet_spe.toPlainText()
        if(objets_spe == ""):
            objets_spe = "Aucun objet spécial"
        disciplines = [self.comboBox_kai1.currentText(), self.comboBox_kai2.currentText(), self.comboBox_kai3.currentText(), self.comboBox_kai4.currentText(), self.comboBox_kai5.currentText()]
        armes = [self.comboBox_arme1.currentText(), self.comboBox_arme2.currentText()]

        # Insérer les variables respectives dans la table personnage et la table sac_à_dos et les tables personnage_kai et personnage_arme
        insert_personnage(personnage, endurance, habilete)
        id_personnage = trouver_id_personnage(self, personnage)
        insert_sac_a_dos(id_personnage, objets, repas, objets_spe)

        #Insérer KAI
        i = 0
        for element in disciplines:
            element = trouver_id_kai(disciplines[i])
            insert_perso_kai(id_personnage, element)
            print(i)
            print(element)
            i += 1

        #Insérer ARMES
        print("boucle j")
        j = 0
        for element in armes:
            print(armes[j]) #l'arme sélectionné
            element = trouver_id_arme(armes[j])
            print(element) #id de l'arme sélectionné
            insert_perso_arme(id_personnage, element)
            j += 1

        msg = QMessageBox()
        msg.setWindowTitle("Confirmation")
        msg.setText("Le personnage a été ajouté à la base de données.")
        msg.exec_()

        # TO DO #
        # Loader la fenêtre pour se connecter au personnage?
            

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
