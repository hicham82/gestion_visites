from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import pandas as pd
from .models import  Visite
from .forms import VisiteForm
from .models import Personnel
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import VisiteForm, FiltreVisitesForm
from django.contrib import messages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from bidi.algorithm import get_display
from arabic_reshaper import reshape
from io import BytesIO
import zipfile
import os
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, Func, Value
from django.db.models.functions import ExtractMonth, ExtractYear
from calendar import month_name  # Pour récupérer les noms des mois
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from django.conf import settings
from babel.dates import format_date, get_day_names
import locale
from babel.dates import format_date








def creer_visite(request):
    form = VisiteForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            numero_somme = form.cleaned_data['numero_somme_enseignant']
            try:
                # Vérifie si l'enseignant existe
                enseignant = Personnel.objects.get(som_enseignant=numero_somme)

                # Annule une ancienne visite si elle existe
                ancienne_visite = Visite.objects.filter(
                    enseignant_visite=enseignant, status='Programmée'
                ).first()
                if ancienne_visite:
                    ancienne_visite.status = 'Annulée'
                    ancienne_visite.save()
                    messages.info(request, f"L'ancienne visite pour {enseignant.nom_enseignant} a été annulée.")

                # Crée une nouvelle visite
                nouvelle_visite = form.save(commit=False)
                nouvelle_visite.enseignant_visite = enseignant
                nouvelle_visite.status = 'Programmée'
                nouvelle_visite.save()

                messages.success(request, f"La visite pour {enseignant.nom_enseignant} a été programmée avec succès !")
                return redirect('confirmation_visite', visite_id=nouvelle_visite.id)

            except Personnel.DoesNotExist:
                form.add_error('numero_somme_enseignant', 'Numéro de somme introuvable')
        else:
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')

    return render(request, 'creer_visite.html', {'form': form})

    return render(request, 'creer_visite.html', {'form': form})
def obtenir_nom_enseignant(request):
    numero_somme = request.GET.get('numero_somme')
    if not numero_somme:
        return JsonResponse({'error': 'Numéro de somme manquant'}, status=400)
    try:
        enseignant = Personnel.objects.get(som_enseignant=numero_somme)
        return JsonResponse({'nom_enseignant': enseignant.nom_enseignant})
    except Personnel.DoesNotExist:
        return JsonResponse({'error': 'Numéro de somme introuvable'}, status=404)
def confirmation_visite(request, visite_id):
    visite = get_object_or_404(Visite, pk=visite_id)
    return render(request, 'confirmation_visite.html', {'visite': visite})
@login_required
def liste_visites(request):
    form = FiltreVisitesForm(request.GET or None)

    # Filtrer uniquement les visites programmées
    visites = Visite.objects.filter(status='Programmée').order_by('date_visite')

    # Application des filtres si le formulaire est valide
    if form.is_valid():
        date_visite = form.cleaned_data.get('date_visite')
        nom_enseignant = form.cleaned_data.get('nom_enseignant')
        nom_inspecteur = form.cleaned_data.get('nom_inspecteur')

        if date_visite:
            visites = visites.filter(date_visite=date_visite)
        if nom_enseignant:
            visites = visites.filter(
                Q(enseignant_visite__nom_enseignant__icontains=nom_enseignant) |
                Q(enseignant_visite__som_enseignant__icontains=nom_enseignant)
            )
        if nom_inspecteur:
            visites = visites.filter(
                Q(nom_inspecteur__icontains=nom_inspecteur) |
                Q(som_inspecteur__icontains=nom_inspecteur)
            )

    # Pagination avec conservation des paramètres
    paginator = Paginator(visites, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Conserver les paramètres de la requête
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')

    # Gestion des permissions
    user_has_full_control = request.user.has_perm('inspections.change_visite')
    can_print = request.user.has_perm('inspections.print_visite')

    # Retourne le contexte au template
    return render(request, 'liste_visites.html', {
        'form': form,
        'page_obj': page_obj,
        'query_params': query_params,
        'user_has_full_control': user_has_full_control,
        'can_print': can_print,
    })
@permission_required('inspections.change_visite', raise_exception=True)
def modifier_visite(request, id):
    visite = get_object_or_404(Visite, id=id)  # Charger la visite concernée
    if request.method == 'POST':
        # Formulaire avec données soumises (et instance existante)
        form = VisiteForm(request.POST, instance=visite)
        if form.is_valid():
            form.save()  # Sauvegarder les modifications
            return redirect('liste_visites')  # Redirection après modification
    else:
        # Formulaire pré-rempli pour modification
        form = VisiteForm(instance=visite)
    return render(request, 'modifier_visite.html', {'form': form})

@permission_required('inspections.delete_visite', raise_exception=True)
def supprimer_visite(request, id):
    visite = get_object_or_404(Visite, id=id)
    if request.method == 'POST':
        visite.delete()  # Supprime la visite de la base de données
        return redirect('liste_visites')  # Redirige vers la liste des visites après suppression
    return render(request, 'supprimer_visite.html', {'visite': visite})
@require_POST
def telecharger_visites_excel(request):
    # Récupère les IDs des visites sélectionnées
    visite_ids = request.POST.getlist('visite_ids')

    # Récupère les visites correspondantes dans la base de données
    visites = Visite.objects.filter(id__in=visite_ids)

    # Prépare les données pour l'export
    data = []
    for visite in visites:
        data.append({
            'Numéro de Somme de l’Enseignant': visite.enseignant_visite.som_enseignant,
            'Nom de l’Enseignant': visite.enseignant_visite.nom_enseignant,
            'CIN': visite.enseignant_visite.cin_enseignant,
            'Cadre': visite.enseignant_visite.cadre_enseignant,
            'Établissement': visite.enseignant_visite.etab_enseignant,
            'Spécialité': visite.enseignant_visite.specialite_enseignant,
            'Cycle': visite.enseignant_visite.cycle_enseignant,
            'Numéro de Somme de l’Inspecteur': visite.som_inspecteur,
            'Nom de l’Inspecteur': visite.nom_inspecteur,
            'Date de la Visite': visite.date_visite,
            'Heure de la Visite': visite.heure_visite,
            'Centre de la Visite': visite.centre_visite,
            'Numéro de Somme du Premier Accompagnateur': visite.som_premier_accompagnateur,
            'Nom du Premier Accompagnateur': visite.nom_premier_accompagnateur,
            'Établissement du Premier Accompagnateur': visite.etab_premier_accompagnateur,
            'Numéro de Somme du Deuxième Accompagnateur': visite.som_deuxieme_accompagnateur,
            'Nom du Deuxième Accompagnateur': visite.nom_deuxieme_accompagnateur,
            'Établissement du Deuxième Accompagnateur': visite.etab_deuxieme_accompagnateur,
        })

    # Créer un DataFrame avec Pandas
    df = pd.DataFrame(data)

    # Générer le fichier Excel
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="visites_selectionnees.xlsx"'
    df.to_excel(response, index=False)

    return response
def afficher_details_visite(request, visite_id):
    visite = get_object_or_404(Visite, id=visite_id)
    return render(request, 'afficher_details_visite.html', {'visite': visite})

# Helper function to draw Arabic text
def draw_arabic_text(c, x, y, text):
    reshaped_text = reshape(text)  # Reshape Arabic for correct display
    bidi_text = get_display(reshaped_text)  # Apply BiDi algorithm for RTL alignment
    c.drawRightString(x, y, bidi_text)  # Align text to the right

# Function to generate and download convocations
@permission_required('inspections.print_visite', raise_exception=True)
def print_visite(request, visite_id):
    visite = get_object_or_404(Visite, id=visite_id)

    # Conversion de la date en arabe
    day_name_ar = format_date(visite.date_visite, "EEEE", locale='ar')
    date_ar = visite.date_visite.strftime("%Y/%m/%d")
    date_visite_ar = f"{day_name_ar} {date_ar}"

    # Contexte pour le template HTML
    context = {
        'visite': visite,
        'enseignant': visite.enseignant_visite,
        'accompagnateurs': [
            {
                'nom': visite.nom_premier_accompagnateur,
                'som': visite.som_premier_accompagnateur,
                'etab': visite.etab_premier_accompagnateur,
            },
            {
                'nom': visite.nom_deuxieme_accompagnateur,
                'som': visite.som_deuxieme_accompagnateur,
                'etab': visite.etab_deuxieme_accompagnateur,
            },
        ],
        'date_visite_ar': date_visite_ar,  # Date au format arabe
    }

    # Génération du contenu HTML
    html_string = render_to_string('convocation.html', context)

    # Utilisation de base_url pour charger les fichiers statiques
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))
    pdf = html.write_pdf()

    # Retourne le PDF généré
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="convocation_{visite.id}.pdf"'
    return response

def statistiques(request):
    visites_par_mois = (
        Visite.objects.filter(status="Programmée")
        .annotate(month=ExtractMonth("date_visite"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("month")
    )

    visites_par_inspecteur = (
        Visite.objects.filter(status="Programmée")
        .values("nom_inspecteur")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    visites_par_specialite = (
        Visite.objects.filter(status="Programmée")
        .values("enseignant_visite__specialite_enseignant")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    # Convertir les mois en noms de mois
    labels_mois = [
        month_name[data["month"]] if data["month"] else "Inconnu"
        for data in visites_par_mois
    ]
    data_mois = [data["total"] for data in visites_par_mois]

    labels_inspecteur = [data["nom_inspecteur"] for data in visites_par_inspecteur]
    data_inspecteur = [data["total"] for data in visites_par_inspecteur]

    labels_specialite = [
        data["enseignant_visite__specialite_enseignant"]
        for data in visites_par_specialite
    ]
    data_specialite = [data["total"] for data in visites_par_specialite]

    context = {
        "labels_mois": labels_mois,
        "data_mois": data_mois,
        "labels_inspecteur": labels_inspecteur,
        "data_inspecteur": data_inspecteur,
        "labels_specialite": labels_specialite,
        "data_specialite": data_specialite,
    }
    return render(request, "statistiques.html", context)


