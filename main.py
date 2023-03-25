import json
from django.http import JsonResponse
from flask import Flask, render_template, request, redirect, url_for
from class_Commande import Commande, CommandeEncoder
from class_ListeCommandes import TemplateListeCommandes

app = Flask(__name__)

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

ListeCommandes = TemplateListeCommandes()

try:
    with open("commandes.json", "r") as f:
        ListeCommandes.liste = json.load(f)
except FileNotFoundError:
    with open("commandes.json", "w") as f:
        ListeCommandes.liste = []
        json.dump(ListeCommandes.liste, f)
except json.decoder.JSONDecodeError:
    ListeCommandes.liste = []


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/ajouter_commande', methods=['GET', 'POST'])
def ajouter_commande(liste_commandes=ListeCommandes.liste):
    if request.method == 'POST':
        nom_dentiste = request.form['nom_dentiste']
        date_fin = request.form['date_fin']
        processus = request.form['processus']
        num_boite = request.form['num_boite']

        ListeCommandes.liste.append(Commande(nom_dentiste, date_fin, processus, num_boite))
        ListeCommandes.trier_par_priorite()

        with open("commandes.json", "w") as f:
            json.dump(ListeCommandes.liste, f,cls=CommandeEncoder)

        # Affichage d'un message de confirmation
        message = "Commande ajoutée avec succès"
        return render_template('ajouter_commande.html', message=message)
    else:
        return render_template('ajouter_commande.html')


# Create a function to delete a command
@app.route('/delete_commande', methods=['GET', 'POST'])
def delete_commande():
    if request.method == 'POST':
        commande_id = request.form['commande_id']

        try:
            commande = ListeCommandes.liste.pop(int(commande_id))
            with open('commandes.json', 'w') as f:
                json.dump(ListeCommandes.liste, f,cls=CommandeEncoder)

            message = f"Commande {commande['num_boite']} supprimée avec succès"

        except IndexError:
            message = "Aucune commande à supprimer"
        return redirect(url_for('delete_commande', message=message), code=303)
    else:
        message = request.args.get('message', '')
        return render_template('delete_commandes.html', commandes=ListeCommandes.liste, message=message)


@app.route('/liste_commandes')
def commandes_show():
    ListeCommandes.trier_par_priorite()
    return render_template('gestion_commandes.html', commandes=ListeCommandes.liste, dependencies=dependencies)


@app.route('/status')
def statut_variables():
    variables = {}
    variables['config'] = {'debug': app.debug}
    variables['liste_commandes'] = ListeCommandes.liste
    variables['dependencies'] = dependencies
    return render_template('status.html', variables=variables)


# Crée une fonction qui peut recevoir les des requêtes POST et qui les modifies dans la liste de commandes
@app.route('/update_commande', methods=['POST'])
def update_commande():
    commande_id = request.form['commande_id']
    etat = request.form['etat']

    ListeCommandes.liste[int(commande_id)][etat] = True

    with open('commandes.json', 'w') as f:
        json.dump(ListeCommandes.liste, f,cls=CommandeEncoder)

    return JsonResponse({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
