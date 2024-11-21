from django.db import models

class Personnel(models.Model):
    som_enseignant = models.CharField(max_length=20, unique=True)
    cin_enseignant = models.CharField(max_length=20)
    nom_enseignant = models.CharField(max_length=100)
    cadre_enseignant = models.CharField(max_length=100)
    date_affect_enseignant = models.DateField()
    code_etab_enseignant = models.CharField(max_length=20)
    etab_enseignant = models.CharField(max_length=100)
    specialite_enseignant = models.CharField(max_length=100)
    cycle_enseignant = models.CharField(max_length=50)

    def __str__(self):
        return self.nom_enseignant

class Visite(models.Model):
    enseignant_visite = models.ForeignKey(Personnel, on_delete=models.CASCADE, related_name="visites")
    som_inspecteur = models.CharField(max_length=20)
    nom_inspecteur = models.CharField(max_length=100)
    som_premier_accompagnateur = models.CharField(max_length=20, blank=True, null=True)
    nom_premier_accompagnateur = models.CharField(max_length=100, blank=True, null=True)
    etab_premier_accompagnateur = models.CharField(max_length=100, blank=True, null=True)
    som_deuxieme_accompagnateur = models.CharField(max_length=20, blank=True, null=True)
    nom_deuxieme_accompagnateur = models.CharField(max_length=100, blank=True, null=True)
    etab_deuxieme_accompagnateur = models.CharField(max_length=100, blank=True, null=True)
    date_visite = models.DateField()
    heure_visite = models.TimeField()
    centre_visite = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('Programmée', 'Programmée'),
        ('Annulée', 'Annulée'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Programmée'
    )


    def __str__(self):
        return f"Visite de {self.enseignant_visite.nom_enseignant} par {self.nom_inspecteur} le {self.date_visite}"

    class Meta:
        permissions = [
            ("print_visite", "Can print visite"),
        ]