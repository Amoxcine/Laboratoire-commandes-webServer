import json
from django.http import JsonResponse
from flask import Flask, render_template, request, redirect, url_for
from class_Commande import Commande, CommandeEncoder
from class_ListeCommandes import TemplateListeCommandes

app = Flask(__name__)

ListeCommandes = TemplateListeCommandes()

try:
    with open("commandes.json", "r") as f:
        json_data = json.load(f)
        ListeCommandes = TemplateListeCommandes()
        for data in json_data:
            commande = Commande(data["UniqueID"], data["DateCreation"], data["DateFin"], data["NomDentiste"], data["NumBoite"], data["Processus"], data["priorite"], data["Etapes"])
            ListeCommandes.ajouter_commande(commande)
except FileNotFoundError:
    with open("commandes.json", "w") as f:
        ListeCommandes = TemplateListeCommandes()
        json.dump(ListeCommandes.get_liste_commandes(), f, cls=CommandeEncoder)
except json.decoder.JSONDecodeError:
    ListeCommandes = TemplateListeCommandes()


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/ajouter_commande', methods=['GET', 'POST'])
def ajouter_commande():
    if request.method == 'POST':
        nom_dentiste = request.form['nom_dentiste']
        date_fin = request.form['date_fin']
        processus = request.form['processus']
        num_boite = request.form['num_boite']

        ListeCommandes.ajouter_commande(Commande(nom_dentiste, date_fin, processus, num_boite))
        ListeCommandes.trier_par_priorite()

        with open("commandes.json", "w") as f:
            json.dump(ListeCommandes.get_liste_commandes(), f,cls=CommandeEncoder)

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
            commande = ListeCommandes.supprimer_commande(int(commande_id))
            with open('commandes.json', 'w') as f:
                json.dump(ListeCommandes.get_liste_commandes(), f,cls=CommandeEncoder)

            message = f"Commande {commande[commande_id]} supprimée avec succès"

        except IndexError:
            message = "Aucune commande à supprimer"
        return redirect(url_for('delete_commande', message=message), code=303)
    else:
        message = request.args.get('message', '')
        return render_template('delete_commandes.html', commandes=ListeCommandes.get_liste_commandes(), message=message)


@app.route('/liste_commandes')
def commandes_show():
    ListeCommandes.trier_par_priorite()
    return render_template('gestion_commandes.html', commandes=ListeCommandes.toJson(), dependencies=dependencies)


@app.route('/status')
def statut_variables():
    variables = {}
    variables['config'] = {'debug': app.debug}
    variables['liste'] = ListeCommandes.toJson()
    variables['dependencies'] = dependencies
    return render_template('status.html', variables=variables)


# Crée une fonction qui peut recevoir les des requêtes POST et qui les modifies dans la liste de commandes
@app.route('/update_commande', methods=['POST'])
def update_commande():
    """Reçoit une requête POST et modifie la commande correspondante"""
    commande_id = request.form['commande_id']
    etat = request.form['etat']



    with open('commandes.json', 'w') as f:
        json.dump(ListeCommandes.get_liste_commandes(), f,cls=CommandeEncoder)

    return JsonResponse({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True)
