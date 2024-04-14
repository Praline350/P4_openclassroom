# Gestion du club d'échecs

Ce programme a pour but d'aider à la gestion générale d'un club d'échecs.  
Il permet la gestion des joueurs, des tournois et des matchs.  

## Installation

1. Téléchargez l'ensemble des packages (controller, models, views) ainsi que main.py et requirements.txt.  
2. Gardez l'ensemble des packages dans le même répertoire.

## Configuration de l'environnement virtuel

Il est conseillé de créer un environnement virtuel pour isoler les dépendances du projet. Vous pouvez suivre les étapes suivantes :  
Sur Windows :
```sh
python -m venv env
source env/Scripts/activate
pip install -r requirements.txt
```
Sur MacOS & Linux:
```sh
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```
# Fonctionnaliés  

## Les menus:  

### Menu Joueur:  
1. Vous pourrez ajouter un nouveau joueur à la base de données général des joueurs. Un nom, prénom, date de naissnace ainsi que son numéro national d'echec sera demander.
2. Vous pourrez supprimé un joueur en cas de besoin.
3. Vous pourrez également modifier les informations d'un joueur en cas d'erreur de saisi.
4. Le retour nous ramène au menu principal
5. Sortir permet de couper le programme

### Menu Tournois  
1. Vous pourrez ajouter un nouveau tournois à la base de données des tournois. Un nom, une localisation ainsi qu'une date de début et de fin sera demandé.
   Le tournoi sera présent dans le dossier data/data_tournament  
2. Vous pourrez ajouter des joueurs à un tournoi. Une liste des tournois apparait alors. Vous devrez remplir L'IDN du joueur. Si jamais l'IDN n'est pas juste, une liste de tout les joueurs apparait pour selectionner le joueur en question.
   Vous pouvez ajouter un autre joueur ou revenir au menu.
3. Vous pourrez supprimer un joueur d'un tournoi. Même fonctionnement que pour l'ajouter. Un message de validation permet d'éviter de supprimé un joueur par erreur.
4. Vous pourrez supprimer un tournoi, une liste des tournois apparait. Un message de validation permet d'éviter les erreurs.
5. Vous pourrez ajouter une description à un tournoi.
6. Et également faire une sauvegarde d'un tournoi, commmencer, en cours, ou fini.

### Jouer un tournoi
1. Choississez parmis la liste des tournois en cours ou créer un tournoi
2. Choississez entre commencer(ou continuer) le tournoi ou revenir a une sauvegarde.
3. Si le tournoi ne contient aucun joueur vous pourrez ajouter des joueurs a ce moment là.
4. Le programme demandera si vous voulez effectuer une save avant de commencer.
5. A chaque début de round les joueur sont répartie dans des matchs en fonction de leur points(ou aléaoirement pour le premier round)
6. Le programme sauvegarde l'anvancer du tournoi entre chaque round.
7. Choissisez le vainqueur (ou match nul) à chaque match. Les points de chaque match sont unique mais le score général est mis a jour a chaque match
8. A la fin des rounds le vainqueur est désigné. Le tournoi passe alors en "Tournament closed" et le vainqueur est ajouté a la data tournoi.

### Jouer un tournoi d'une backup
1. Vous pouvez jouer un tournoi directement en partant d'une sauvegarde
2. La liste des tournoi est alors donner, ainsi que celle des backup.
3. La backup selectionnée prend alors la place du tournoi.
4. Une validation est demandé, car la backup surpprimera les information du tournoi en question.
5. Le tournoi se joue alors normalement

### Rapports
1. Vous avez accès à différents rapports
2. Le rapport s'affiche alors sur la console.
3. Vous pouvez alors exporter ou non le rapport.
4. Les rapports se trouvent dans le dossier export_data

   
# Générer un rapport Flake8-Html

Pour générer un rapport flake8-html :  
1. Se placer dans le repértoire du programme
2. Activer l'environnement virtuel
3. Faite la commande suivante :
```sh
flake8 --format=html --htmldir=reports controller models views
```
Le rapport ce trouvera donc dans le dossier reports du répetoire du programme
   
