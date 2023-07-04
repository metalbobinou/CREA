# Scrapping

La première étape du processus consiste à récupérer la base de donnée qui sera ensuite nettoyée, puis traitée. Pour cela, nous procédons à la récupération semi-automatique des documents de la Bibliothèque nationale de France (BnF).
Les documents qui nous intéressent seront ici les documents provenant des collections de Gallica consacrée à « Littérature jeunesse », et plus particulièrement la presse enfantine.

## Pyllicalabs
Pyllica est un outil écrit en Python permettant de récupérer des documents hébergés sur la bibliothèque numérique Gallica. Il permet notamment de constituer rapidement de grands corpus afin d'effectuer des analyses assistées par ordinateur (statistique textuelles, text mining, reconnaissance d'image).
Il est disponible ici : https://github.com/Dorialexander/Pyllica

## Les problèmes de pyllica

### Limitation de requête
Chaque élément récupéré est une requête server différente, or une limitation du nombre de requête par personne et par minute est activée. Il faut donc utiliser une méthode permettant d'attendre un certain temps entre chaque appel 
à `textpress`.

Résolution du problème : Job Cron.

### Sélection des dates
L'option `rate` de la fonction `textpress` permet de sélectionner le temps en jour entre deux publications. Les problèmes que cette option posent sont:
- Les sorties basées sur le mois et pas le jour ("Tous les premier lundi du mois", "Tous les 1er du mois").
- Les exceptions (L'une des ressources est publiée tous les 1er du mois, mais parfois des numéros spéciaux sont publiés le 15).
- La gestion de la fréquence de parution de chaque document rajoutant encore du contenu à la base de donnée.

Résolution du problème : Incrément manuel + Récupération manuelle des exceptions + Sélection du temps en **mois** entre 2 publications, et pas en **jour**

## Job Cron

cron est un programme (Unix) permettant d'exécuter automatiquement des scripts selon un cycle défini à l'avance.
C'est une bonne manière de récupérer les ressources sans excéder la limite de requêtes, à condition de connaitre au moment de l'exécution à quel stade nous en sommes, pour pouvoir avancer la date à chaque fois.

Pour cela, on utilise quatre fichiers dans get_text/.
- get_text.sh : Le script qui sera exécuté par cron, se contentant d'appeller get_text.py
- get_text.py : Le programme python présenté plus bas.
- get_text.txt : Le fichier contenant les informations permettant de récupérer les dates de début et de fin. Il contient également l'index du texte dans la base de donnée, et l'index auquel arrêter la récupération (L'objectif étant de séparer le travail sur plusieurs postes).
- all_texts.txt : Base de donnée de la partie Scrapping, fichier contenant les noms et liens des documents à récupérer. Le fichier contient également les informations permettant d'initialiser `get_text.txt` pour chaque document.

On utilise ensuite dans un terminal `crontab -e` nous permettant de définir le cycle comme suit : `*/n * * * * /.../get_text.sh` pour appeller le script toutes les n minutes.

Il semble qu'un appel par minute soit accepté, nous pourrions en vouloir plus en utilisant `* * * * * /.../get_text.sh & sleep 30 ; /.../get_text.sh` pour avoir un appel toutes les 30 secondes par exemple.


## Incrément manuel

La méthode la plus simple pour récupérer toutes les ressources est de lancer la récupération sur tous les jours de la période sélectionnée, du 01/01/1870 au 31/12/1919.

Seulement, l'incrément manuel pose un problème de temps car il est beaucoup moins précis. Il nécessiterai 335 jours pour récupérer tous les documents possibles. Il faut donc se tourner vers une méthode plus efficace et spécialisée, où le `get_text.txt` serait modifié par le `all_text.txt` pour l'adapter à chaque texte.

## Gestion des erreurs

Un problème que nous pouvons rencontrer avec cette fonction concerne le comportement suivant:
- textpress est appelé sur une journée ne comportant pas de document à récupérer
- la fonction retourne une erreur, qui arrête l'exécution du code
- l'incrémentation n'est pas atteinte, le code tente alors de récupérer le document de la journée en boucle.

Pour éviter cette situation, on effectue l'incrémentation avant de faire la requête.
