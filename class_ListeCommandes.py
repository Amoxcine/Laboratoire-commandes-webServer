from class_Commande import Commande, CommandeEncoder
from datetime import datetime
import json


def tri_par_date(Commande):
    # On récupère la date de fin de la commande au format YYYY-MM-DD
    print(Commande)
    date_fin = Commande.get_DateFin()
    # On retourne cette date en format date pour permettre le tri
    return datetime.strptime(date_fin, '%Y-%m-%d').strftime('%d %m %Y')


class TemplateListeCommandes:
    def __init__(self):
        self._liste = []

    def trier_par_priorite(self):
        # On trie la liste des commandes en fonction de leur date de fin et de leur position dans la liste
        self._liste = sorted(self._liste, key=tri_par_date)

    def ajouter_commande(self, commande):
        self._liste.append(commande)

    def supprimer_commande(self, id_commande):
        self._liste.pop(id_commande)

    def get_liste_commandes(self):
        return self._liste

    def set_liste_commandes(self, liste_commandes):
        self._liste = liste_commandes

    def toJson(self):
        return [value.toJson() for value in self._liste]
