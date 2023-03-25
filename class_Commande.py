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
    def __init__(self, nom_dentiste, date_fin, processus, num_boite):
        self.UniqueID = uuid.uuid4()
        self.DateCreation = datetime.datetime.now().strftime("%Y-%m-%d")
        self.DateFin = date_fin
        self.NomDentiste = nom_dentiste
        self.NumBoite = num_boite
        self.Priorite = 0
        self.Processus = processus
        self.etapes = patern_processus[processus]

    # SET
    def setDateFin(self, date_fin):
        self.DateFin = date_fin

    def setNomDentiste(self, nom_dentiste):
        self.NomDentiste = nom_dentiste

    def setNumBoite(self, num_boite):
        self.NumBoite = num_boite

    def setProcessus(self, processus):
        self.Processus = processus
        self.etapes = patern_processus[processus]

    def set_priorite(self, priorite):
        self.priorite = priorite

    # GET
    def getUniqueID(self):
        return self.UniqueID

    def getDateCreation(self):
        return self.DateCreation

    def getDateFin(self):
        return self.DateFin

    def getNomDentiste(self):
        return self.NomDentiste

    def getNumBoite(self):
        return self.NumBoite

    def getProcessus(self):
        return self.Processus

    def get_priorite(self):
        return self.priorite

    def get_etapes(self):
        return self.etapes

class CommandeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Commande):
            return {
                "UniqueID": str(obj.getUniqueID()),
                "DateCreation": obj.getDateCreation(),
                "DateFin": obj.getDateFin(),
                "NomDentiste": obj.getNomDentiste(),
                "NumBoite": obj.getNumBoite(),
                "priorite": obj.get_priorite(),
                "Processus": obj.getProcessus(),
                "etapes": obj.get_etapes(),
            }
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.strftime('%d-%m-%Y')
        else:
            return json.JSONEncoder.default(self, obj)