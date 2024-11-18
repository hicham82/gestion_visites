from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView  # Import de LogoutView
from django.views.generic import RedirectView
from .views import obtenir_nom_enseignant
from django.http import HttpResponseRedirect

urlpatterns = [
    path('creer-visite/', views.creer_visite, name='creer_visite'),
    path('confirmation-visite/<int:visite_id>/', views.confirmation_visite, name='confirmation_visite'),
    path('liste-visites/', views.liste_visites, name='liste_visites'),  # URL pour la liste des visites
    path('modifier-visite/<int:id>/', views.modifier_visite, name='modifier_visite'),  # URL pour modifier une visite
    path('supprimer-visite/<int:id>/', views.supprimer_visite, name='supprimer_visite'),  # URL pour supprimer une visite
    path('telecharger-visites-excel/', views.telecharger_visites_excel, name='telecharger_visites_excel'),
    path('details-visite/<int:visite_id>/', views.afficher_details_visite, name='afficher_details_visite'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('obtenir-nom-enseignant/', obtenir_nom_enseignant, name='obtenir_nom_enseignant'),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),  # Redirige la racine vers la vue login
    path('contact/', lambda request: HttpResponseRedirect('/login/')),  # Redirige vers /login/

]
