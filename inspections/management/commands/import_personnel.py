import pandas as pd
from django.core.management.base import BaseCommand
from inspections.models import Personnel

class Command(BaseCommand):
    help = "Importer des enseignants à visiter à partir d'un fichier Excel"

    def add_arguments(self, parser):
        parser.add_argument('fichier', type=str, help="Chemin du fichier Excel à importer")

    def handle(self, *args, **options):
        fichier = options['fichier']

        try:
            # Lire le fichier Excel
            df = pd.read_excel(fichier)

            # Vérifiez si les colonnes du fichier correspondent au modèle
            required_columns = [
                'som_enseignant', 'cin_enseignant', 'nom_enseignant',
                'cadre_enseignant', 'date_affect_enseignant', 'code_etab_enseignant',
                'etab_enseignant', 'specialite_enseignant', 'cycle_enseignant'
            ]

            if not all(col in df.columns for col in required_columns):
                self.stderr.write("Erreur : Le fichier Excel ne contient pas toutes les colonnes requises.")
                return

            # Ajouter les données dans le modèle
            for _, row in df.iterrows():
                personnel, created = Personnel.objects.update_or_create(
                    som_enseignant=row['som_enseignant'],  # Utilise som_enseignant comme identifiant unique
                    defaults={
                        'cin_enseignant': row['cin_enseignant'],
                        'nom_enseignant': row['nom_enseignant'],
                        'cadre_enseignant': row['cadre_enseignant'],
                        'date_affect_enseignant': row['date_affect_enseignant'],
                        'code_etab_enseignant': row['code_etab_enseignant'],
                        'etab_enseignant': row['etab_enseignant'],
                        'specialite_enseignant': row['specialite_enseignant'],
                        'cycle_enseignant': row['cycle_enseignant'],
                    }
                )
                if created:
                    self.stdout.write(f"Ajouté : {row['nom_enseignant']} ({row['som_enseignant']})")
                else:
                    self.stdout.write(f"Mis à jour : {row['nom_enseignant']} ({row['som_enseignant']})")

            self.stdout.write(self.style.SUCCESS("Importation réussie !"))

        except Exception as e:
            self.stderr.write(f"Erreur : {e}")

