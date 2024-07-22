from django.shortcuts import render
from .models import Membres

# Create your views here.
# Cryptage MDP
import hashlib, os
from datetime import datetime

def uploadFile(request,em):
    if "myfile" in request.FILES:
        fichier = request.FILES["myfile"]
        dateTime = datetime.now()

        extension = os.path.splitext(fichier.name)
        newname = f'{em}{extension[1]}'

        emplacement = os.path.join("static/img/img_user/",newname)
        with open(emplacement, 'wb') as destination: #w/b : w=normal , b=binaire
            for chunk in fichier.chunks():
                destination.write(chunk)
    return newname

def cryptage_text(x):
    hachage = hashlib.sha384()
    hachage.update(x.encode("utf-8"))
    return hachage.hexdigest()

def pageinscription(request):
    return render(request,"inscription.html")

def insertionMembre(request):
    if request.method == 'POST':
        pseudo = request.POST.get("pseudo")
        mail = request.POST.get("email")
        pwds = request.POST.get("pwd")
        pwds_conf = request.POST.get("pwdConf")
        photo = request.POST.get("myfile")

        validation = True

        if pseudo != "" and mail != "" and pwds != "" and pwds_conf != "" and photo != "":
            emailExist = Membres.objects.filter(email=mail)
            nbEmail = len(emailExist)
            if nbEmail == 0:
                if pwds == pwds_conf:
                    insertion = Membres(
                        Pseudo = pseudo,
                        email = mail,
                        pwd = cryptage_text(pwds),
                        photo = f'static/img/img_user/{uploadFile(request,mail)}'
                    )
                    insertion.save()
                    message = "Vous êtes inscris avec succées !"
                    return render(request, "connexion.html", {"sms":message})
                else:
                    error = "Mot de passe non identique"
                    return render(request, "inscription.html", {"diso":error})
            else:
                error = "Email existe déja"
                return render(request, "inscription.html", {"diso":error})
        else:
            error = "Tous les champs sont obligatoire !"
            return render(request, "inscription.html", {"diso":error})
        
    return render(request, "inscription.html")
    
def connexion(request):
    if request.method == 'POST':
        mail = str(request.POST.get("email"))
        pwds = request.POST.get("pwd")

    try:
        emailExist = Membres.objects.get(email = mail)
    except Membres.DoesNotExist:
        error = "Vous n'êtes pas inscrit !"
        return render(request, 'connexion.html', {"sms":error})
    
    validation = True
    if mail != "" and pwds != "":
        if cryptage_text(pwds) == emailExist.pwd:
            validation = True
        else:
            validation = False
            error = "Mot de passe incorrect !"
            return render(request, "connexion.html", {"sms":error})
    else:
        error = "Tous les champs sont obligatoires !"
        return render(request, "connexion.html", {"sms":error})

    if validation:
        email_exist_dict = {
            "id": emailExist.id,
            "pseudo":emailExist.Pseudo,
            "email":emailExist.email,
            "photo":str(emailExist.photo),
            "pwd":emailExist.pwd,
        }

    request.session["client"] = email_exist_dict
    data = email_exist_dict
    return render(request, "membre.html", {"data":data})

def pageconnexion(request):
    return render(request, "connexion.html")

def deconnexion(request):
    request.session.clear()
    return render(request, "connexion.html")

def membre(request):
    data = request.session["client"]
    if len(data) != 0:
        return render(request, "membre.html", {"data":data})
    else:
        return render(request, "connexion.html")

        