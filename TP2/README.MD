# Authors: 
* **Antoine Granger**,
* **Gweanael Robert**

# TP2 - 8INF957 - Programmation objet avancée

**Université du Québec à Chicoutimi**<br>
**Département d’informatique et de mathématique**

- **Professeur** : Hamid Mcheick 
- **Groupe** : deux étudiant(e)s au maximum
- **Session** : Aut2023 
- **Date de distribution** : 03 octobre 2023
- **Pondération** : 15 points 
- **Date de remise** : 14 novembre 2023

## Objectifs

Le but de ce TP est de familiariser les étudiants avec les concepts OO avancés suivants :
- SOLID
- Cohésion et couplage
- Généricité, Héritage & Délégation
- Programmation concurrente (Multithreading)
- Diagramme de classes
- Gestion d’exceptions
- Robustesse de logiciels
- Expression Lambda, NIO
- Séparation de préoccupations, AOP (AspectJ), SOP (HyperJ), VOP
- Programmation orientée composants
- Programmation orientée microservices

## Question 4 (50%)

En utilisant le langage de programmation Python, vous devez étudier les concepts suivants et réaliser une étude de cas pour ces concepts :
- Polymorphisme, surcharge des méthodes (overloading), redéfinition des méthodes (overriding)
- Généricité
- Modularité

### À faire :

a) Montrer comment ces concepts sont offerts en Python avec des exemples exécutables.
b) Présenter les avantages de Python dans les analyses de données avec une étude de cas (code exécutable avec les données utilisées). Par exemple, comment afficher les patients ayant les label 4.

## Livrables :

i. Implantation d'exemples en Python pour démontrer ces concepts. (70%)
ii. Un document word expliquant comment vous avez implémenté ces concepts et présentant également les avantages de Python en analyse de données à travers des exemples. (20%)
iii. Ce fichier README contenant vos noms. (10%)
iv. Ensemble du travail fourni dans un fichier .zip.

## Remarques :

Pour tester le code, vous pouvez Utiliser la commande 
```
python deploy.py
```

Puis installer postman et importer le fichier : ***Library_management_system.postman_collection.json***

Vous devrez ensuite ajouter un utilisateur dans la base de données du système pour pouvoir vous authentifier.
Dans postman, aller dans /users/post user et cliquez sur **Post User**
Dans body, entrer les informations suivantes :
```json
{
    "username": "toto",
    "password": "password",
    "role": "admin"
}
```
et cliquer sur **Send**

Ensuite, vous pouvez vous authentifier avec les nouvelles identifiants
Dans postman, aller dans /api_gateway/login et et renseigner les identifiants dans le body.
```json
{
    "username": "toto",
    "password": "password"
}
```

Un token est renvoyé par le serveur
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRvdG8iLCJyb2xlIjoiYWRtaW4ifQ.MIzcT7Y_P3BXVXS_ilskIHbuWS85M0SJVFvh8TqThVw"
}
```

Dans postman, aller le champs **Authorization** des requêtes dans /api_gateway avec la catégorie **Bearer token**.
Le token ci dessus devrais déjà être renseigner par defaut.
Maintenant vous pouvez tester le code à traves des exemples de requetes HTTP.