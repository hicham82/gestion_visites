from django import forms
from .models import Visite


class VisiteForm(forms.ModelForm):
    numero_somme_enseignant = forms.CharField(
        max_length=20,
        label="Numéro de Somme de l'Enseignant à Visiter",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le numéro de somme'})
    )
    nom_enseignant = forms.CharField(
        max_length=100,
        label="Nom de l'Enseignant",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'Nom de l’enseignant automatique'})
    )
    som_inspecteur = forms.CharField(
        max_length=20,
        label="Numéro de Somme de l'Inspecteur",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre numéro de somme'})
    )
    nom_inspecteur = forms.CharField(
        max_length=100,
        label="Nom de l'Inspecteur",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez votre nom'})
    )
    som_premier_accompagnateur = forms.CharField(
        max_length=20,
        label="Numéro de Somme du Premier Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le numéro de somme du premier accompagnateur'})
    )
    nom_premier_accompagnateur = forms.CharField(
        max_length=100,
        label="Nom du Premier Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom du premier accompagnateur'})
    )
    etab_premier_accompagnateur = forms.CharField(
        max_length=100,
        label="Établissement du Premier Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Établissement du premier accompagnateur'})
    )
    som_deuxieme_accompagnateur = forms.CharField(
        max_length=20,
        label="Numéro de Somme du Deuxième Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le numéro de somme du deuxième accompagnateur'})
    )
    nom_deuxieme_accompagnateur = forms.CharField(
        max_length=100,
        label="Nom du Deuxième Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nom du deuxième accompagnateur'})
    )
    etab_deuxieme_accompagnateur = forms.CharField(
        max_length=100,
        label="Établissement du Deuxième Accompagnateur",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Établissement du deuxième accompagnateur'})
    )
    date_visite = forms.DateField(
        widget=forms.TextInput(attrs={'placeholder': 'Sélectionnez la date de la visite'})
    )
    heure_visite = forms.TimeField(
        widget=forms.TextInput(attrs={'placeholder': 'Sélectionnez l’heure de la visite'})
    )
    centre_visite = forms.CharField(
        max_length=100,
        label="Centre de la Visite",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le centre de la visite'})
    )

    class Meta:
        model = Visite
        fields = [
            'numero_somme_enseignant', 'nom_enseignant', 'som_inspecteur', 'nom_inspecteur',
            'som_premier_accompagnateur', 'nom_premier_accompagnateur', 'etab_premier_accompagnateur',
            'som_deuxieme_accompagnateur', 'nom_deuxieme_accompagnateur', 'etab_deuxieme_accompagnateur',
            'date_visite', 'heure_visite', 'centre_visite'
        ]

class FiltreVisitesForm(forms.Form):
    date_visite = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date de la visite"
    )
    nom_enseignant = forms.CharField(
        max_length=100,
        required=False,
        label="Nom ou numéro de somme de l'enseignant"
    )
    nom_inspecteur = forms.CharField(
        max_length=100,
        required=False,
        label="Nom ou numéro de somme de l'inspecteur"
    )


