from flask import Flask, jsonify, request, render_template
from datetime import datetime , timedelta
import mysql.connector
from flask_cors import CORS
import random
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
CORS(app)
config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "gomuscu",
    "port": 3306
}

db = mysql.connector.connect(**config)

def get_db():
    global db
    try:
        db.ping(reconnect=True, attempts=3, delay=2)
    except:
        db = mysql.connector.connect(**config)
    return db


@app.route("/")
def accueil():
    return jsonify({
        "message": "Serveur GoMuscu opérationnel"
    })


@app.route("/register", methods=["POST"])
def register():

    donnees = request.get_json()

    nom = donnees.get("nom")
    email = donnees.get("email")
    mot_de_passe = donnees.get("mot_de_passe")

    if not nom or not email or not mot_de_passe:
        return jsonify({
            "success": False,
            "message": "Tous les champs sont obligatoires"
        }), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM utilisateurs WHERE email = %s",
        (email,)
    )

    utilisateur = cursor.fetchone()

    if utilisateur:
        cursor.close()
        db.close()

        return jsonify({
            "success": False,
            "message": "Cette adresse mail est déjà utilisée"
        }), 409
    mot_de_passe_hash = generate_password_hash(mot_de_passe)

    cursor.execute(
        """
        INSERT INTO utilisateurs (nom, email, mot_de_passe)
        VALUES (%s, %s, %s)
        """,
        (nom, email, mot_de_passe_hash)
    )

    db.commit()

    nouvel_id = cursor.lastrowid

    cursor.close()
    db.close()

    return jsonify({
        "success": True,
        "message": "Compte créé avec succès",
        "user_id": nouvel_id
    }), 201






@app.route("/login", methods=["POST"])
def login():

    try:
        # Récupération des données envoyées par Flet
        donnees = request.get_json()

        email = donnees.get("email")
        mot_de_passe = donnees.get("mot_de_passe")

        # Vérification des champs
        if not email or not mot_de_passe:
            return jsonify({
                "success": False,
                "message": "Veuillez remplir tous les champs."
            }), 400

        # Connexion MySQL
        connexion = get_db()

        curseur = connexion.cursor(dictionary=True)

        # Recherche de l'utilisateur
        curseur.execute(
            """
            SELECT id, nom, email, mot_de_passe
            FROM utilisateurs
            WHERE email = %s
            """,
            (email,)
        )

        utilisateur = curseur.fetchone()

        # Fermeture
        

        # Utilisateur inexistant
        if utilisateur is None:
            curseur.close()
            connexion.close()
            return jsonify({
                "success": False,
                "message": "Adresse mail ou mot de passe incorrect."
            }), 401
        hash_mdp = utilisateur["mot_de_passe"]

        # Vérification du mot de passe
        if not check_password_hash(hash_mdp,mot_de_passe):

            return jsonify({
                "success": False,
                "message": "Adresse mail ou mot de passe incorrect.",
                "nom_utilisateur": utilisateur['nom']
            }), 401

        # Connexion réussie
        token = secrets.token_urlsafe(32)

        date_expiration = datetime.now() + timedelta(days=30)

        curseur.execute(
            """
            INSERT INTO sessions
            (utilisateur_id, token, date_expiration)
            VALUES (%s, %s, %s)
            """,
            (
                utilisateur["id"],
                token,
                date_expiration
            )
        )

        connexion.commit()
        curseur.close()
        connexion.close()
        return jsonify({
            "success": True,
            "message": "Connexion réussie.",
            "token" : token,
            "utilisateur": {
                "id": utilisateur["id"],
                "nom": utilisateur["nom"],
                "email": utilisateur["email"]
            }
        }), 200

    except mysql.connector.Error as erreur:

        print("ERREUR MYSQL :", erreur)

        return jsonify({ 
            "success": False,
            "message": "Erreur de connexion à la base de données."
        }), 500

    except Exception as erreur:

        print("ERREUR LOGIN :", erreur)

        return jsonify({
            "success": False,
            "message": "Une erreur est survenue."
        }), 500


@app.route("/verify-session", methods=["POST"])
def verify_session():

    try:

        donnees = request.get_json()

        token = donnees.get("token")

        if not token:
            return jsonify({
                "success": False,
                "message": "Token manquant."
            }), 401

        connexion = get_db()

        curseur = connexion.cursor(dictionary=True)

        curseur.execute(
            """
            SELECT
                sessions.utilisateur_id,
                sessions.date_expiration,
                utilisateurs.nom,
                utilisateurs.email
            FROM sessions
            JOIN utilisateurs
                ON utilisateurs.id = sessions.utilisateur_id
            WHERE sessions.token = %s
            """,
            (token,)
        )

        session = curseur.fetchone()

        # -----------------------------------------------
        # TOKEN INEXISTANT
        # -----------------------------------------------

        if session is None:

            curseur.close()
            connexion.close()

            return jsonify({
                "success": False,
                "message": "Session invalide."
            }), 401

        # -----------------------------------------------
        # TOKEN EXPIRÉ
        # -----------------------------------------------

        if session["date_expiration"] < datetime.now():

            curseur.execute(
                """
                DELETE FROM sessions
                WHERE token = %s
                """,
                (token,)
            )

            connexion.commit()

            curseur.close()
            connexion.close()

            return jsonify({
                "success": False,
                "message": "Session expirée."
            }), 401

        # -----------------------------------------------
        # TOKEN VALIDE
        # -----------------------------------------------

        curseur.close()
        connexion.close()

        return jsonify({
            "success": True,
            "message": "Session valide.",
            "utilisateur": {
                "id": session["utilisateur_id"],
                "nom": session["nom"],
                "email": session["email"]
            }
        }), 200

    except mysql.connector.Error as erreur:

        print("ERREUR MYSQL :", erreur)

        return jsonify({
            "success": False,
            "message": "Erreur MySQL."
        }), 500

    except Exception as erreur:

        print("ERREUR VERIFY SESSION :", erreur)

        return jsonify({
            "success": False,
            "message": "Erreur serveur."
        }), 500

@app.route("/logout", methods=["POST"])
def logout():
    donnees = request.get_json()
    token = donnees.get("token")

    if not token:
        return jsonify({
            "success": False,
            "message": "Token manquant"
        }), 400

    connexion = get_db()

    curseur = connexion.cursor()

    curseur.execute(
        "DELETE FROM sessions WHERE token = %s",
        (token,)
    )

    connexion.commit()

    curseur.close()
    connexion.close()

    return jsonify({
        "success": True
    })

@app.route("/ajouter_seance", methods=["POST"])
def ajouter_seance():
    donnees = request.get_json()

    nom = donnees.get("nom")
    heure = donnees.get("heure")
    date = donnees.get("date")
    token = donnees.get("token")

    try:
        connexion = get_db()
        curseur = connexion.cursor(dictionary=True)

        # Récupérer l'ID de l'utilisateur grâce au token
        curseur.execute(
            "SELECT utilisateur_id FROM sessions WHERE token = %s",
            (token,)
        )

        session = curseur.fetchone()

        if not session:
            curseur.close()
            connexion.close()

            return jsonify({
                "success": False,
                "message": "Token invalide."
            }), 401

        utilisateur_id = session["utilisateur_id"]

        print("Utilisateur ID :", utilisateur_id)

        # Ajouter la séance
        curseur.execute(
            """
            INSERT INTO seance (utilisateur_id, nom, date, heure)
            VALUES (%s, %s, %s, %s)
            """,
            (utilisateur_id, nom, date, heure)
        )

        print("b")

        connexion.commit()

        curseur.close()
        connexion.close()

        return jsonify({
            "success": True,
            "message": "Séance ajoutée."
        }), 200

    except Exception as e:
        print("ERREUR AJOUT SEANCE :", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/recuperer_seances", methods=["POST"])
def recuperer_seances():
    donnees = request.get_json()
    token = donnees.get("token")
    print("TOKEN :", token)

    try:
        connexion = get_db()
        curseur = connexion.cursor(dictionary=True)

        # Récupérer l'utilisateur grâce au token
        curseur.execute(
            "SELECT utilisateur_id FROM sessions WHERE token = %s",
            (token,)
        )

        session = curseur.fetchone()

        if not session:
            curseur.close()
            connexion.close()

            return jsonify({
                "success": False,
                "message": "Token invalide."
            }), 401

        utilisateur_id = session["utilisateur_id"]

        # Récupérer les séances
        curseur.execute(
            """
            SELECT id, nom, date, heure, prevenir
            FROM seance
            WHERE utilisateur_id = %s
            ORDER BY date, heure
            """,
            (utilisateur_id,)
        )

        seances = curseur.fetchall()

        curseur.close()
        connexion.close()

        # Transformer les données pour JSON
        for seance in seances:

            # DATE
            seance["date"] = seance["date"].strftime("%Y-%m-%d")

            # HEURE
            heure = seance["heure"]

            if hasattr(heure, "strftime"):
                # Si MySQL renvoie un objet time
                seance["heure"] = heure.strftime("%H:%M:%S")
            else:
                # Si MySQL renvoie un timedelta
                total_seconds = int(heure.total_seconds())

                heures = total_seconds // 3600
                minutes = (total_seconds % 3600) // 60
                secondes = total_seconds % 60

                seance["heure"] = f"{heures:02d}:{minutes:02d}:{secondes:02d}"

        return jsonify({
            "success": True,
            "seances": seances
        }), 200

    except Exception as e:
        print("ERREUR RECUPERATION SEANCES :", e)

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@app.route("/supprimer_seance", methods=["POST"])
def supprimer_seance():
    try:
        donnees = request.get_json()
        token = donnees.get("token")
        id_seance = donnees.get("id")

        if not token or not id_seance:
            return jsonify({"success": False, "message": "Données manquantes"}), 400

        connexion = get_db()
        curseur = connexion.cursor(dictionary=True)

        curseur.execute(
            "SELECT utilisateur_id FROM sessions WHERE token = %s",
            (token,)
        )
        utilisateur = curseur.fetchone()

        if not utilisateur:
            curseur.close()
            connexion.close()
            return jsonify({"success": False, "message": "Session invalide"}), 401

        curseur.execute(
            "DELETE FROM seance WHERE id = %s AND utilisateur_id = %s",
            (id_seance, utilisateur["utilisateur_id"])
        )
        if curseur.rowcount == 0:
            connexion.rollback()
            curseur.close()
            connexion.close()
            return jsonify({"success": False, "message": "Séance introuvable"}), 404

        connexion.commit()
        curseur.close()
        connexion.close()

        return jsonify({"success": True, "message": "Séance supprimée"})

    except Exception as e:
        print("ERREUR MYSQL SUPPRESSION :", e)
        return jsonify({"success": False, "message": "Erreur serveur"}), 500

    
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
