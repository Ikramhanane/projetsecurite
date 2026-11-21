# CryptoBox — TP1

Application web locale pour expérimenter trois chiffrements classiques :

- César ;
- substitution alphabétique ;
- transposition par colonnes.

## Technologies

- Python 3 pour les algorithmes et le serveur local.
- HTML et CSS pour l'interface.
- JavaScript pour les interactions et les requêtes vers Python.

Aucune bibliothèque de cryptographie.
Aucun paquet externe à installer.

## Lancement sous Windows

Dans le dossier du projet :

```powershell
py app.py
```

Ouvrir ensuite :

```text
http://127.0.0.1:8000
```

Pour arrêter le serveur : `Ctrl+C` dans le terminal.

Si `py` n'est pas disponible mais que `python` lance Python 3 :

```powershell
python app.py
```

L'interface doit être ouverte depuis le serveur, pas par un double-clic
sur index.html et pas avec Live Server.

## Tests

```powershell
py -m unittest -v
```

## Organisation

| Fichier | Rôle |
|---|---|
| crypto.py | Algorithmes et validation des entrées |
| app.py | Serveur local et API de calcul |
| index.html | Interface HTML, CSS et JavaScript |
| test_crypto.py | Tests automatiques |
| .gitignore | Fichiers exclus du dépôt |

## Fonctionnalités

### César

- Chiffrement et déchiffrement.
- Clé entière ramenée modulo 26.
- Force brute testant les 25 clés de 1 à 25.
- Affichage d'une seule proposition avec sa clé.
- Fragment connu facultatif pour aider la sélection.

La sélection automatique utilise un petit lexique et les fréquences
des lettres françaises. Elle n'est pas infaillible.

Elle peut échouer pour un mot court, un nom propre, un message
non français ou une suite de lettres aléatoires.

La clé 0 est utilisable en chiffrement et en déchiffrement manuel,
mais elle n'est pas incluse dans les 25 essais demandés par le TP.

### Substitution

La clé doit être une permutation des 26 lettres A à Z.

La première lettre de la clé remplace A, la deuxième remplace B, etc.

### Transposition

- Écriture du message en lignes sous le mot-clé.
- Complément de la dernière ligne par des X.
- Lecture des colonnes dans l'ordre alphabétique du mot-clé.
- En cas de lettres identiques dans le mot-clé :
  priorité à la colonne la plus à gauche.

Le déchiffrement conserve les X finaux, car ils peuvent appartenir
au véritable message.

## Exemples du TP

| Algorithme | Message | Clé | Résultat |
|---|---|---|---|
| César | BONJOUR | 3 | ERQMRXU |
| Substitution | ATTAQUE | QWERTYUIOPASDFGHJKLZXCVBNM | QZZQJXT |
| Transposition | RENDEZVOUSAMIDI | PORTE | ESIEVMRZANOIDUD |

## Conventions

- Messages non vides.
- Lettres A à Z uniquement.
- Sans espaces, accents, chiffres ou ponctuation.
- Aucune suppression silencieuse des caractères invalides.

L'interface limite les messages à 10 000 lettres.

## Utilisation pour un message à plusieurs couches

Retirer les couches dans l'ordre inverse du chiffrement.

Le bouton « Utiliser ce résultat comme message » permet de préparer
l'étape suivante. Choisir ensuite l'algorithme et l'opération adaptés.

Ne pas supprimer automatiquement les X entre les couches.

## Limites et sécurité

Serveur lié à 127.0.0.1 pour une utilisation locale pédagogique.
Ce serveur n'est pas destiné à une mise en production sur Internet.

Les chiffrements étudiés ne doivent pas être utilisés pour protéger
des données sensibles.

## Travail en binôme

Chaque membre utilise son identité Git et effectue ses propres commits.

Les contributions doivent correspondre à de véritables modifications,
tests ou améliorations comprises par leur auteur.