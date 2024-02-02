from django.contrib import admin
from Notes.models import Semestres, Niveau, UE, Etudiant, Enseignant, Evaluation, EC, Choisir, Choisir_EC,Message

class AdminSemestre(admin.ModelAdmin):
    list_display = ('IdSemestre', 'Numero')
admin.site.register(Semestres, AdminSemestre)

class AdminNiveau(admin.ModelAdmin):
    list_display = ('IdNiveau', 'Niv')
admin.site.register(Niveau, AdminNiveau)

class AdminUE(admin.ModelAdmin):
    list_display = ('Code_ue', 'Libelle', 'Credit', 'Type', 'idniv', 'idsem')
admin.site.register(UE, AdminUE)

class AdminEtudiant(admin.ModelAdmin):
    list_display = ('Matricule', 'Nom', 'Genre', 'DateNaiss', 'Email', 'Password', 'Profil', 'Niveau_etu')
admin.site.register(Etudiant, AdminEtudiant)

class AdminEnseignant(admin.ModelAdmin):
    list_display = ('IdEnseignant', 'Nom', 'DateNaiss', 'Genre', 'Email', 'Password', 'Numtel', 'Profil')
admin.site.register(Enseignant, AdminEnseignant)

class AdminEvaluation(admin.ModelAdmin):
    list_display = ('IdEvaluation', 'Type', 'Note', 'Etudiant', 'Code_ue')
admin.site.register(Evaluation, AdminEvaluation)

class AdminEC(admin.ModelAdmin):
    list_display = ('Code_ec', 'Libelle', 'Code_ue')
admin.site.register(EC, AdminEC)

class AdminChoisir(admin.ModelAdmin):
    list_display = ('Code_ue', 'Etudiant')
admin.site.register(Choisir, AdminChoisir)

class AdminChoisir_EC(admin.ModelAdmin):
    list_display = ('Enseignant', 'EC_Choisit')
admin.site.register(Choisir_EC, AdminChoisir_EC)
class AdminMessage(admin.ModelAdmin):
    list_display = ('Idmessage','SendAt','Emeteur', 'Recepteur','Text')
admin.site.register(Message, AdminMessage)