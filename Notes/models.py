from django.db import models

class Semestres(models.Model):
    IdSemestre = models.AutoField(primary_key=True, verbose_name=("idSemestre"))
    Numero = models.SmallIntegerField(blank=False, verbose_name=("Numero"))
    
    class Meta:
        verbose_name = ("Semestres")
        verbose_name_plural = ("Semestres")
        db_table = ("Semestres")
        
    def __str__(self):
        return "Semestre" + str(self.Numero)
    
class Niveau(models.Model):
    IdNiveau = models.AutoField(primary_key=True, blank=False)
    Niv = models.CharField(max_length=2)
    
    class Meta:
        verbose_name = ("Niveau")
        verbose_name_plural = ("Niveaux")
        db_table = ("Niveaux")
        
    def __str__(self) -> str:
        return str(self.Niv)
    
class UE(models.Model):
    Code_ue = models.CharField(max_length=50, primary_key=True)
    Libelle = models.CharField(max_length=255)
    Credit = models.IntegerField()
    
    STATUT_CHOICES = [
        ('optionnelle', 'Optionnelle'),
        ('fondamentale', 'Fondamentale'),
    ]
    
    Type = models.CharField(max_length=20,choices=STATUT_CHOICES,default='optionnelle')
    idniv = models.ForeignKey(Niveau, verbose_name=("idniv"), on_delete=models.CASCADE)
    idsem = models.ForeignKey(Semestres, verbose_name=("idsem"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("UE")
        verbose_name_plural = ("UE")
        db_table = ("UE")
    
    def __str__(self) -> str:
        return self.Code_ue
    
class Etudiant(models.Model):
    Matricule = models.CharField(max_length=50, primary_key=True)
    Nom = models.CharField(max_length=50)
    
    CHOICES_SEX = [
        ('femme', 'Femme'),
        ('homme', 'Homme')
    ]
    
    Genre = models.CharField(max_length=8, choices=CHOICES_SEX)
    DateNaiss = models.DateField(verbose_name=("Date de Naissance"), auto_now=False, auto_now_add=False)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Profil = models.ImageField(upload_to='profil/', default='profil/default_profil.jpg')
    Niveau_etu = models.ForeignKey(Niveau, verbose_name=("Niveau_etu"), on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Etudiant")
        verbose_name_plural = ("Etudiants")
        db_table = ("Etudiants")
    
    def __str__(self) -> str:
        return self.Nom
    
class Enseignant(models.Model):
    IdEnseignant = models.AutoField(primary_key=True)
    Nom = models.CharField(max_length=50)
    DateNaiss = models.DateField(auto_now=False)
    Genre = models.CharField(max_length=8)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=50)
    Numtel = models.IntegerField()
    Profil = models.ImageField(upload_to='profil/', default='profil/default_profil.jpg')
    
    class Meta:
        verbose_name = ("Enseignant")
        verbose_name_plural = ("Enseignants")
        db_table = ("Enseignants")
    
    def __str__(self) -> str:
        return self.Nom
    
class Evaluation(models.Model):
    IdEvaluation = models.AutoField(primary_key=True, verbose_name=("IdEvaluation"))
    STATUT_CHOICE = [
        ('cc', 'CC'),
        ('tp', 'TP'),
        ('sn', 'SN')
    ]
    
    Type = models.CharField(max_length=5, choices=STATUT_CHOICE, default='cc')
    Note = models.FloatField()
    Etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    Code_ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Evaluation")
        verbose_name_plural = ("Evaluations")
        db_table = ("Evaluations")
    
    def __str__(self) -> str:
        return self.Type
    
class EC(models.Model):
    Code_ec = models.CharField(max_length=50, primary_key=True, blank=False)
    Libelle = models.CharField(max_length=250)
    Code_ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("EC")
        verbose_name_plural = ("EC")
        db_table = ("EC")
    
    def __str__(self) -> str:
        return self.Code_ec
        
class Choisir(models.Model):
    Code_ue = models.ForeignKey(UE, on_delete=models.CASCADE)
    Etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Choisir")
        verbose_name_plural = ("Choisir")
        unique_together = ('Code_ue', 'Etudiant')
        db_table = ("Choisir")
        
    def __str__(self) -> str:
        return self.Code_ue.Code_ue
    
class Choisir_EC(models.Model):
    Enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    EC_Choisit = models.ForeignKey(EC, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = ("Choisir_EC")
        verbose_name_plural = ("Choisir_EC")
        unique_together = ('Enseignant', 'EC_Choisit')
        db_table = ("Choisir_EC")
        
    def __str__(self):
        return self.Enseignant.Nom
    
class Message(models.Model):
    Idmessage= models.AutoField(primary_key=True, verbose_name=("Idmessage"))
    Emeteur = models.EmailField(max_length=254)
    Recepteur = models.EmailField(max_length=254)
    Text = models.TextField()
    SendAt = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = ("Message")
        verbose_name_plural = ("Message")
        db_table = (" Message")
        
    def __str__(self):
        return self.Emeteur
