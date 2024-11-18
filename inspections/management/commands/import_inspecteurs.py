import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Importer des inspecteurs à partir d'un fichier Excel"

    def add_arguments(self, parser):
        parser.add_argument('fichier', type=str, help="Chemin du fichier Excel à importer")

    def handle(self, *args, **options):
        fichier = options['fichier']

        try:
            # Lire le fichier Excel
            df = pd.read_excel(fichier)

            # Vérifiez que toutes les colonnes nécessaires existent
            required_columns = ['nom_inspecteur', 'email_inspecteur', 'password_inspecteur']
            if not all(col in df.columns for col in required_columns):
                self.stderr.write("Erreur : Le fichier Excel doit contenir les colonnes suivantes : nom_inspecteur, email_inspecteur, password_inspecteur")
                return

            # Ajouter chaque inspecteur au système
            for _, row in df.iterrows():
                email = row['email_inspecteur']
                password = row['password_inspecteur']

                # Vérifiez si l'utilisateur existe déjà
                if User.objects.filter(email=email).exists():
                    self.stdout.write(f"Utilisateur existant : {email}")
                else:
                    # Créez le compte utilisateur
                    user = User.objects.create_user(
                        username=row['nom_inspecteur'],
                        email=email,
                        password=password
                    )
                    user.is_staff = True  # Définir comme utilisateur ayant accès à l'administration
                    user.save()
                    self.stdout.write(f"Inspecteur ajouté : {row['nom_inspecteur']} ({email})")

            self.stdout.write(self.style.SUCCESS("Importation des inspecteurs terminée avec succès !"))

        except Exception as e:
            self.stderr.write(f"Erreur lors de l'importation : {e}")
