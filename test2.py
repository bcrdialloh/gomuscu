
import flet as ft
import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://192.168.1.35:5000"


# ============================================================
# APPLICATION
# ============================================================

def main(page: ft.Page):

    # --------------------------------------------------------
    # CONFIGURATION DE LA PAGE
    # --------------------------------------------------------

    page.title = "GoMuscu"
    page.bgcolor = "#C9DDE7"

    # Empêche certains débordements sur mobile
    page.padding = 0

    # --------------------------------------------------------
    # COULEURS
    # --------------------------------------------------------

    BG_COLOR = "#C9DDE7"
    WHITE = "#FFFFFF"
    BLACK = "#000000"
    GREY = "#777777"
    DARK_GREY = "#555555"

    # --------------------------------------------------------
    # VARIABLES
    # --------------------------------------------------------

    nom_utilisateur = "Bachir"

    # ========================================================
    # FONCTIONS UTILITAIRES
    # ========================================================

    def afficher_message(message, couleur=BLACK):
        """
        Affiche un message en bas de l'écran.
        """

        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(
                    message,
                    color=WHITE,
                ),
            )
        )

    # ========================================================
    # INSCRIPTION
    # ========================================================

    def inscription(nom, mail, mdp):

        # Vérification basique
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
            "mot_de_passe": mdp
        }

        try:

            print("Envoi de l'inscription...")
            print("Données :", donnees)

            reponse = requests.post(
                API_URL + "/register",
                json=donnees,
                timeout=10
            )

            print("STATUS :", reponse.status_code)
            print(
                "TYPE :",
                reponse.headers.get("Content-Type")
            )
            print("REPONSE :", reponse.text)

            # ------------------------------------------------
            # SUCCÈS
            # ------------------------------------------------

            if 200 <= reponse.status_code < 300:

                afficher_message(
                    "Compte créé avec succès !"
                )

                # Retour à la connexion
                page.navigate("/login")

            # ------------------------------------------------
            # ERREUR SERVEUR
            # ------------------------------------------------

            else:

                try:
                    resultat = reponse.json()

                    message = resultat.get(
                        "message",
                        "Une erreur est survenue."
                    )

                except Exception:

                    message = reponse.text

                afficher_message(
                    f"Erreur : {message}"
                )

        # ----------------------------------------------------
        # SERVEUR INACCESSIBLE
        # ----------------------------------------------------

        except requests.exceptions.ConnectionError:

            afficher_message(
                "Impossible de contacter le serveur."
            )

            print(
                "ERREUR : serveur inaccessible."
            )

        # ----------------------------------------------------
        # TIMEOUT
        # ----------------------------------------------------

        except requests.exceptions.Timeout:

            afficher_message(
                "Le serveur met trop de temps à répondre."
            )

        # ----------------------------------------------------
        # AUTRE ERREUR
        # ----------------------------------------------------

        except Exception as erreur:

            afficher_message(
                "Une erreur est survenue."
            )

            print(
                "ERREUR INSCRIPTION :",
                erreur
            )

    # ========================================================
    # CONNEXION
    # ========================================================
    def connexion(mail, mdp):

        if not mail.strip():
            afficher_message(
                "Veuillez entrer votre adresse mail."
            )
            return

        if not mdp.strip():
            afficher_message(
                "Veuillez entrer votre mot de passe."
            )
            return

        donnees = {
            "email": mail,
            "mot_de_passe": mdp
        }

        print("Tentative de connexion...")
        print("Données :", donnees)

        try:

            reponse = requests.post(
                API_URL + "/login",
                json=donnees,
                timeout=10
            )

            print("STATUS :", reponse.status_code)
            print("REPONSE :", reponse.text)

            if reponse.status_code == 200:

                resultat = reponse.json()

                print("RESULTAT :", resultat)

                if resultat.get("success"):

                    # Récupération du nom envoyé par Flask
                    utilisateur = resultat.get(
                        "utilisateur",
                        {}
                    )

                    global nom_utilisateur

                    nom_utilisateur = utilisateur.get(
                        "nom",
                        "Utilisateur"
                    )

                    print(
                        "Connexion réussie pour :",
                        nom_utilisateur
                    )

                    print(
                        "Route avant navigation :",
                        page.route
                    )

                    page.navigate("/home")

                    print(
                        "Route après navigation :",
                        page.route
                    )

                else:

                    afficher_message(
                        resultat.get(
                            "message",
                            "Identifiants incorrects."
                        )
                    )

            else:

                try:

                    resultat = reponse.json()

                    afficher_message(
                        resultat.get(
                            "message",
                            "Identifiants incorrects."
                        )
                    )

                except Exception:

                    afficher_message(
                        "Identifiants incorrects."
                    )

        except requests.exceptions.ConnectionError:

            afficher_message(
                "Impossible de contacter le serveur."
            )

        except requests.exceptions.Timeout:

            afficher_message(
                "Le serveur met trop de temps à répondre."
            )

        except Exception as erreur:

            print(
                "ERREUR CONNEXION :",
                erreur
            )

            afficher_message(
                "Erreur lors de la connexion."
            )

    # ========================================================
    # PAGE DE CONNEXION
    # ========================================================

    def vue_connexion():

        # ----------------------------------------------------
        # CHAMPS
        # ----------------------------------------------------

        champ_mail = ft.TextField(
            hint_text="Adresse mail",

            text_style=ft.TextStyle(
                color=BLACK
            ),

            hint_style=ft.TextStyle(
                color=GREY
            ),

            prefix_icon=ft.Icons.EMAIL_OUTLINED,

            border_radius=15,
            border_width=0,

            filled=True,
            bgcolor=WHITE,

            width=320,
            height=55,
        )

        champ_mdp = ft.TextField(
            hint_text="Mot de passe",

            text_style=ft.TextStyle(
                color=BLACK
            ),

            hint_style=ft.TextStyle(
                color=GREY
            ),

            prefix_icon=ft.Icons.LOCK_OUTLINE,

            password=True,
            can_reveal_password=True,

            border_radius=15,
            border_width=0,

            filled=True,
            bgcolor=WHITE,

            width=320,
            height=70,
        )

        # ----------------------------------------------------
        # BOUTON CONNEXION
        # ----------------------------------------------------

        bouton_connexion = ft.Button(
            content="Se connecter",

            width=320,
            height=55,

            on_click=lambda e: connexion(
                champ_mail.value,
                champ_mdp.value
            ),
        )

        # ----------------------------------------------------
        # BOUTON INSCRIPTION
        # ----------------------------------------------------

        bouton_inscription = ft.Button(
            content="Créer un compte",

            width=320,
            height=55,

            on_click=lambda e: page.navigate(
                "/register"
            ),
        )

        # ----------------------------------------------------
        # FORMULAIRE
        # ----------------------------------------------------

        formulaire = ft.Container(

            content=ft.Column(

                controls=[

                    ft.Text(
                        "Bienvenue",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        "Connectez-vous à votre compte GoMuscu",

                        size=14,

                        color=DARK_GREY,

                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(
                        height=15
                    ),

                    champ_mail,

                    champ_mdp,

                    ft.Container(
                        height=5
                    ),

                    bouton_connexion,

                    bouton_inscription,
                ],

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=12,
            ),

            width=360,

            padding=25,

            border_radius=25,

            bgcolor="#00000015",
        )

        # ----------------------------------------------------
        # VIEW
        # ----------------------------------------------------

        return ft.View(

            route="/login",

            bgcolor=BG_COLOR,

            controls=[

                ft.SafeArea(

                    content=ft.Container(

                        content=formulaire,

                        alignment=ft.Alignment(
                            0,
                            0
                        ),

                        expand=True,
                    ),

                    expand=True,
                )
            ],
        )

    # ========================================================
    # PAGE INSCRIPTION
    # ========================================================

    def vue_inscription():

        # ----------------------------------------------------
        # NOM
        # ----------------------------------------------------

        champ_nom = ft.TextField(
            hint_text="Nom",

            text_style=ft.TextStyle(
                color=BLACK
            ),

            hint_style=ft.TextStyle(
                color=GREY
            ),

            prefix_icon=ft.Icons.PERSON_OUTLINE,

            border_radius=15,
            border_width=0,

            filled=True,
            bgcolor=WHITE,

            width=320,
            height=55,
        )

        # ----------------------------------------------------
        # MAIL
        # ----------------------------------------------------

        champ_mail = ft.TextField(
            hint_text="Adresse mail",

            text_style=ft.TextStyle(
                color=BLACK
            ),

            hint_style=ft.TextStyle(
                color=GREY
            ),

            prefix_icon=ft.Icons.EMAIL_OUTLINED,

            border_radius=15,
            border_width=0,

            filled=True,
            bgcolor=WHITE,

            width=320,
            height=55,
        )

        # ----------------------------------------------------
        # MOT DE PASSE
        # ----------------------------------------------------

        champ_mdp = ft.TextField(
            hint_text="Mot de passe",

            text_style=ft.TextStyle(
                color=BLACK
            ),

            hint_style=ft.TextStyle(
                color=GREY
            ),

            prefix_icon=ft.Icons.LOCK_OUTLINE,

            password=True,

            can_reveal_password=True,

            border_radius=15,
            border_width=0,

            filled=True,
            bgcolor=WHITE,

            width=320,
            height=70,
        )

        # ----------------------------------------------------
        # BOUTON INSCRIPTION
        # ----------------------------------------------------

        bouton_inscription = ft.Button(
            content="Créer mon compte",

            width=320,
            height=55,

            on_click=lambda e: inscription(
                champ_nom.value,
                champ_mail.value,
                champ_mdp.value
            ),
        )

        # ----------------------------------------------------
        # BOUTON CONNEXION
        # ----------------------------------------------------

        bouton_connexion = ft.Button(
            content="Se connecter",

            width=320,
            height=55,

            on_click=lambda e: page.navigate(
                "/login"
            ),
        )

        # ----------------------------------------------------
        # FORMULAIRE
        # ----------------------------------------------------

        formulaire = ft.Container(

            content=ft.Column(

                controls=[

                    ft.Text(
                        "Créer un compte",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        "Créez votre compte GoMuscu",

                        size=14,

                        color=DARK_GREY,

                        text_align=ft.TextAlign.CENTER,
                    ),

                    ft.Container(
                        height=15
                    ),

                    champ_nom,

                    champ_mail,

                    champ_mdp,

                    ft.Container(
                        height=5
                    ),

                    bouton_inscription,

                    bouton_connexion,
                ],

                horizontal_alignment=(
                    ft.CrossAxisAlignment.CENTER
                ),

                spacing=12,
            ),

            width=360,

            padding=25,

            border_radius=25,

            bgcolor="#00000015",
        )

        # ----------------------------------------------------
        # VIEW
        # ----------------------------------------------------

        return ft.View(

            route="/register",

            bgcolor=BG_COLOR,

            controls=[

                ft.SafeArea(

                    content=ft.Container(

                        content=formulaire,

                        alignment=ft.Alignment(
                            0,
                            0
                        ),

                        expand=True,
                    ),

                    expand=True,
                )
            ],
        )

    # ========================================================
    # NAVIGATION BAR
    # ========================================================

    def navigation_bar():

        # ----------------------------------------------------
        # DÉTERMINER LA PAGE ACTIVE
        # ----------------------------------------------------

        route = page.route

        if route == "/home":
            selected_index = 0

        elif route == "/planning":
            selected_index = 1

        elif route == "/seance":
            selected_index = 2

        elif route == "/profil":
            selected_index = 3

        else:
            selected_index = 0

        # ----------------------------------------------------
        # NAVIGATION
        # ----------------------------------------------------

        def changement_navigation(e):

            index = e.control.selected_index

            routes = [
                "/home",
                "/planning",
                "/seance",
                "/profil",
            ]

            if 0 <= index < len(routes):

                page.navigate(
                    routes[index]
                )

        # ----------------------------------------------------
        # BARRE
        # ----------------------------------------------------

        return ft.NavigationBar(

            selected_index=selected_index,

            on_change=changement_navigation,

            bgcolor="#00000060",

            destinations=[

                ft.NavigationBarDestination(

                    icon=ft.Icons.HOME_OUTLINED,

                    selected_icon=ft.Icons.HOME,

                    label="Accueil",
                ),

                ft.NavigationBarDestination(

                    icon=(
                        ft.Icons.CALENDAR_MONTH_OUTLINED
                    ),

                    selected_icon=(
                        ft.Icons.CALENDAR_MONTH
                    ),

                    label="Planning",
                ),

                ft.NavigationBarDestination(

                    icon=(
                        ft.Icons.FITNESS_CENTER_OUTLINED
                    ),

                    selected_icon=(
                        ft.Icons.FITNESS_CENTER
                    ),

                    label="Séance",
                ),

                ft.NavigationBarDestination(

                    icon=(
                        ft.Icons.ACCOUNT_CIRCLE_OUTLINED
                    ),

                    selected_icon=(
                        ft.Icons.ACCOUNT_CIRCLE
                    ),

                    label="Profil",
                ),
            ],
        )

    # ========================================================
    # PAGE PRINCIPALE DE L'APPLICATION
    # ========================================================

    def vue_application():
        global nom_utilisateur
        # ----------------------------------------------------
        # CONTENU
        # ----------------------------------------------------

        if page.route == "/home":
            print("home")

            contenu = ft.Column(

                controls=[

                    ft.Text(
                        f"Ravi de vous revoir, "
                        f"{nom_utilisateur}",

                        size=16,

                        color=BLACK,
                    ),

                    ft.Container(
                        height=20
                    ),

                    ft.Text(
                        "Accueil",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        "Prêt pour ta prochaine séance ?",

                        size=16,

                        color=DARK_GREY,
                    ),
                ],

                spacing=10,
            )

        # ----------------------------------------------------
        # PLANNING
        # ----------------------------------------------------

        elif page.route == "/planning":

            contenu = ft.Column(

                controls=[

                    ft.Text(
                        "Planning",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        "Ton planning d'entraînement",

                        size=16,

                        color=DARK_GREY,
                    ),
                ],

                spacing=10,
            )

        # ----------------------------------------------------
        # SÉANCE
        # ----------------------------------------------------

        elif page.route == "/seance":

            contenu = ft.Column(

                controls=[

                    ft.Text(
                        "Séance",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        "Commence ton entraînement",

                        size=16,

                        color=DARK_GREY,
                    ),
                ],

                spacing=10,
            )

        # ----------------------------------------------------
        # PROFIL
        # ----------------------------------------------------

        elif page.route == "/profil":

            contenu = ft.Column(

                controls=[

                    ft.Text(
                        "Profil",

                        size=30,

                        weight=ft.FontWeight.BOLD,

                        color=BLACK,
                    ),

                    ft.Text(
                        f"Utilisateur : "
                        f"{nom_utilisateur}",

                        size=16,

                        color=DARK_GREY,
                    ),

                    ft.Container(
                        height=20
                    ),

                    ft.Button(
                        content="Se déconnecter",

                        width=250,

                        height=50,

                        on_click=lambda e: (
                            page.navigate("/login")
                        ),
                    ),
                ],

                spacing=10,
            )

        # ----------------------------------------------------
        # VIEW APPLICATION
        # ----------------------------------------------------

        return ft.View(

            route=page.route,

            bgcolor=BG_COLOR,

            padding=20,

            navigation_bar=navigation_bar(),

            controls=[

                ft.SafeArea(

                    content=ft.Container(

                        content=contenu,

                        expand=True,

                    ),

                    expand=True,
                )
            ],
        )

    # ========================================================
    # ROUTAGE
    # ========================================================

    def route_change(e=None):

        print(
            "Nouvelle route :",
            page.route
        )

        # ----------------------------------------------------
        # VÉRIFICATION DE LA ROUTE
        # ----------------------------------------------------

        routes_auth = [
            "/login",
            "/register",
        ]

        routes_app = [
            "/home",
            "/planning",
            "/seance",
            "/profil",
        ]

        # ----------------------------------------------------
        # ROUTE INCONNUE
        # ----------------------------------------------------

        if (
            page.route not in routes_auth
            and page.route not in routes_app
        ):

            page.navigate("/login")

            return

        # ----------------------------------------------------
        # RECONSTRUCTION DES VIEWS
        # ----------------------------------------------------

        page.views.clear()

        # ----------------------------------------------------
        # LOGIN
        # ----------------------------------------------------

        if page.route == "/login":

            page.views.append(
                vue_connexion()
            )

        # ----------------------------------------------------
        # REGISTER
        # ----------------------------------------------------

        elif page.route == "/register":

            page.views.append(
                vue_inscription()
            )

        # ----------------------------------------------------
        # APPLICATION
        # ----------------------------------------------------

        elif page.route in routes_app:

            page.views.append(
                vue_application()
            )

        # ----------------------------------------------------
        # UPDATE
        # ----------------------------------------------------

        page.update()

    # ========================================================
    # RETOUR ARRIÈRE
    # ========================================================

    async def view_pop(e):

        print(
            "Retour arrière :",
            e.view.route if e.view else None
        )

        if e.view is not None:

            page.views.remove(
                e.view
            )

            if page.views:

                route = page.views[-1].route

                await page.push_route(
                    route
                )

    # ========================================================
    # ÉVÉNEMENTS DE NAVIGATION
    # ========================================================

    page.on_route_change = route_change

    page.on_view_pop = view_pop

    # ========================================================
    # ROUTE DE DÉPART
    # ========================================================

    page.route = "/login"

    route_change()


# ============================================================
# LANCEMENT
# ============================================================

if __name__ == "__main__":
    ft.run(main)

