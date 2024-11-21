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
        required=False,  # Champ rempli automatiquement
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
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le numéro de somme du premier accompagnateur'})
    )
    nom_premier_accompagnateur = forms.CharField(
        max_length=100,
        label="Nom du Premier Accompagnateur",
        widget=forms.TextInput(attrs={'placeholder': 'Nom du premier accompagnateur'})
    )
    etab_premier_accompagnateur = forms.CharField(
        max_length=100,
        label="Établissement du Premier Accompagnateur",
        widget=forms.TextInput(attrs={'placeholder': 'Établissement du premier accompagnateur'})
    )
    som_deuxieme_accompagnateur = forms.CharField(
        max_length=20,
        label="Numéro de Somme du Deuxième Accompagnateur",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le numéro de somme du deuxième accompagnateur'})
    )
    nom_deuxieme_accompagnateur = forms.CharField(
        max_length=100,
        label="Nom du Deuxième Accompagnateur",
        widget=forms.TextInput(attrs={'placeholder': 'Nom du deuxième accompagnateur'})
    )
    etab_deuxieme_accompagnateur = forms.CharField(
        max_length=100,
        label="Établissement du Deuxième Accompagnateur",
        widget=forms.TextInput(attrs={'placeholder': 'Établissement du deuxième accompagnateur'})
    )
    date_visite = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Sélectionnez la date de la visite'}),
        label="Date de la Visite"
    )
    heure_visite = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'placeholder': 'Sélectionnez l’heure de la visite'}),
        label="Heure de la Visite"
    )
    centre_visite = forms.CharField(
        max_length=100,
        label="Centre de la Visite",
        widget=forms.TextInput(attrs={'placeholder': 'Entrez le centre de la visite'})
    )

    class Meta:
        model = Visite
        fields = [
            'numero_somme_enseignant',
            'nom_enseignant',
            'som_inspecteur', 'nom_inspecteur',
            'som_premier_accompagnateur', 'nom_premier_accompagnateur', 'etab_premier_accompagnateur',
            'som_deuxieme_accompagnateur', 'nom_deuxieme_accompagnateur', 'etab_deuxieme_accompagnateur',
            'date_visite', 'heure_visite', 'centre_visite'
        ]

    def __init__(self, *args, **kwargs):
        """
        Initialisation personnalisée pour les champs en mode lecture.
        """
        super().__init__(*args, **kwargs)

        if 'instance' in kwargs and kwargs['instance']:
            # Pré-remplir "Numéro de somme" et "Nom de l'enseignant"
            self.fields['numero_somme_enseignant'].initial = kwargs['instance'].enseignant_visite.som_enseignant
            self.fields['numero_somme_enseignant'].widget.attrs['readonly'] = 'readonly'

            self.fields['nom_enseignant'].initial = kwargs['instance'].enseignant_visite.nom_enseignant
            self.fields['nom_enseignant'].widget.attrs['readonly'] = 'readonly'

    def clean(self):
        """
        Vérifie que tous les champs sont remplis.
        """
        cleaned_data = super().clean()

        # Vérification des champs obligatoires
        required_fields = [
            'numero_somme_enseignant', 'nom_enseignant', 'som_inspecteur', 'nom_inspecteur',
            'som_premier_accompagnateur', 'nom_premier_accompagnateur', 'etab_premier_accompagnateur',
            'som_deuxieme_accompagnateur', 'nom_deuxieme_accompagnateur', 'etab_deuxieme_accompagnateur',
            'date_visite', 'heure_visite', 'centre_visite'
        ]

        for field in required_fields:
            if not cleaned_data.get(field):
                self.add_error(field, "Ce champ est obligatoire.")

        return cleaned_data


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
