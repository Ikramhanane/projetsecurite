"""
CryptoBox : algorithmes du TP1.
Aucune bibliothèque de cryptographie.
"""

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def verifier_texte(texte):
    """Vérifie les conventions du TP."""
    if not isinstance(texte, str) or not texte:
        raise ValueError("Le message ne doit pas être vide.")

    if any(lettre not in ALPHABET for lettre in texte):
        raise ValueError(
            "Utilisez uniquement les lettres A à Z, "
            "sans espaces, sans accents et sans chiffres."
        )

    return texte


# --------------------------------------------------
# CÉSAR
# --------------------------------------------------

def cesar_chiffrer(message, cle):
    verifier_texte(message)
    cle = int(cle) % 26

    resultat = ""

    for lettre in message:
        position = ALPHABET.index(lettre)
        nouvelle_position = (position + cle) % 26
        resultat += ALPHABET[nouvelle_position]

    return resultat


def cesar_dechiffrer(message, cle):
    return cesar_chiffrer(message, -int(cle))


def cesar_force_brute(message):
    """Retourne les 25 essais demandés dans le TP."""
    verifier_texte(message)

    candidats = []

    for cle in range(1, 26):
        candidats.append({
            "cle": cle,
            "texte": cesar_dechiffrer(message, cle)
        })

    return candidats


# Petit lexique pédagogique, à enrichir.
# Il ne permet pas de reconnaître tous les messages.
MOTS_CONNUS = {
    "BONJOUR",
    "SALUT",
    "MERCI",
    "ATTAQUE",
    "MESSAGE",
    "SECRET",
    "SECURITE",
    "CRYPTOGRAPHIE",
    "ORDINATEUR",
    "PROGRAMMATION",
    "PYTHON",
    "RENDEZVOUS",
    "BRAVO",
    "FELICITATIONS",
}

# Fréquences approximatives des lettres en français.
FREQUENCES = (
    8.15, 0.97, 3.15, 3.73, 17.39, 1.12, 0.97,
    0.85, 7.31, 0.45, 0.02, 5.69, 2.87, 7.12,
    5.28, 2.80, 1.21, 6.64, 8.14, 7.22, 6.38,
    1.64, 0.03, 0.41, 0.28, 0.15
)


def score_francais(message):
    """
    Classement approximatif.
    Un score élevé signifie seulement « plus plausible ».
    """
    longueur = len(message)
    ecart = 0

    for lettre, frequence in zip(ALPHABET, FREQUENCES):
        attendu = longueur * frequence / 100
        observe = message.count(lettre)
        ecart += (observe - attendu) ** 2 / attendu

    bonus_mots = sum(
        len(mot) ** 2
        for mot in MOTS_CONNUS
        if mot in message
    )

    mot_exact = message in MOTS_CONNUS

    return mot_exact, bonus_mots, -ecart


def proposer_cesar(message, indice=""):
    """
    Teste les 25 clés et propose un seul candidat.
    L'indice est un fragment connu du message clair.
    """
    candidats = cesar_force_brute(message)

    if indice:
        verifier_texte(indice)

    def classement(candidat):
        texte = candidat["texte"]
        contient_indice = bool(indice and indice in texte)
        return contient_indice, *score_francais(texte)

    meilleur = max(candidats, key=classement)

    if indice:
        correspondances = sum(
            indice in candidat["texte"]
            for candidat in candidats
        )

        if correspondances == 1:
            note = (
                "Un seul candidat contient votre indice. "
                "Vérifiez néanmoins le sens du message."
            )
        elif correspondances == 0:
            note = (
                "Aucun candidat ne contient votre indice. "
                "La proposition repose sur un classement linguistique."
            )
        else:
            note = (
                "Plusieurs candidats contiennent votre indice. "
                "La proposition reste incertaine."
            )
    else:
        note = (
            "Proposition automatique non garantie, surtout pour "
            "un mot court, un nom propre ou des lettres aléatoires."
        )

    return {
        "resultat": meilleur["texte"],
        "cle": meilleur["cle"],
        "essais": 25,
        "note": note
    }


# --------------------------------------------------
# SUBSTITUTION
# --------------------------------------------------

def verifier_cle_substitution(cle):
    if (
        not isinstance(cle, str)
        or len(cle) != 26
        or set(cle) != set(ALPHABET)
    ):
        raise ValueError(
            "La clé de substitution doit contenir les 26 lettres "
            "A à Z, chacune une seule fois."
        )


def substitution_chiffrer(message, cle):
    verifier_texte(message)
    verifier_cle_substitution(cle)

    resultat = ""

    for lettre in message:
        position = ALPHABET.index(lettre)
        resultat += cle[position]

    return resultat


def substitution_dechiffrer(message, cle):
    verifier_texte(message)
    verifier_cle_substitution(cle)

    resultat = ""

    for lettre in message:
        position = cle.index(lettre)
        resultat += ALPHABET[position]

    return resultat


# --------------------------------------------------
# TRANSPOSITION PAR COLONNES
# --------------------------------------------------

def ordre_colonnes(cle):
    verifier_texte(cle)

    # Pour deux lettres identiques, la colonne de gauche
    # est lue avant celle de droite.
    return sorted(
        range(len(cle)),
        key=lambda position: (cle[position], position)
    )


def transposition_chiffrer(message, cle):
    verifier_texte(message)
    ordre = ordre_colonnes(cle)

    nombre_colonnes = len(cle)

    nombre_x = (-len(message)) % nombre_colonnes
    message_complete = message + "X" * nombre_x

    resultat = ""

    for colonne in ordre:
        for position in range(
            colonne,
            len(message_complete),
            nombre_colonnes
        ):
            resultat += message_complete[position]

    return resultat


def transposition_dechiffrer(message, cle):
    verifier_texte(message)
    ordre = ordre_colonnes(cle)

    nombre_colonnes = len(cle)

    if len(message) % nombre_colonnes != 0:
        raise ValueError(
            "La longueur du message chiffré doit être un multiple "
            "de la longueur du mot-clé."
        )

    nombre_lignes = len(message) // nombre_colonnes
    colonnes = [""] * nombre_colonnes

    position = 0

    for colonne in ordre:
        colonnes[colonne] = message[
            position:position + nombre_lignes
        ]
        position += nombre_lignes

    resultat = ""

    for ligne in range(nombre_lignes):
        for colonne in range(nombre_colonnes):
            resultat += colonnes[colonne][ligne]

    # Ne pas supprimer automatiquement les X :
    # certains peuvent appartenir au vrai message.
    return resultat