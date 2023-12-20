# Architecture en microservice pour la gestion de librairie
*Par Antoine GRANGER et Gwenael ROBERT*

Ce projet contient le code partiel pour la gestion du backend d'une application de gestion de librairie. 
Il se compose des différents microservices, stockés dans des dossiers portant le même nom que le service offert. 

La gestion des microservices utilise **Docker** pour gérer les containers et les microservices peuvent communiquer entre eux par requêtes HTTP. 
De plus chacun des microservices possède sa propre base de données stockée en local.

Le déploiement de cette architecture nécessite l'installation de docker ainsi que d'un moyen d'envoyer des requêtes HTTP dans le bon format. (Les formats attendus pour les objets se trouvent dans les dossiers *models* )
Pour faciliter le test des fonctionnalités, des scripts *python* sont présents pour déployer, arrêter et nettoyer les containers, respectivement **deploy.py**, **stop.py** et **clear.py** . 

Afin de faciliter l'envoi des requêtes HTTP, une interface CLI est offert. Afin de lancer l'application il faut se placer à la racine du projet et lancer la commande suivante, a noter qu'il faut également que DockerEngine soit lancé en arrière plan.

```
python -m CLI.run
```

De plus, un fichier contenant diverses requêtes HTTP est fourni et peut être utilisé sur l'application PostMan pour envoyer et visualiser le comportement de l'application. 

NB: Afin d'ouvrir l'application en tant qu'Administrateur, il est nécessaire d'ajouter un premier administrateur par requête HTTP. Pour cette raison, il est recommandé d'utiliser les requêtes fournies plus haut. 
