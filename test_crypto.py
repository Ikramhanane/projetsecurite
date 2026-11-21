import unittest

from crypto import (
    ALPHABET,
    cesar_chiffrer,
    cesar_dechiffrer,
    cesar_force_brute,
    proposer_cesar,
    substitution_chiffrer,
    substitution_dechiffrer,
    transposition_chiffrer,
    transposition_dechiffrer,
)


class TestCesar(unittest.TestCase):

    def test_exemple_du_tp(self):
        self.assertEqual(
            cesar_chiffrer("BONJOUR", 3),
            "ERQMRXU"
        )

        self.assertEqual(
            cesar_dechiffrer("ERQMRXU", 3),
            "BONJOUR"
        )

    def test_toutes_les_cles(self):
        for cle in range(26):
            chiffre = cesar_chiffrer(ALPHABET, cle)
            clair = cesar_dechiffrer(chiffre, cle)

            self.assertEqual(clair, ALPHABET)

    def test_modulo(self):
        self.assertEqual(
            cesar_chiffrer("BONJOUR", 29),
            cesar_chiffrer("BONJOUR", 3)
        )

        self.assertEqual(
            cesar_chiffrer("BONJOUR", -1),
            cesar_chiffrer("BONJOUR", 25)
        )

    def test_force_brute(self):
        candidats = cesar_force_brute("ERQMRXU")

        self.assertEqual(len(candidats), 25)

        self.assertIn(
            {"cle": 3, "texte": "BONJOUR"},
            candidats
        )

        self.assertEqual(
            {candidat["cle"] for candidat in candidats},
            set(range(1, 26))
        )

    def test_proposition(self):
        proposition = proposer_cesar("ERQMRXU")

        self.assertEqual(
            proposition["resultat"],
            "BONJOUR"
        )

        self.assertEqual(proposition["cle"], 3)
        self.assertEqual(proposition["essais"], 25)

    def test_indice(self):
        chiffre = cesar_chiffrer("RENDEZVOUSDEMAIN", 7)
        proposition = proposer_cesar(chiffre, "DEMAIN")

        self.assertEqual(proposition["cle"], 7)

        self.assertEqual(
            proposition["resultat"],
            "RENDEZVOUSDEMAIN"
        )


class TestSubstitution(unittest.TestCase):

    def setUp(self):
        self.cle = "QWERTYUIOPASDFGHJKLZXCVBNM"

    def test_exemple_du_tp(self):
        self.assertEqual(
            substitution_chiffrer("ATTAQUE", self.cle),
            "QZZQJXT"
        )

        self.assertEqual(
            substitution_dechiffrer("QZZQJXT", self.cle),
            "ATTAQUE"
        )

    def test_aller_retour(self):
        chiffre = substitution_chiffrer(
            ALPHABET,
            self.cle
        )

        self.assertEqual(
            substitution_dechiffrer(chiffre, self.cle),
            ALPHABET
        )

    def test_cle_invalide(self):
        for cle in ("ABC", "A" * 26, ALPHABET.lower()):
            with self.assertRaises(ValueError):
                substitution_chiffrer("BONJOUR", cle)


class TestTransposition(unittest.TestCase):

    def test_exemple_du_tp(self):
        self.assertEqual(
            transposition_chiffrer(
                "RENDEZVOUSAMIDI",
                "PORTE"
            ),
            "ESIEVMRZANOIDUD"
        )

        self.assertEqual(
            transposition_dechiffrer(
                "ESIEVMRZANOIDUD",
                "PORTE"
            ),
            "RENDEZVOUSAMIDI"
        )

    def test_aller_retour_et_remplissage(self):
        cles = (
            "PORTE",
            "CORDE",
            "BANANE",
            "A",
            "MOTCLELONG"
        )

        messages = (
            "A",
            "BONJOUR",
            "AXX",
            ALPHABET
        )

        for cle in cles:
            for message in messages:
                with self.subTest(
                    cle=cle,
                    message=message
                ):
                    chiffre = transposition_chiffrer(
                        message,
                        cle
                    )

                    nombre_x = (-len(message)) % len(cle)
                    attendu = message + "X" * nombre_x

                    self.assertEqual(
                        transposition_dechiffrer(
                            chiffre,
                            cle
                        ),
                        attendu
                    )

    def test_lettres_repetees_du_mot_cle(self):
        self.assertEqual(
            transposition_chiffrer("ABCDEF", "ABA"),
            "ADCFBE"
        )

    def test_longueur_invalide(self):
        with self.assertRaises(ValueError):
            transposition_dechiffrer("ABC", "PORTE")

    def test_cle_vide(self):
        with self.assertRaises(ValueError):
            transposition_chiffrer("BONJOUR", "")


class TestValidation(unittest.TestCase):

    def test_messages_invalides(self):
        messages_invalides = (
            "",
            "bonjour",
            "ÉCOLE",
            "BON JOUR",
            "ABC1"
        )

        for message in messages_invalides:
            with self.subTest(message=message):
                with self.assertRaises(ValueError):
                    cesar_chiffrer(message, 3)


if __name__ == "__main__":
    unittest.main()