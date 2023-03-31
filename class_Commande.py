import datetime
import uuid
import json

dependencies = {
    "1": {
        "reception_empreinte": None,
        "scan_commande": ["reception_empreinte"],
        "fichier_envoye": ["scan_commande"],
        "modele_receptionne": ["fichier_envoye"],
        "modele_controle": ["modele_receptionne"],
        "modele_briallance": ["modele_controle"],
    },
    "2": {
        "couler_moule": None,
        "moule_sechage": ["couler_moule"],
        "moule_controle": ["moule_sechage"],
        "inlay_core": ["moule_controle"],
        "shape": ["inlay_core"],
        "ceramique": ["shape"],
    },
    "3": {
        "reception_empreinte": None,
        "modele": ["reception_empreinte"],
        "moule_sechage": ["modele"],
        "moule_controle": ["moule_sechage"],
        "trace_contours": ["moule_controle"],
        "cire": ["trace_contours"],
        "clef": ["cire"],
        "resine": ["clef"],
        "bain": ["resine"],
        "gratter_polir": ["bain"],
    }
}

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
        if UniqueID == "":
            self._UniqueID = uuid.uuid4()
        else:
            self._UniqueID = UniqueID
        if DateCreation == "":
            self._DateCreation = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            self._DateCreation = DateCreation
        self._DateFin = DateFin
        self._NomDentiste = NomDentiste
        self._NumBoite = NumBoite
        self._Processus = Processus
        if Priorite == "":
            self._Priorite = 0
        else:
            self._Priorite = Priorite
        if Etapes is {}:
            self._Etapes = patern_processus[Processus]
        else:
            self._Etapes = Etapes

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

    def toJson(self):
        return {
            "UniqueID": self._UniqueID,
            "DateCreation": self._DateCreation,
            "DateFin": self._DateFin,
            "NomDentiste": self._NomDentiste,
            "NumBoite": self._NumBoite,
            "priorite": self._Priorite,
            "Processus": self._Processus,
            "Etapes": self._Etapes,
            }

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