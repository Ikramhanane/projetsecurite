import json

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from crypto import (
    cesar_chiffrer,
    cesar_dechiffrer,
    proposer_cesar,
    substitution_chiffrer,
    substitution_dechiffrer,
    transposition_chiffrer,
    transposition_dechiffrer,
)


DOSSIER = Path(__file__).resolve().parent


def executer_calcul(donnees):
    if not isinstance(donnees, dict):
        raise ValueError("Format de demande incorrect.")

    champs = ("algorithme", "operation", "message", "cle", "indice")

    for champ in champs:
        if not isinstance(donnees.get(champ, ""), str):
            raise ValueError("Les champs doivent être du texte.")

    algorithme = donnees.get("algorithme", "")
    operation = donnees.get("operation", "")
    message = donnees.get("message", "")
    cle = donnees.get("cle", "")
    indice = donnees.get("indice", "")

    if len(message) > 10000:
        raise ValueError("Le message est limité à 10 000 lettres.")

    if len(cle) > 1000 or len(indice) > 10000:
        raise ValueError("La clé ou l'indice est trop long.")

    if operation not in {"chiffrer", "dechiffrer", "brute"}:
        raise ValueError("Opération inconnue.")

    if algorithme not in {"cesar", "substitution", "transposition"}:
        raise ValueError("Algorithme inconnu.")

    if operation == "brute":
        if algorithme != "cesar":
            raise ValueError(
                "La force brute est disponible uniquement pour César."
            )

        return proposer_cesar(message, indice)

    if algorithme == "cesar":
        try:
            cle_numerique = int(cle)
        except ValueError:
            raise ValueError("La clé César doit être un entier.")

        if operation == "chiffrer":
            resultat = cesar_chiffrer(message, cle_numerique)
        else:
            resultat = cesar_dechiffrer(message, cle_numerique)

        return {
            "resultat": resultat,
            "cle": cle_numerique % 26,
            "note": "Calcul effectué avec la clé indiquée."
        }

    if algorithme == "substitution":
        if operation == "chiffrer":
            resultat = substitution_chiffrer(message, cle)
        else:
            resultat = substitution_dechiffrer(message, cle)

        return {
            "resultat": resultat,
            "note": "Substitution effectuée avec votre alphabet."
        }

    if operation == "chiffrer":
        resultat = transposition_chiffrer(message, cle)
        note = "Des X sont ajoutés si la dernière ligne est incomplète."
    else:
        resultat = transposition_dechiffrer(message, cle)
        note = (
            "Les éventuels X de remplissage sont conservés. "
            "Ils ne peuvent pas être distingués automatiquement "
            "des véritables lettres du message."
        )

    return {
        "resultat": resultat,
        "note": note
    }


class Application(BaseHTTPRequestHandler):

    def envoyer_json(self, contenu, statut=200):
        contenu_encode = json.dumps(
            contenu,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(statut)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header("Content-Length", str(len(contenu_encode)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(contenu_encode)

    def do_GET(self):
        if self.path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
            return

        if self.path != "/":
            self.send_error(404)
            return

        contenu = (DOSSIER / "index.html").read_bytes()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(contenu)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(contenu)

    def do_POST(self):
        if self.path != "/api/calcul":
            self.send_error(404)
            return

        try:
            longueur = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.envoyer_json(
                {"erreur": "Taille de demande incorrecte."},
                400
            )
            return

        if not 0 < longueur <= 200000:
            self.envoyer_json(
                {"erreur": "Demande vide ou trop volumineuse."},
                413
            )
            return

        try:
            contenu = self.rfile.read(longueur).decode("utf-8")
            donnees = json.loads(contenu)
            resultat = executer_calcul(donnees)

        except (ValueError, UnicodeDecodeError) as erreur:
            self.envoyer_json({"erreur": str(erreur)}, 400)
            return

        self.envoyer_json(resultat)


if __name__ == "__main__":
    adresse = ("127.0.0.1", 8000)

    try:
        serveur = HTTPServer(adresse, Application)
    except OSError as erreur:
        print("Impossible de démarrer le serveur :", erreur)
        print("Vérifiez qu'une autre instance n'utilise pas le port 8000.")
        raise SystemExit(1)

    print("CryptoBox est prêt.")
    print("Ouvrez : http://127.0.0.1:8000")
    print("Pour arrêter : Ctrl+C")

    try:
        serveur.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt de CryptoBox.")
    finally:
        serveur.server_close()