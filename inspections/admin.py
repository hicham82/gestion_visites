import openpyxl
from django.contrib import admin
from django.http import HttpResponse
from django.contrib.admin import SimpleListFilter
from datetime import datetime
from .models import Visite, Personnel


# Action pour exporter en Excel
def export_visites_xlsx(modeladmin, request, queryset):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Visites Programmées"

    headers = [
        "Date Visite", "Heure Visite", "Centre de Visite",
        "Nom Enseignant", "Numéro de Somme", "Établissement Enseignant", "Spécialité Enseignant",
        "Nom Inspecteur", "Numéro de Somme Inspecteur",
        "Nom Accompagnateur 1", "Numéro de Somme Accompagnateur 1", "Établissement Accompagnateur 1",
        "Nom Accompagnateur 2", "Numéro de Somme Accompagnateur 2", "Établissement Accompagnateur 2",
        "Statut"
    ]
    sheet.append(headers)

    for visite in queryset:
        sheet.append([
            visite.date_visite,
            visite.heure_visite,
            visite.centre_visite,
            visite.enseignant_visite.nom_enseignant,
            visite.enseignant_visite.som_enseignant,
            visite.enseignant_visite.etab_enseignant,
            visite.enseignant_visite.specialite_enseignant,
            visite.nom_inspecteur,
            visite.som_inspecteur,
            visite.nom_premier_accompagnateur,
            visite.som_premier_accompagnateur,
            visite.etab_premier_accompagnateur,
            visite.nom_deuxieme_accompagnateur,
            visite.som_deuxieme_accompagnateur,
            visite.etab_deuxieme_accompagnateur,
            visite.status
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="visites_programmées.xlsx"'
    workbook.save(response)
    return response


# Filtre personnalisé pour une date précise
class DatePreciseFilter(SimpleListFilter):
    title = "Date précise"
    parameter_name = "date_precise"

    def lookups(self, request, model_admin):
        return []  # Aucun choix pré-défini

    def queryset(self, request, queryset):
        if self.value():
            try:
                selected_date = datetime.strptime(self.value(), "%Y-%m-%d").date()
                return queryset.filter(date_visite=selected_date)
            except ValueError:
                pass
        return queryset

    def choices(self, changelist):
        form = f"""
            <input type="date" name="{self.parameter_name}" 
                   value="{self.value() or ''}" 
                   style="margin-left: 10px; margin-right: 10px; width: 150px;"
                   onchange="this.form.submit()">
        """
        return [{
            "query_string": changelist.get_query_string({}, [self.parameter_name]),
            "display": form,
        }]




# Classe Admin pour Visite
from django.contrib.admin import DateFieldListFilter

class VisiteAdmin(admin.ModelAdmin):
    list_display = ('enseignant_visite', 'nom_inspecteur', 'date_visite', 'status')
    list_filter = (
        ('date_visite', DateFieldListFilter),  # Filtre intégré Django
        'nom_inspecteur',  # Filtre par inspecteur
        'enseignant_visite',  # Filtre par enseignant
        'status',  # Filtre par statut
    )
    search_fields = ('nom_inspecteur', 'enseignant_visite__nom_enseignant')
    actions = [export_visites_xlsx]

    def enseignant_visite_nom(self, obj):
        return obj.enseignant_visite.nom_enseignant

    enseignant_visite_nom.admin_order_field = 'enseignant_visite__nom_enseignant'




# Enregistrement du modèle Personnel dans l'interface admin
class PersonnelAdmin(admin.ModelAdmin):
    list_display = ('nom_enseignant', 'som_enseignant', 'etab_enseignant', 'specialite_enseignant')
    search_fields = ('nom_enseignant', 'som_enseignant', 'etab_enseignant')


# Enregistrement des modèles
admin.site.register(Visite, VisiteAdmin)
admin.site.register(Personnel, PersonnelAdmin)
