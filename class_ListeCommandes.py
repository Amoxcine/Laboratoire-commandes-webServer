from class_Commande import Commande
from datetime import datetime


def tri_par_date(Commande):
    # On récupère la date de fin de la commande au format YYYY-MM-DD
    print(Commande)
    date_fin = Commande.get_DateFin()
    # On retourne cette date en format date pour permettre le tri
    return datetime.strptime(date_fin, '%Y-%m-%d').strftime('%d %m %Y')


class TemplateListeCommandes:
    def __init__(self):
        self.liste = []

    def ajouter_commande(self, commande):
        self.liste.append(commande)

    def supprimer_commande(self, commande):
        self.liste.remove(commande)

    def trier_par_priorite(self):
        # On trie la liste des commandes en fonction de leur date de fin et de leur position dans la liste
        self.liste = sorted(self.liste, key=tri_par_date)

    def get_liste_commandes(self):
        return self.liste

    def set_liste_commandes(self, liste_commandes):
        self.liste = liste_commandes

