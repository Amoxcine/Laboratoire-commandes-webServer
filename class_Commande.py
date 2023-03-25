import datetime
import uuid
import json

patern_processus = {
    "1": {
        "reception_empreinte": "not-started",
        "scan_commande": "disabled",
        "fichier_envoye": "disabled",
        "modele_receptionne": "disabled",
        "modele_controle": "disabled",
        "modele_briallance": "disabled",
    },
    "2": {
        "couler_moule": "not-started",
        "moule_sechage": "disabled",
        "moule_controle": "disabled",
        "inlay_core": "disabled",
        "shape": "disabled",
        "ceramique": "disabled",
    },
    "3": {
        "reception_empreinte": "not-started",
        "modele": "disabled",
        "moule_sechage": "disabled",
        "moule_controle": "disabled",
        "trace_contours": "disabled",
        "cire": "disabled",
        "clef": "disabled",
        "resine": "disabled",
        "bain": "disabled",
        "gratter_polir": "disabled",
    }
}

class Commande:

    def __init__(self, UniqueID, DateCreation, DateFin, NomDentiste, NumBoite, Processus, Priorite, Etapes):
        self._UniqueID = UniqueID
        self._DateCreation = DateCreation
        self._DateFin = DateFin
        self._NomDentiste = NomDentiste
        self._NumBoite = NumBoite
        self._Processus = Processus
        self._Priorite = Priorite
        self._Etapes = Etapes

    def __init__(self, nom_dentiste, date_fin, processus, num_boite):
        self._UniqueID = uuid.uuid4()
        self._DateCreation = datetime.datetime.now().strftime("%Y-%m-%d")
        self._DateFin = date_fin
        self._NomDentiste = nom_dentiste
        self._NumBoite = num_boite
        self._Priorite = 0
        self._Processus = processus
        self._Etapes = patern_processus[processus]

    # SET
    def set_DateFin(self, date_fin):
        self._DateFin = date_fin

    def set_NomDentiste(self, nom_dentiste):
        self._NomDentiste = nom_dentiste

    def set_NumBoite(self, num_boite):
        self._NumBoite = num_boite

    def set_Processus(self, processus):
        self._Processus = processus
        self._Etapes = patern_processus[processus]

    def set_Priorite(self, Priorite):
        self._Priorite = Priorite

    # GET
    def get_UniqueID(self):
        return self._UniqueID

    def get_DateCreation(self):
        return self._DateCreation

    def get_DateFin(self):
        return self._DateFin

    def get_NomDentiste(self):
        return self._NomDentiste

    def get_NumBoite(self):
        return self._NumBoite

    def get_Processus(self):
        return self._Processus

    def get_Priorite(self):
        return self._Priorite

    def get_Etapes(self):
        return self._Etapes

class CommandeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Commande):
            return {
                "UniqueID": str(obj.get_UniqueID()),
                "DateCreation": obj.get_DateCreation(),
                "DateFin": obj.get_DateFin(),
                "NomDentiste": obj.get_NomDentiste(),
                "NumBoite": obj.get_NumBoite(),
                "priorite": obj.get_Priorite(),
                "Processus": obj.get_Processus(),
                "Etapes": obj.get_Etapes(),
            }
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.datetime.strftime('%d-%m-%Y')
        else:
            return json.JSONEncoder.default(self, obj)