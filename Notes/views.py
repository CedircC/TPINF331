from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.core.files.storage import default_storage
from Notes.models import *
import plotly.graph_objects as go
import plotly.io as pio
import pdfkit
from django.conf import settings
import os

def Acceuil(request):
    return render(request, 'index.html')

def choose_account(request):
    return render(request, 'choose_account.html')

def register_student(request):
    liste_niveau = Niveau.objects.all()
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        nom = request.POST.get('nom')
        genre = request.POST.get('genre')
        date = request.POST.get('date')
        email = request.POST.get('email')
        password = request.POST.get('password')
        niveau = request.POST.get('niveau')
        
        model_niv = Niveau.objects.get(Niv = niveau)
          
        new_student = Etudiant.objects.create(Matricule = matricule, Nom = nom, Genre = genre, DateNaiss = date, Email = email, Password = password, Niveau_etu = model_niv)
        new_student.save()
        
        request.session['matricule'] = matricule
        return redirect('choisir_ue')
    
    return render(request, 'student_register.html', {'liste_niveau': liste_niveau})

def choisir_ue(request):
    etudiant = Etudiant.objects.get(Matricule = request.session.get('matricule',None))
    ue = UE.objects.filter(idniv = etudiant.Niveau_etu)
    contexte = {
        'etudiant': etudiant,
        'ListeUE': ue,
    }
    
    if request.method == 'POST':
        multi = request.POST.getlist('checkue')
        
        for elt in multi:
            ue = UE.objects.get(Code_ue = elt)
            choix = Choisir.objects.create(Code_ue = ue, Etudiant = etudiant)
            choix.save()
            
        return redirect('mainstudent')  
    
    return render(request, 'choisir_ue.html', contexte)
    

def register_teacher(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        nom = request.POST.get('nom')
        genre = request.POST.get('genre')
        date = request.POST.get('date')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        new_teacher = Enseignant.objects.create(Nom = nom, DateNaiss = date, Genre = genre, Email = email, Password = password, Numtel = phone)
        new_teacher.save()
        
        request.session['Idenseignant'] = new_teacher.IdEnseignant
        return redirect('choisir_ec')
    
    return render(request, 'teacher_register.html')

def choisir_ec(request):
    enseignant = Enseignant.objects.get(IdEnseignant = request.session.get('Idenseignant'))
    ec = EC.objects.all()
    choixec = Choisir_EC.objects.all()
    listeec = []
    
    for elts in ec:
        trouve = 0
        for elt in choixec:
            if elt.EC_Choisit == elts:
                trouve = 1
        
        if trouve == 0:
            listeec.append(elts)    

    print(listeec)
    
    contexte = {
        'enseignant': enseignant,
        'listeEc': listeec, 
    }
    
    if request.method == 'POST':
        multi = request.POST.getlist('checkec')
        print(multi)
        
        for elt in multi:
            ec = EC.objects.get(Code_ec = elt)
            choix = Choisir_EC.objects.create(Enseignant = enseignant, EC_Choisit = ec)
            choix.save()
        
        request.session['Idenseignant'] = enseignant.IdEnseignant
        return redirect('click_ue')  
    
    
    return render(request, 'choisir_ec.html', contexte)

def login_student(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')
        
        try:
            etudiant = Etudiant.objects.get(Matricule = matricule, Password = password)
            request.session['matricule'] = matricule
            return redirect('mainstudent')
        except Etudiant.DoesNotExist:
            print('Info incorrect')

    return render(request, 'pages-login.html')

def logout_view(request):
    logout(request)
    
    return redirect('Acceuil')

def login_teacher(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            enseignant = Enseignant.objects.get(Email = email, Password = password)
            request.session['Idenseignant'] = enseignant.IdEnseignant
            return redirect('click_ue')
        except Enseignant.DoesNotExist:
            print('Infos incorrect')
    
    return render(request, 'teacher_login.html')

def mainteacher(request, code):
    t =Choisir.objects.filter(Code_ue=code)
    ue = UE.objects.get(Code_ue = code)
    
    etudiant=[]
    for el in t:
        etudiant.append(el.Etudiant)
    liste_note = ['Not available' for i in range(3)]
    notes={}     
    liste_note = ['Not available' for i in range(3)]  
    for el in etudiant:
        if request.method == 'POST':
            cc = request.POST.get(el.Matricule+"cc")
            if cc!='Not available':   
                no = Evaluation.objects.create(Type="cc", Note=cc,Code_ue =ue, Etudiant = el)
                no.save()
                
            tp = request.POST.get(el.Matricule+"tp")
            if tp!='Not available':
                no = Evaluation.objects.create(Type="tp", Note=tp,Code_ue = ue, Etudiant = el)
                no.save()
                
            sn = request.POST.get(el.Matricule+"sn")

            if sn!='Not available' :
                no = Evaluation.objects.create(Type="sn", Note=sn,Code_ue = ue, Etudiant = el)
                no.save()

    for choix in etudiant:
        ol= Evaluation.objects.filter(Etudiant = choix, Code_ue = ue)
        notes[choix]= ['Not available' for i in range(3)]
        for v in ol:
            if(v.Type=='cc'):
                notes[choix][0]=v.Note
            if(v.Type=="tp"):
                notes[choix][1]=v.Note
            if(v.Type=="sn"):
                notes[choix][2]=v.Note                    
        
          
            
    ccc=[]
    tpp=[]
    snn=[]
    for t in notes.values():
        if(t[0])!="Not available":
            ccc.append(t[0])
        if(t[1])!="Not available":    
            tpp.append(t[1])
        if(t[2])!="Not available":    
            snn.append(t[2])
    cc1=[]     
    tp1=[]
    sn1=[]
    gra=[0,0,0,0]
    a=[]
    for cle,va in notes.items():
        a.append(cle.Nom)
        if(va[0])!="Not available":
            cc1.append(va[0])
            gra[0]=gra[0]+1
        else:
            cc1.append(0)
                
        if(va[1])!="Not available":    
            tp1.append(va[1])
            gra[1]=gra[1]+1
        else:
            tp1.append(0)
        if(va[2])!="Not available":    
            sn1.append(va[2])
            gra[2]=gra[2]+1
        else:
            sn1.append(0)    
    df=a
    gra[3]=gra[0]+gra[1]+gra[2]
    for i in range(len(gra)-1):
        if len(a) == 0:
            gra[i] = (gra[i] / 1) * 100
        else:
            gra[i] = (gra[i] / len(a)) * 100
    if len(a) == 0:        
        gra[3] = (gra[3]) / (3 * 1) * 100  
    else:
        gra[3] = (gra[3]) / (3 * len(a)) * 100
    
      
        
        
    
       
               
            

        
  
        
    data = [
    go.Box(
        y=ccc,  # Exemple de données pour la boîte à moustaches
        name='cc' , # Nom du groupe
        orientation='v'
    ),
    go.Box(
        y=tpp,  # Exemple de données pour la boîte à moustaches
        name='tp',  # Nom du groupe
        orientation='v'
    ),
    go.Box(
        y=snn,  # Exemple de données pour la boîte à moustaches
        name='sn' ,
        orientation='v'# Nom du groupe
    ),
    # Ajoutez plus de boîtes à moustaches pour chaque groupe de données
         ]

    figure = go.Figure(data=data)
    figure.update_traces(
    marker_color='lightblue',  # Couleur des boîtes à moustaches
    line_color='blue',  # Couleur des lignes de contour des boîtes à moustaches
    boxmean=True,  # Afficher la ligne représentant la valeur moyenne
    notched=True,  # Afficher les encoches sur les boîtes à moustaches
    boxpoints='all',  # Afficher tous les points de données individuels
    jitter=0.3,  # Espacement des points de données individuels
    whiskerwidth=0.2,  # Largeur des lignes des moustaches
    showlegend=False  # Masquer la légende
)
    figure.update_layout(
    plot_bgcolor='white',  # Couleur de fond du graphique
    paper_bgcolor='white',  # Couleur de fond du papier
    font_color='black',  # Couleur du texte
    xaxis=dict(
        showgrid=False,  # Masquer les lignes de griy'],,
        zeroline=False  # Masquer la ligne zéro sur l'axe x
    ),
    yaxis=dict(
        showgrid=True,  # Afficher les lignes de grille sur l'axe y
        gridcolor='lightgray'  # Couleur des lignes de grille sur l'axe y
    )
)
    graph_html1 = figure.to_html(full_html=False)  
    
    cc_scores =cc1
    sn_scores =sn1
    tp_scores =tp1

    labels = [f" {et}(CC: {cc}, SN: {sn}, TP: {tp})" for et,cc, sn, tp in zip(a,cc_scores, sn_scores, tp_scores,)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=cc_scores, y=sn_scores, mode='markers', name='CC',
                            hovertext=labels, hoverinfo='text',
                            marker=dict(color='rgb(31, 119, 180)', size=8, line=dict(width=1, color='rgb(0, 0, 0)'))))
    fig.add_trace(go.Scatter(x=cc_scores, y=tp_scores, mode='markers', name='TP',
                            hovertext=labels, hoverinfo='text',
                            marker=dict(color='rgb(255, 127, 14)', size=8, line=dict(width=1, color='rgb(0, 0, 0)'))))

    fig.update_layout(
        title='Student Performance',
        xaxis=dict(title='CC Scores', zeroline=False),
        yaxis=dict(title='TP/SN Scores', zeroline=False),
        plot_bgcolor='rgb(245, 245, 245)',
        hovermode='closest',
        showlegend=True,
        legend=dict(x=0.1, y=1.1, orientation='h')
    )
    graph_html2= pio.to_html(fig, full_html=False)
    
                   
    categories = df

    # Données pour chaque série
    cc_data = cc1
    sn_data = tp1
    tp_data = sn1

    # Création du graphe à barres    
    fig = go.Figure()

    # Ajout des traces (séries)
    fig.add_trace(go.Bar(
        name="CC",
        x=categories,
        y=cc_data,
        marker_color="#2196F3"
    ))

    fig.add_trace(go.Bar(
        name="TP",
        x=categories,
        y=sn_data,
        marker_color="#FF9800"
    ))

    fig.add_trace(go.Bar(
        name="SN",
        x=categories,
        y=tp_data,
        marker_color="#4CAF50"
    ))

    # Personnalisation du titre et des étiquettes des axes
    fig.update_layout(
        title="STUDENT Bar Chart",
        xaxis=dict(title="Catégories", showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(title="NOTES", showgrid=False, tickfont=dict(size=14)),
        font=dict(family="Arial, sans-serif", color="#333"),
        plot_bgcolor="#fff",
        barmode="group",
        bargap=0.2,
        bargroupgap=0.1,
        legend=dict(font=dict(size=14), traceorder="normal")
    )
    
    
    # Affichage du graphe
    graph_html3= pio.to_html(fig, full_html=False)

    
    fig = go.Figure(data=go.Pie(values=gra, labels=['CC etudiant note', 'TP etudiant note', 'SN etudiant note', 'TOTAL etudiant note'], hole=0.5))
    
    # Convertir le graphique en HTML
    graph_html4 = fig.to_html(full_html=False)

    project_directory = settings.BASE_DIR
    pdf_path = os.path.join(project_directory, 'rapport'+code+'.pdf')

    table_html = ' <table id="letableau" class="table datatable"  ><thead><tr><th><b>N</b>ame</th><th>Matricule</th><th>CC</th><th>TP</th><th>SN</th><th></th></tr></thead><tbody>'
    for element,n in notes.items():
        table_html +=f'<tr><td>{element.Nom}</td><td><input class="subnotemat" type="text" value="{element.Matricule}" readonly name="matricule"></td><td><input class="subnote" type="text" value="{n[0]}" name="{{element.Matricule}}cc"></td><td><input class="subnote" type="text" value="{n[1]}" name="{{element.Matricule}}tp"></td><td><input class="subnote" type="text" value="{n[2]}" name="{{element.Matricule}}sn"></td><td></div></td></tr>'
                                        
    table_html +='</tbody></table>'
    table_styles = '''
<style>
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
        color: #333333;
    }

    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #dddddd;
    }

    th {
        background-color: #007bff;
        color: #ffffff;
        font-weight: bold;
        text-transform: uppercase;
    }

    tr:hover {
        background-color: #f2f2f2;
        transition: background-color 0.3s ease;
    }

    .highlight-row {
        background-color: #eaf6ff;
        transition: background-color 0.3s ease;
    }

    .button {
        display: inline-block;
        padding: 10px 20px;
        background-color: #007bff;
        color: #ffffff;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s ease;
        text-decoration: none;
    }

    .button:hover {
        background-color: #0056b3;
    }

    .button-primary {
        background-color: #ffffff;
        color: #007bff;
        border: 2px solid #007bff;
    }

    .button-primary:hover {
        background-color: #007bff;
        color: #ffffff;
    }
</style>
'''

    # Concaténer les styles CSS avec le tableau HTML
    table_html = table_styles + table_html




    graphes_html = ["rapport statistique et graphique de"+code,table_html,graph_html1,graph_html2,graph_html3,graph_html4]  # Ajoutez autant de graphes que nécessaire
    html_concatene = ''
# Convertir chaque graphe HTML en PDF et les ajouter au fichier de sortie
    for index, graphe_html in enumerate(graphes_html):
        html_concatene += graphe_html

#     config = pdfkit.configuration(wkhtmltopdf='/home/cedirc/Bureau/.venv/lib/python3.10/site-packages/wkhtmltopdf')
#     pdfkit.from_url('http://example.com', 'out.pdf', configuration=config)        

# # Générer le fichier PDF à partir du contenu HTML concaténé
#     pdfkit.from_string(html_concatene, pdf_path, options={'page-size': 'A4'}) 
    ess=Enseignant.objects.get(IdEnseignant = request.session.get('Idenseignant'))
    if request.method == 'POST':
            message = request.POST.get("message")
            matricule= request.POST.get("checkue",None)
            if(message!=''):
                if matricule :
                    etudiant = Etudiant.objects.get(Matricule=matricule)
                    no = Message.objects.create(Emeteur=ess.Email,Recepteur=etudiant.Email,Text=message)
                    no.save()
    mess= Message.objects.filter(Recepteur=ess.Email)
    send= Message.objects.filter(Emeteur=ess.Email) 
    nm=len(mess)
    ns=len(send) 
    
    
    contexte = {
        'etudiant': etudiant,
        'enseignant': Enseignant.objects.get(IdEnseignant = request.session.get('Idenseignant')),
        'ue': ue,
        'notes':notes,
        'plot': graph_html1,
        'cc1':cc1,
        'gra':gra,
        'sn1':sn1,
        'tp1':tp1,
        'df':df,
        'nm':nm,
        'mess':reversed(mess),
        'send':reversed(send),
        'ns':ns,
        'nuage':graph_html2,
        'bar':graph_html3,
        
    }
    
    return render(request, 'mainteacher.html', contexte)

def mainstudent(request):
    matricule=request.session.get('matricule',None)
    etudiant = Etudiant.objects.get(Matricule=matricule)
    choisir = Choisir.objects.filter(Etudiant=etudiant)
    li={}
    j=1
    for choix in choisir:
        li[j]=choix.Code_ue
        j+=1
        

        
    
    notes = {}
    liste_note = ['Not available' for i in range(3)]
    # 0 = cc
    # 1 = tp
    # 2 = sn
    
    for choix in choisir:
        ol = Evaluation.objects.filter(Etudiant = etudiant, Code_ue = choix.Code_ue)
        notes[choix]= ['Not available' for i in range(3)]
        for v in ol:
            if(v.Type=='cc'):
                notes[choix][0]=v.Note
            if(v.Type=="tp"):
                notes[choix][1]=v.Note
            if(v.Type=="sn"):
                notes[choix][2]=v.Note
    k=[]  
    
    
        
   
                    
    total=0           
    for el in notes.values():
        for elt in el:
            if elt != 'Not available':
                total += elt
        if total == 0:
            total = 'Not available'
        el.append(total)
        total = 0 
 
                 
  
                    
    for el in notes.values():
            for n in range(len(el)):
                if(isinstance(el[n],int)==True):
                    el[n]="Not available"                     
    k=[]
    for i in notes.values():
            k.append(i)             
    for es in k:
            a=len(es)
            for els in range(a):
                if(es[els]=="Not available"):
                    es[els]=0         
    for i in notes.values():
            for e in range(len(i)):
                if(isinstance(i[e],int)==True):
                    i[e]="Not available" 
    ues=[]
    to=[]                 
    for i,z in notes.items():   
        ues.append(i.Code_ue.Code_ue)
        to.append(z[3])    


        
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="SN",
        x=ues,
        y=to,
        marker_color="#4CAF50"
    ))

    # Personnalisation du titre et des étiquettes des axes
    fig.update_layout(
        title="STUDENT Bar Chart",
        xaxis=dict(title="Catégories", showgrid=False, tickfont=dict(size=14)),
        yaxis=dict(title="NOTES", showgrid=False, tickfont=dict(size=14)),
        font=dict(family="Arial, sans-serif", color="#333"),
        plot_bgcolor="#fff",
        barmode="group",
        bargap=0.2,
        bargroupgap=0.1,
        legend=dict(font=dict(size=14), traceorder="normal")
    )
    
    
    graph_html3= pio.to_html(fig, full_html=False)          
    h=0   
    if request.method == 'POST':
        message = request.POST.get("message")
        uecheck= request.POST.get("checkue",None)  
        ec=EC.objects.filter(Code_ue =uecheck)
        if(uecheck):
            for j in range(len(ues)):
                if uecheck==ues[j]:
                    h=j
            for elmr in ec:
                    listc=(Choisir_EC.objects.filter(EC_Choisit=elmr))
                    if len(listc)!=0:
                        if message!='':
                            no = Message.objects.create(Emeteur=etudiant.Email,Recepteur=listc[0].Enseignant.Email,Text=message)
                            no.save()  
    mess= Message.objects.filter(Recepteur=etudiant.Email)
    send= Message.objects.filter(Emeteur=etudiant.Email) 
    nm=len(mess)
    ns=len(send)     

                               
    contexte = {
        'etudiant': etudiant,
        'choisir': choisir,
        'notes': notes,
        'li':li,
        'k':k,
        'ues':ues,
        'h':int(h),
        'mess':reversed(mess),
        'send':reversed(send),
        'nm':nm,
        'ns':ns,
        'bar':graph_html3
        
    }
    
    return render(request, 'studentnote.html',contexte)

def click_ue(request):
    enseignant = Enseignant.objects.get(IdEnseignant = request.session.get('Idenseignant'))
    listechoix = Choisir_EC.objects.filter(Enseignant = enseignant)
    listeue = []
    
    # for elt in listechoix:
    #     ue = UE.objects.get(Code_ue = elt.EC_Choisit.Code_ue.Code_ue)
    #     listeue.append(ue)
    
    for elt in listechoix:
        listeue.append(elt.EC_Choisit.Code_ue)
    # print(listechoix)
    nl=[]
    for item in  listeue:
        if item not in  nl:
            nl.append(item)
        
    contexte = {
        'enseignant': enseignant,
        'listeue': nl,
    }
    
    return render(request, 'click_ue.html', contexte)

def student_user_profil(request):
    matricule = request.session.get('matricule')
    etudiant = Etudiant.objects.get(Matricule = matricule)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        profil = request.FILES.get('profil')

        if profil:    
            file_path = f"profil/{profil.name}"
            default_storage.save(file_path, profil)

            etudiant.Profil = file_path
            etudiant.save()

        etudiant.Nom = name
        etudiant.Email = email
        etudiant.save()
        
        return redirect('student_user_profil')

    contexte = {
        'etudiant': etudiant,
    }

    return render(request, 'student_user_profil.html', contexte)

def teacher_user_profil(request):
    enseignant = Enseignant.objects.get(IdEnseignant = request.session.get('Idenseignant'))

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        profil = request.FILES.get('profil')

        if profil:    
            file_path = f"profil/{profil.name}"
            default_storage.save(file_path, profil)

            enseignant.Profil = file_path
            enseignant.save()

        enseignant.Nom = name
        enseignant.Email = email
        enseignant.Numtel = phone
        enseignant.save()

    contexte = {
        'enseignant': enseignant,
    }

    return render(request, 'teacher_user_profil.html', contexte)