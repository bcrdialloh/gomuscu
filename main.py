import flet as ft
import requests
from flet import SharedPreferences
import json
import os
import calendar
from datetime import datetime
def main(page: ft.Page):
    page.fonts = {"Poppins": "Poppins-Regular.ttf","PoppinsBold": "Poppins-Bold.ttf"}
    police = "Poppins"
    police_sous = "PoppinsBold"
    import os
    print(os.path.exists("Poppins-Regular.ttf"))
    print(os.getcwd())
    preferences = SharedPreferences()
    API_URL = "http://192.168.1.35:5000"
    page.bgcolor = "#C9DDE7"
    page.title = "GoMuscu"
    nom_utilisateur = None
    email = None
    contenu = ft.Column(expand=True)

    def afficher_message(message, couleur="black"):
     
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    message,
                    color="black",
                ),
            )
        )
    

    async def ajouter_token(token):
        await ft.SharedPreferences().set("gomuscu.auth_token", token)



    #-------------------------------------------------
    #PAGE DE CONNEXION
    #-------------------------------------------------
    def connexion(mail,mdp):
        page.run_task(connexion_async,mail,mdp)

    async def connexion_async(mail,mdp) :
        global email
        if not mail.strip():
            afficher_message("Veuillez entrer votre adresse mail.")
            return
        if not mdp.strip():
            afficher_message("Veuillez entrer votre mot de passe.")
            return

        donnees = {"email": mail,"mot_de_passe": mdp}
        reponse = requests.post(API_URL + "/login",json=donnees)

        if reponse.status_code == 200 :
            resultat = reponse.json()

            if resultat.get("success"):
                utilisateur = resultat.get("utilisateur",{})
                print(utilisateur)
                global nom_utilisateur
                global email
                global token
                email = utilisateur.get("email","Utilisateur")
                print(email)
                nom_utilisateur = utilisateur.get("nom","Utilisateur")
                token = resultat.get("token")
                await ajouter_token(token)
                lancement()
        else:
            afficher_message("Adresse mail ou mot de passe incorect.")

                    
    def inscription(nom,mail,mdp):
        global nom_utilisateur
        if not nom.strip():
            afficher_message("Veuillez entrer votre nom.")
            return

        if not mail.strip():
            afficher_message("Veuillez entrer votre adresse mail.")
            return

        if not mdp.strip():
            afficher_message("Veuillez entrer un mot de passe.")
            return

        donnees = {
            "nom": nom,
            "email": mail,
            "mot_de_passe": mdp}

            
        reponse = requests.post(API_URL + "/register",json=donnees)

        if 200 <= reponse.status_code <= 300 :
            connexion(mail,mdp)
        else:
            afficher_message("Adresse mail ou mot de passe incorect.")

            


    def connexion_inscription():
        page.clean()

        champ_mail = ft.TextField(
            hint_text="Adresse mail",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#777777"),
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=15,
            border_width=0,
            filled=True,
            bgcolor="#FFFFFF",
            width=320,
            height=55,
        )

        champ_mdp = ft.TextField(
            hint_text="Mot de passe",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#777777"),
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_width=0,
            filled=True,
            bgcolor="#FFFFFF",
            width=320,
            height=70,
        )

        bouton = ft.Button(
            "Se connecter",
            width=320,
            height=55,
            on_click=lambda e: connexion(champ_mail.value,champ_mdp.value)
        )

        bouton_inscription = ft.Button(
            "Créer un compte",
            width=320,
            height=55,
            on_click=lambda e: page_inscription(),
        )

        formulaire = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Bienvenue",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                    ),

                    ft.Text(
                        "Connectez-vous à votre compte GoMuscu",
                        size=14,
                        color="#555555",
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(height=15),

                    champ_mail,
                    champ_mdp,

                    ft.Container(height=5),

                    bouton,
                    bouton_inscription,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            width=360,
            padding=25,
            border_radius=25,
            bgcolor="#00000015",
        )

        page.add(
            ft.SafeArea(
                content=ft.Container(
                    content=formulaire,
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                ),
                expand=True,
            )
        )


    def page_inscription():
        page.clean()


        champ_nom = ft.TextField(
            hint_text="Nom",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#777777"),
            prefix_icon=ft.Icons.PERSON_OUTLINE,
            border_radius=15,
            border_width=0,
            filled=True,
            bgcolor="#FFFFFF",
            width=320,
            height=55,
        )

        champ_mail = ft.TextField(
            hint_text="Adresse mail",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#777777"),
            prefix_icon=ft.Icons.EMAIL_OUTLINED,
            border_radius=15,
            border_width=0,
            filled=True,
            bgcolor="#FFFFFF",
            width=320,
            height=55,
        )

        champ_mdp = ft.TextField(
            hint_text="Mot de passe",
            text_style=ft.TextStyle(color="black"),
            hint_style=ft.TextStyle(color="#777777"),
            prefix_icon=ft.Icons.LOCK_OUTLINE,
            password=True,
            can_reveal_password=True,
            border_radius=15,
            border_width=0,
            filled=True,
            bgcolor="#FFFFFF",
            width=320,
            height=70,
        )

        bouton = ft.Button(
            "Créer mon compte",
            width=320,
            height=55,
            on_click=lambda e: inscription(champ_nom.value,champ_mail.value,champ_mdp.value)
        )

        bouton_connexion = ft.Button(
            "Se connecter",
            width=320,
            height=55,
            on_click=lambda e: connexion_inscription(),
        )

        formulaire = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Créer un compte",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="black",
                    ),

                    ft.Text(
                        "Créez votre compte GoMuscu",
                        size=14,
                        color="#555555",
                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(height=15),

                    champ_nom,
                    champ_mail,
                    champ_mdp,
                    

                    ft.Container(height=5),

                    bouton,
                    bouton_connexion,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            width=360,
            padding=25,
            border_radius=25,
            bgcolor="#00000015",
        )

        page.add(
            ft.SafeArea(
                content=ft.Container(
                    content=formulaire,
                    alignment=ft.Alignment(0, 0),
                    expand=True,
                ),
                expand=True,
            )
        )
    async def async_deconnexion():
        token = await ft.SharedPreferences().get("gomuscu.auth_token")

        if token:
            try:
                reponse = requests.post(
                        API_URL + "/logout",
                        json={"token": token}
                    )
                await ft.SharedPreferences().remove("gomuscu.auth_token")
                connexion_inscription()

            except Exception as e:
                    print("Erreur logout serveur :", e)



 

    def se_deconnecter():
        page.run_task(async_deconnexion)
        connexion_inscription()
    
    
    def retour_profil(e):
        bouton = e.control
        bouton.scale = 0.8
        page.update()
        bouton.scale = 1
        page.update()
        page_profil()

    def user_info():
        global nom_utilisateur

        bouton_retour = ft.Container(
            content=ft.IconButton(
                bgcolor=None,
                icon=ft.Icons.ARROW_BACK,
                icon_color="black",
                icon_size=26,
                on_click=lambda e: page_profil(),
            ),
            bgcolor="#FFFFFF80",
            border_radius=30,
            width=48,
            height=48,
            alignment=ft.Alignment(0, 0),
        )

        contenu.controls = [
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            bouton_retour,
                            ft.Text("Mes informations", size=24, weight=ft.FontWeight.BOLD, color="black"),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),

                    ft.Text("Gère les informations de ton compte", size=15, color="#666666"),

                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=90, color="#555555"),
                                ft.Text(nom_utilisateur, size=23, weight=ft.FontWeight.BOLD, color="black", text_align=ft.TextAlign.CENTER, width=float("inf")),
                                ft.Text("Membre GoMuscu", size=14, color="#777777"),
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=5,
                        ),
                        bgcolor="#FFFFFF",
                        border_radius=20,
                        padding=20,
                        width=float("inf"),
                    ),

                    ft.Text("Compte", size=18, weight=ft.FontWeight.BOLD, color="black"),

                    ft.Button("Modifier mon profil", icon=ft.Icons.EDIT_OUTLINED, color="black", bgcolor="#FFFFFF", width=float("inf"), height=60),

                    ft.Button("Modifier mon adresse mail", icon=ft.Icons.EMAIL_OUTLINED, color="black", bgcolor="#FFFFFF", width=float("inf"), height=60),

                    ft.Button("Modifier mon mot de passe", icon=ft.Icons.LOCK_OUTLINE, color="black", bgcolor="#FFFFFF", width=float("inf"), height=60),

                    ft.Text("Sécurité", size=18, weight=ft.FontWeight.BOLD, color="black"),

                    ft.Button("Gérer la sécurité", icon=ft.Icons.SECURITY_OUTLINED, color="black", bgcolor="#FFFFFF", width=float("inf"), height=60),

                    ft.Button("Se déconnecter", icon=ft.Icons.LOGOUT, color="#D32F2F", bgcolor="#FFFFFF", width=float("inf"), height=60, on_click=lambda e: se_deconnecter()),

                    ft.Container(height=100),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        ]

    page.update()





    # --------------------------------------------------
    # CHANGEMENT DE PAGE
    # --------------------------------------------------

    def page_acceuil():
        global nom_utilisateur
        contenu.controls = [
            ft.Text(
                "Ravis de vous revoir, "+nom_utilisateur+ " !",
                size=16, color = "black",font_family=police
            )
        ]
        selectionner(0)
        page.update()




    def page_planning():
        seances = {}
        maintenant = datetime.now()
        annee, mois, jour_aujourd_hui = maintenant.year, maintenant.month, maintenant.day
        jour_selectionne = {"date": maintenant.strftime("%Y-%m-%d")}

        titre_mois = ft.Text(f"{calendar.month_name[mois].capitalize()} {annee}", size=22, weight=ft.FontWeight.BOLD, color="black", font_family=police)
        calendrier = ft.Column(spacing=5)
        contenu_seances = ft.Column(spacing=10)

        def afficher_seances_jour():
            date = jour_selectionne["date"]
            contenu_seances.controls.clear()
            if date in seances and seances[date]:
                for i, s in enumerate(seances[date]):
                    def supprimer():
                        page.run_task(async_supprimer)
                    async def async_supprimer(i=i, date=date):
                        try:
                            token = await seance_recuperer_token()
                            if not token:
                                afficher_message("Session invalide.")
                                return

                            id_seance = seances[date][i]["id"]

                            reponse = requests.post(
                                API_URL + "/supprimer_seance",
                                json={"token": token, "id": id_seance}
                            )

                            resultat = reponse.json()

                            if resultat.get("success"):
                                seances[date].pop(i)
                                if not seances[date]:
                                    del seances[date]

                                afficher_seances_jour()
                                page.update()
                            else:
                                afficher_message(resultat.get("message", "Impossible de supprimer la séance."))

                        except Exception as erreur:
                            print("ERREUR SUPPRESSION SEANCE :", erreur)
                            afficher_message("Impossible de contacter le serveur.")

                    contenu_seances.controls.append(
                        ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(s["heure"], size=15, weight=ft.FontWeight.BOLD, color="black"),
                                    ft.Text(s["nom"], size=15, color="#555555")
                                ], spacing=2, expand=True),
                                ft.IconButton(icon=ft.Icons.DELETE_OUTLINE, icon_color="#777777", tooltip="Supprimer la séance", on_click=supprimer)
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            bgcolor="#FFFFFF", border_radius=15, padding=ft.Padding(15, 10, 8, 10), width=float("inf")
                        )
                    )
            else:
                contenu_seances.controls.append(ft.Text("Aucune séance prévue.", size=14, color="#777777"))

        def afficher_calendrier():
            calendrier.controls.clear()
            calendrier.controls.append(
                ft.Row([
                    ft.Container(content=ft.Text(j, size=13, weight=ft.FontWeight.BOLD, color="#777777", text_align=ft.TextAlign.CENTER, font_family=police), expand=True, alignment=ft.Alignment(0, 0))
                    for j in ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
                ])
            )

            for semaine in calendar.monthcalendar(annee, mois):
                ligne = ft.Row(spacing=5)
                for jour in semaine:
                    if jour == 0:
                        ligne.controls.append(ft.Container(expand=True, height=45))
                        continue

                    date = f"{annee}-{mois:02d}-{jour:02d}"
                    actif = date == jour_selectionne["date"]
                    aujourd_hui = jour == jour_aujourd_hui
                    ligne.controls.append(
                        ft.Container(
                            content=ft.Container(
                                content=ft.Text(str(jour), size=15, weight=ft.FontWeight.BOLD if actif or aujourd_hui else ft.FontWeight.NORMAL, color="white" if actif else "black", text_align=ft.TextAlign.CENTER),
                                width=40, height=40, bgcolor="#000000" if actif else "#C9DDE7" if aujourd_hui else "#FFFFFF",
                                border_radius=20, alignment=ft.Alignment(0, 0), ink=True,
                                on_click=lambda e, d=date: selectionner_jour(d)
                            ),
                            expand=True, alignment=ft.Alignment(0, 0)
                        )
                    )
                calendrier.controls.append(ligne)

        def selectionner_jour(date):
            jour_selectionne["date"] = date
            afficher_calendrier()
            afficher_seances_jour()
            page.update()

        async def charger_seances():
            try:
                token = await seance_recuperer_token()
                if not token:
                    print("Aucun token trouvé.")
                    return

                reponse = requests.post(API_URL + "/recuperer_seances", json={"token": token})
                

                try:
                    resultat = reponse.json()
                except requests.exceptions.JSONDecodeError:
                    return

                if not resultat.get("success"):
                    return

                seances.clear()
                for s in resultat.get("seances", []):
                    date = str(s["date"])
                    seances.setdefault(date, []).append({
                        "id": s["id"],
                        "heure": str(s["heure"])[:5],
                        "nom": s["nom"]
                    })

                afficher_seances_jour()
                page.update()
                

            except Exception as e:
                afficher_message(e)

        def ajouter_seance(e):
            maintenant = datetime.now()
            date = jour_selectionne["date"]
            aujourd_hui = maintenant.strftime("%Y-%m-%d") == date
            heure_min = maintenant.hour if aujourd_hui else 0
            minute_min = maintenant.minute if aujourd_hui else 0
            heure_selectionnee = {"heure": heure_min, "minute": minute_min}
            heures = list(range(heure_min, 24))
            liste_heures = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO, height=180)
            liste_minutes = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO, height=180)

            apercu_heure = ft.Text(f"{heure_min:02d}:{minute_min:02d}", size=28, weight=ft.FontWeight.BOLD, color="black", text_align=ft.TextAlign.CENTER)

            def afficher_heures():
                liste_heures.controls.clear()
                for h in heures:
                    selectionnee = h == heure_selectionnee["heure"]
                    liste_heures.controls.append(
                        ft.Container(
                            content=ft.Text(f"{h:02d} h", size=16, weight=ft.FontWeight.BOLD if selectionnee else ft.FontWeight.NORMAL, color="black"),
                            width=75, height=42, alignment=ft.Alignment(0, 0), border_radius=12,
                            bgcolor="#C9DDE7" if selectionnee else "transparent", ink=True,
                            on_click=lambda e, h=h: changer_heure(h)
                        )
                    )

            def afficher_minutes():
                liste_minutes.controls.clear()
                disponibles = list(range(maintenant.minute, 60)) if aujourd_hui and heure_selectionnee["heure"] == maintenant.hour else list(range(60))
                if heure_selectionnee["minute"] not in disponibles:
                    heure_selectionnee["minute"] = disponibles[0]

                for m in disponibles:
                    selectionnee = m == heure_selectionnee["minute"]
                    liste_minutes.controls.append(
                        ft.Container(
                            content=ft.Text(f"{m:02d}", size=16, weight=ft.FontWeight.BOLD if selectionnee else ft.FontWeight.NORMAL, color="black"),
                            width=65, height=42, alignment=ft.Alignment(0, 0), border_radius=12,
                            bgcolor="#C9DDE7" if selectionnee else "transparent", ink=True,
                            on_click=lambda e, m=m: changer_minute(m)
                        )
                    )

            def changer_heure(h):
                heure_selectionnee["heure"] = h
                disponibles = list(range(maintenant.minute, 60)) if aujourd_hui and h == maintenant.hour else list(range(60))
                if heure_selectionnee["minute"] not in disponibles:
                    heure_selectionnee["minute"] = disponibles[0]
                afficher_heures()
                afficher_minutes()
                apercu_heure.value = f"{h:02d}:{heure_selectionnee['minute']:02d}"
                page.update()

            def changer_minute(m):
                heure_selectionnee["minute"] = m
                afficher_minutes()
                apercu_heure.value = f"{heure_selectionnee['heure']:02d}:{m:02d}"
                page.update()

            champ_nom = ft.TextField(
                label="Nom de la séance", hint_text="Ex : Pectoraux", border_radius=15,
                filled=True, bgcolor="#FFFFFF", border_width=0, color="black",
                label_style=ft.TextStyle(color="#777777"), hint_style=ft.TextStyle(color="#999999")
            )

            afficher_heures()
            afficher_minutes()

            async def valider(e):
                nom = champ_nom.value.strip()
                if not nom:
                    champ_nom.error_text = "Entre le nom de la séance"
                    page.update()
                    return

                heure = f"{heure_selectionnee['heure']:02d}:{heure_selectionnee['minute']:02d}"
                token = await seance_recuperer_token()

                if not token:
                    afficher_message("Session invalide.")
                    return

                try:
                    reponse = requests.post(
                        API_URL + "/ajouter_seance",
                        json={"date": date, "nom": nom, "heure": heure, "token": token}
                    )
                    resultat = reponse.json()

                    if resultat.get("success"):
                        seances.setdefault(date, []).append({
                            "id": resultat.get("id"),
                            "nom": nom,
                            "heure": heure
                        })
                        dialog.open = False
                        afficher_seances_jour()
                        page.update()
                    else:
                        afficher_message(resultat.get("message", "Une erreur s'est produite"))

                except Exception as erreur:
                    print("ERREUR AJOUT SEANCE :", erreur)
                    afficher_message("Impossible de contacter le serveur.")

            dialog = ft.AlertDialog(
                modal=True, bgcolor="#C9DDE7",
                title=ft.Text("Ajouter une séance", size=23, weight=ft.FontWeight.BOLD, color="black"),
                content=ft.Container(
                    width=330, height=400,
                    content=ft.Column([
                        champ_nom,
                        ft.Container(height=5),
                        ft.Text("Heure de la séance", size=15, weight=ft.FontWeight.BOLD, color="#555555"),
                        apercu_heure,
                        ft.Container(
                            content=ft.Row([
                                ft.Container(content=liste_heures, bgcolor="#00000008", border_radius=15, padding=5),
                                ft.Container(content=liste_minutes, bgcolor="#00000008", border_radius=15, padding=5)
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                            height=190
                        )
                    ], spacing=10, tight=True, scroll=ft.ScrollMode.HIDDEN)
                ),
                actions=[
                    ft.TextButton("Annuler", on_click=lambda e: (setattr(dialog, "open", False), page.update())),
                    ft.Button("Ajouter", icon=ft.Icons.ADD, bgcolor="#000000", color="white", on_click=valider)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.show_dialog(dialog)

        afficher_calendrier()
        afficher_seances_jour()

        contenu.controls = [
            ft.Column([
                ft.Text("Planning", size=20, weight=ft.FontWeight.W_700, color="black", font_family=police),
                ft.Text("Organise tes séances", size=15, color="#555555", font_family=police_sous),
                ft.Container(height=15),
                ft.Container(
                    content=ft.Column([
                        ft.Row([titre_mois], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(height=10),
                        calendrier
                    ], spacing=5),
                    bgcolor="#FFFFFF", border_radius=20, padding=15, width=float("inf")
                ),
                ft.Container(height=20),
                ft.Text("Séances du jour", size=20, weight=ft.FontWeight.BOLD, color="black", font_family=police),
                contenu_seances,
                ft.Container(height=10),
                ft.Button("Ajouter une séance", icon=ft.Icons.ADD, bgcolor="#FFFFFF", color="black",
                        width=float("inf"), height=55, on_click=ajouter_seance),
                ft.Container(height=100)
            ], scroll=ft.ScrollMode.AUTO, expand=True)
        ]

        page.update()
        page.run_task(charger_seances)    
    def page_seance():
        contenu.controls = [
            ft.Text(
                "Séance",
                size=16,color = "black",
            )
        ]
        selectionner(2)
        page.update()

    def page_profil():
        global nom_utilisateur

        contenu.controls = [
            ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Stack([
                            ft.Container(
                                content=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=90, color="white"),
                                alignment=ft.Alignment(0, 0),
                                expand=True,
                            ),
                        ]),
                        width=float("inf"),
                        height=220,
                        border_radius=20,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE,
                    ),

                    ft.Container(content=ft.Text(nom_utilisateur, size=24, weight=ft.FontWeight.BOLD, color="black", text_align=ft.TextAlign.CENTER,font_family=police), alignment=ft.Alignment(0, 0), width=float("inf")),

                    ft.Container(height=15),

                    ft.Button(
                        "Informations",
                        color="black",
                        bgcolor="#FFFFFF",
                        width=float("inf"),
                        height=60,
                        icon=ft.Icons.PERSON_OUTLINE,
                         on_click=user_info,
                    ),

                    ft.Button(
                        "Nous contacter",
                        color="black",
                        bgcolor="#FFFFFF",
                        width=float("inf"),
                        height=60,
                        icon=ft.Icons.EMAIL_OUTLINED,
                       # on_click=contacter,
                    ),

                    ft.Button(
                        "Paramètres",
                        color="black",
                        bgcolor="#FFFFFF",
                        width=float("inf"),
                        height=60,
                        icon=ft.Icons.SETTINGS_OUTLINED,
                       # on_click=parametres,
                    ),

                    ft.Button(
                        "Supprimer mon compte",
                        color="#D32F2F",
                        bgcolor="#FFFFFF",
                        width=float("inf"),
                        height=60,
                        icon=ft.Icons.DELETE_OUTLINE,
                       # on_click=supprimer_compte,
                    ),

                    ft.Container(height=20),

                    ft.Button(
                        "Se déconnecter",
                        color="white",
                        bgcolor="#D32F2F",
                        width=float("inf"),
                        height=60,
                        icon=ft.Icons.LOGOUT,
                        on_click=lambda e: se_deconnecter(),
                    ),

                    ft.Container(height=100),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            )
        ]

        selectionner(3)
        page.update()

    # --------------------------------------------------
    # ICÔNES DE LA BARRE
    # --------------------------------------------------
    # --------------------------------------------------
# VARIABLES NAVIGATION
# --------------------------------------------------

    index_selectionne = 0


# --------------------------------------------------
# CRÉATION D'UNE ICÔNE
# --------------------------------------------------

    def creer_bouton_navigation(
        index,
        icone_normal,
        icone_selectionne,
        fonction
    ):

        return ft.Container(

            width=55,
            height=55,

            alignment=ft.Alignment(0, 0),

            border_radius=30,

            animate=ft.Animation(
                200,
                ft.AnimationCurve.EASE_OUT
            ),

            content=ft.IconButton(

                icon=icone_normal,

                selected_icon=icone_selectionne,

                selected=True if index == 0 else False,

                icon_color="grey",

                selected_icon_color="black",

                icon_size=30,

                tooltip="",

                on_click=lambda e: (
                    selectionner(index),
                    fonction()
                ),
            ),
        )


    # --------------------------------------------------
    # ICÔNES DE LA BARRE
    # --------------------------------------------------

    icones = [

        creer_bouton_navigation(
            0,
            ft.Icons.HOME_OUTLINED,
            ft.Icons.HOME,
            page_acceuil
        ),

        creer_bouton_navigation(
            1,
            ft.Icons.CALENDAR_MONTH_OUTLINED,
            ft.Icons.CALENDAR_MONTH,
            page_planning
        ),

        creer_bouton_navigation(
            2,
            ft.Icons.FITNESS_CENTER_OUTLINED,
            ft.Icons.FITNESS_CENTER,
            page_seance
        ),

        creer_bouton_navigation(
            3,
            ft.Icons.ACCOUNT_CIRCLE_OUTLINED,
            ft.Icons.ACCOUNT_CIRCLE,
            page_profil
        ),
    ]


    # --------------------------------------------------
    # ANIMATION DE SÉLECTION
    # --------------------------------------------------

    def selectionner(index):

        global index_selectionne

        index_selectionne = index

        for i, bouton in enumerate(icones):

            icon_button = bouton.content

            if i == index:

                # ------------------------------------------
                # ICÔNE ACTIVE
                # ------------------------------------------

                bouton.bgcolor = "#FFFFFF"

                bouton.scale = 1.15

                bouton.width = 50
                bouton.height = 50

                icon_button.selected = True

                icon_button.icon_color = "black"

            else:

                # ------------------------------------------
                # ICÔNES INACTIVES
                # ------------------------------------------

                bouton.bgcolor = "transparent"

                bouton.scale = 1.0

                bouton.width = 40
                bouton.height = 40

                icon_button.selected = False

                icon_button.icon_color = "grey"

        page.update()


    # --------------------------------------------------
    # BARRE DE NAVIGATION
    # --------------------------------------------------
    def lancement():

        page.clean()

        barre_navigation = ft.Container(
            content=ft.Row(
                controls=icones,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor="#00000060",
            width=320,
            height=70,
            border_radius=40,
            padding=5,
        )

        page.add(
            ft.Column(
                controls=[

                    ft.Container(
                        content=contenu,
                        expand=True,
                        padding=ft.Padding(
                            0,
                            60,  # ← contenu plus bas
                            0,
                            0
                        ),
                    ),

                    ft.Container(
                        content=barre_navigation,
                        alignment=ft.Alignment(0, 0),
                        margin=ft.Margin(
                            0,
                            0,
                            0,
                            20,
                        ),
                    ),
                ],
                expand=True,
                spacing=0,
            )
        )

        page_acceuil()
        
    
    async def seance_recuperer_token():
        token = await ft.SharedPreferences().get("gomuscu.auth_token")
        print(token)
        if token:
                
            donnees= {"token":token}
            reponse = requests.post(API_URL + "/verify-session",json=donnees)
            resultat = reponse.json()
            print(resultat)
            if resultat["success"] == True:
                global nom_utilisateur
                global email
                utilisateur = resultat.get("utilisateur",{})
                nom_utilisateur = utilisateur.get("nom","Utilisateur")
                email = utilisateur.get("email","Utilisateur")
                return token
            else:
                afficher_message("Erreur Serveur")
        else:
            connexion_inscription()
    



    # --------------------------------------------------
    # STRUCTURE DE L'APPLICATION
    # --------------------------------------------------
    async def async_recuperer_token():
        token = await ft.SharedPreferences().get("gomuscu.auth_token")
        print(token)
        if token:
            
            donnees= {"token":token}
            reponse = requests.post(API_URL + "/verify-session",json=donnees)
            resultat = reponse.json()
            print(resultat)
            if resultat["success"] == True:
                global nom_utilisateur
                global email
                utilisateur = resultat.get("utilisateur",{})
                nom_utilisateur = utilisateur.get("nom","Utilisateur")
                email = utilisateur.get("email","Utilisateur")
                lancement()
                return token
            else:
                afficher_message("Erreur Serveur")
        else:
            connexion_inscription()

    def recuperer_token():
        return page.run_task(async_recuperer_token)

    recuperer_token()

    
ft.run(main, assets_dir="assets")