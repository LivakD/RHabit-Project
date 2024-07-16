from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import os, json
from datetime import date, datetime, timezone
from django.core.files.storage import FileSystemStorage


def userData(request):
    Task = request.GET.get("Task", "Task=")
    Name = request.GET.get("Name", "Name=")

    with open("/var/www/django-project/Rhabit/data/users/user.json", "r") as dateiLesen:
        Name = json.loads(dateiLesen.read())["name"]

    varContainer = {
        "aktueller_task": Task,
        "DeinUser": Name
    }
    return render(request, "Rhabit/Rhabit_Homepage.html", varContainer)

def searchData(request):
    Name = request.GET.get("Name", "Name=")
    Userpic = request.GET.get("PB", "PB=")

    namen = ["Louis@123", "D3nniS", "KaiDerHai", "Ar00j24"]

    bilder = {
        "Vector": "https://www.shutterstock.com/shutterstock/photos/2128959116/display_1500/stock-vector-abstract-waving-particle-technology-background-design-abstract-wave-moving-dots-flow-particles-hi-2128959116.jpg",
        "Wolken": "https://img.freepik.com/vektoren-kostenlos/handgemalter-aquarellpastellhimmelhintergrund_23-2148902771.jpg",
        "Blätter": "https://img.freepik.com/free-vector/copy-space-bokeh-spring-lights-background_52683-55649.jpg",
        "Auto": "https://www.autoscout24.de/cms-content-assets/6qT8nlNz14DOONScsa0U4x-b5f51e28a5baea490c35725ceddb3700-dodge-challenger-front-1100.jpeg"
    }

    bild = bilder["Vector"]

    alleUser = [
        {"user": "Louis@123", "bild": bilder["Vector"]},
        {"user": "D3nniS", "bild": bilder["Auto"]},
        {"user": "KaiDerHai", "bild": bilder["Blätter"]},
        {"user": "Ar00j24", "bild": bilder["Wolken"]}
    ]

    vars = {
        "Username": Name,
        "namensliste": namen,
        "bild": bild,
        "userliste": alleUser
    }

    return render(request, "Rhabit/Rhabit_Searchpage.html", vars)

def user(request):
    uid = request.GET.get("uid", "")
    pwd = request.GET.get("pwd", "")
    bio = request.GET.get("bio", "")
    email = request.GET.get("email", "")
    habit = request.GET.get("habit", "")
    habitStep = request.GET.get("habitStep", "")
    setHabit = request.GET.get("setHabit", "")
    searchName = request.GET.get("searchName", "")
    wantToFollow = request.GET.get("wantToFollow", "")
    unFollow = request.GET.get("unFollow", "")

    userPath = f"/var/www/django-project/Rhabit/data/users/{uid}.json"
    habitPath = f"/var/www/django-project/Rhabit/data/readyHabits/{habit[:-1]}.json"
    imgPath = ""
    userData = ""
    habitData = ""

    changeName = request.GET.get("changeName", False)
    changePwd = request.GET.get("changePwd", False)
    changeBio = request.GET.get("changeBio", False)
    changeMail = request.GET.get("changeMail", False)
    deletePic = request.GET.get("deletePic", False)
    changePic = request.POST.get("changePic", False)
    postGoal = request.POST.get("postGoal", False)
    addGate = request.GET.get("addGate",False)
    today = date.today()
    postDay = today.strftime("%d.%m.%Y")
    timeNow = datetime.now(timezone.utc)
    postTime = timeNow.strftime("%H:%M Uhr")




    if not os.path.isfile(userPath):
        #return HttpResponse(f"Der User mit der ID {uid} existiert nicht. Bitte registriere dich :-)")
        today = date.today()
        creationDate = today.strftime("%d.%m.%Y")
        
        emptTmpl = {
            "name": "Rhabit-User",
            "email": email,
            "pwd": pwd,
            "creation": creationDate,
            "bio": bio,
            "picture": "0",
            "followers": [
            ],
            "following": [
            ],
            "habits": [
            ],
            "currentHabit": {
                "color": {
                    "backgrC": "",
                    "rowC": "",
                    "blockC": ""
                    },
                "name": "",
                "days": "",
                "dayPosts": [
                ],
                "finalPost": ""
            },
            "finalPostAction": "0"
        }

        with open(userPath, "w", encoding="utf-8") as file:
            tmplDump = json.dumps(emptTmpl, indent = 2)
            file.write(tmplDump)

       # newPerm = 0o666
      #  os.system(f"sudo chmod {newPerm} {userPath}")



    with open(userPath, "r", encoding="utf-8") as file:
        userData = file.read()

    userData = json.loads(userData)
    

    if userData["pwd"] == pwd:
        if userData["picture"] != "0":
            imgPath = userData["picture"]
        else:
            imgPath = "http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/RHabit/imgs/users/0.png"

        followerList = []
        followingList = []

        for entry in userData["followers"]:
            entryPath = f"/var/www/django-project/Rhabit/data/users/{entry}.json"
            if not os.path.isfile(entryPath):
                return HttpResponse(f"Der User mit der ID {entry} existiert nicht!")
            with open(entryPath, "r") as file:
                entryData = json.loads(file.read())
                followerList.append(entryData["name"])

        for entry in userData["following"]:
            entryPath = f"/var/www/django-project/Rhabit/data/users/{entry}.json"
            if not os.path.isfile(entryPath):
                return HttpResponse(f"Der User mit der ID {entry} existiert nicht!")
            with open(entryPath, "r") as file:
                entryData = json.loads(file.read())
                followingList.append(entryData["name"])        

        following = []
        cards = []

        with open(f"/var/www/django-project/Rhabit/data/users/{uid}.json", "r", encoding="utf-8") as file:
            following = json.load(file)["following"]

        for user in following:
            if os.path.isfile(f"/var/www/django-project/Rhabit/data/users/{user}.json"):
                with open(f"/var/www/django-project/Rhabit/data/users/{user}.json", "r", encoding="utf-8") as file:
                    fileData = json.load(file)
                    data = {
                        "uid": user,
                        "name": fileData["name"],
                        "picture": fileData["picture"],
                        "habitName": fileData["currentHabit"]["name"],
                        "days": fileData["currentHabit"]["days"],
                        "currentDays": len(fileData["currentHabit"]["dayPosts"]),
                        "dayPosts": fileData["currentHabit"]["dayPosts"],
                        "finalPost": fileData["currentHabit"]["finalPost"],
                        "postBackC": fileData["currentHabit"]["color"]["backgrC"],
                        "postRowC": fileData["currentHabit"]["color"]["rowC"],
                        "postBlockC": fileData["currentHabit"]["color"]["blockC"],
                        "Foto": fileData["currentHabit"]["finalPost"],
                    }
                    cards.append(data)
            """
                    dates = []
                    times = []
                    with open(userPath, "r", encoding="utf-8") as file:
                        userData = json.load(file)
                        Pdays = userData["currentHabit"]["postDay"]
                        Ptimes = userData["currentHabit"]["postTime"]
                        for daysSet in Pdays:
                            dates.append(daysSet)

                        for timeSet in Ptimes:
                            times.append(timeSet)
            """


        
        SearchContainer = []
        allUser = os.listdir("/var/www/django-project/Rhabit/data/users/")
        userDataPath = "/var/www/django-project/Rhabit/data/users/"
        
        for user in allUser:
            filePath = os.path.join(userDataPath, user)
            with open(filePath, "r", encoding="utf-8") as file:
                fileUser = json.load(file)
                data= {
                    "filename": user,
                    "uid": uid,
                    "username": fileUser["name"],
                    "Profilbild": fileUser["picture"],
                    "folgend": fileUser["followers"],
                    "folgendZahl": len(fileUser["followers"]),
                    "gefolgt": fileUser["following"],
                    "gefolgtZahl": len(fileUser["following"]),
                    "erstellt": fileUser["creation"],
                    "email": fileUser["email"],
                    "habits": fileUser["habits"],
                    "habitZahl": len(fileUser["habits"]),
                    "currentHabit": fileUser["currentHabit"]["name"],
                    "currentdays": fileUser["currentHabit"]["days"],
                    "currentCdays": len(fileUser["currentHabit"]["dayPosts"]),
                    "currentDayPosts": fileUser["currentHabit"]["dayPosts"],
                    "finalPost": fileUser["currentHabit"]["finalPost"],
                    "backgrC": fileUser["currentHabit"]["color"]["backgrC"],
                    "rowC": fileUser["currentHabit"]["color"]["rowC"],
                    "blockC": fileUser["currentHabit"]["color"]["blockC"],
                    "bio": fileUser["bio"]
                }
                if user != f"{uid}.json":
                    SearchContainer.append(data)
                else:
                    pass

        if searchName:
            SearchContainer = []
            allUser = os.listdir("/var/www/django-project/Rhabit/data/users/")
            for user in allUser:
                with open(f"/var/www/django-project/Rhabit/data/users/{user}", "r", encoding="utf-8") as file:
                    fileUser = json.load(file)
                    if searchName in fileUser["name"]:
                        data= {
                            "filename": user,
                            "uid": uid,
                            "username": fileUser["name"],
                            "Profilbild": fileUser["picture"],
                            "folgend": fileUser["followers"],
                            "folgendZahl": len(fileUser["followers"]),
                            "gefolgt": fileUser["following"],
                            "gefolgtZahl": len(fileUser["following"]),
                            "erstellt": fileUser["creation"],
                            "email": fileUser["email"],
                            "habits": fileUser["habits"],
                            "habitZahl": len(fileUser["habits"]),
                            "currentHabit": fileUser["currentHabit"]["name"],
                            "currentdays": fileUser["currentHabit"]["days"],
                            "currentCdays": len(fileUser["currentHabit"]["dayPosts"]),
                            "currentDayPosts": fileUser["currentHabit"]["dayPosts"],
                            "finalPost": fileUser["currentHabit"]["finalPost"],
                            "backgrC": fileUser["currentHabit"]["color"]["backgrC"],
                            "rowC": fileUser["currentHabit"]["color"]["rowC"],
                            "blockC": fileUser["currentHabit"]["color"]["blockC"],
                            "bio": fileUser["bio"]
                        }
                        SearchContainer.append(data)
                    else:
                        pass

        if wantToFollow:
            userData["following"].append(os.path.splitext(wantToFollow)[0])
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))

            followPath = f"/var/www/django-project/Rhabit/data/users/{wantToFollow}"

            with open(followPath, "r", encoding="utf-8") as followFile:
                followData = json.load(followFile)

            followData["followers"].append(uid)

            with open(followPath, "w", encoding="utf-8") as followFile:
                followFile.write(json.dumps(followData, indent=2))
        
        elif unFollow:
            userData["following"].remove(os.path.splitext(unFollow)[0])
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))
            
            unFollowPath = f"/var/www/django-project/Rhabit/data/users/{unFollow}"

            with open(unFollowPath, "r", encoding="utf-8") as unFollowFile:
                unFollowData = json.load(unFollowFile)

            unFollowData["followers"].remove(uid)

            with open(unFollowPath, "w") as unFollowFile:
                unFollowFile.write(json.dumps(unFollowData, indent=2))


        if setHabit == "True":

            with open(habitPath, "r", encoding="utf-8") as file:
                habitData = json.load(file)

            userData["currentHabit"]["name"]= habitData[habitStep]["habitName"]
            userData["currentHabit"]["days"]= habitData[habitStep]["habitDauer"]

            c1 = habitData["colors"]["backgrC"]
            c2 = habitData["colors"]["rowC"]
            c3 = habitData["colors"]["blockC"]

            userData["currentHabit"]["color"]["backgrC"]= c1
            userData["currentHabit"]["color"]["rowC"]= c2
            userData["currentHabit"]["color"]["blockC"]= c3

            with open(userPath, "w", encoding="utf-8") as file:
                json.dump(userData, file, indent = 2)

        elif setHabit == "resetHabit":

            Goal = userData["currentHabit"]["name"]
            userData["habits"].append(Goal)

            userData["currentHabit"]["name"]= ""
            userData["currentHabit"]["days"]= ""
            userData["currentHabit"]["dayPosts"]= []
            userData["currentHabit"]["finalPost"]= ""
            userData["currentHabit"]["color"]["backgrC"]= ""
            userData["currentHabit"]["color"]["rowC"]= ""
            userData["currentHabit"]["color"]["blockC"]= ""

            with open(userPath, "w", encoding="utf-8") as file:
                json.dump(userData, file, indent = 2)


        if changeName:
            userData["name"] = changeName
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))
            #os.rename(userPath, f"/var/www/django-project/Rhabit/data/users/{changeName}.json")

        if changePwd:
            userData["pwd"] = changePwd
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))

        if changeBio:
            userData["bio"] = changeBio
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))


        Vergleichszahl = len(userData["currentHabit"]["dayPosts"]) + 1

        if str(Vergleichszahl) == userData["currentHabit"]["days"] and userData["finalPostAction"] == "0":                
            userData["finalPostAction"] = "1"
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))

        else:
            userData["finalPostAction"] = "0"
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))


        if addGate:
            if int(userData["currentHabit"]["days"]) >= len(userData["currentHabit"]["dayPosts"]):
                userData["currentHabit"]["dayPosts"].append(addGate)
                with open(userPath, "w") as file:
                    file.write(json.dumps(userData, indent=2))
        
        if str(len(userData["currentHabit"]["dayPosts"])) > userData["currentHabit"]["days"]:
            try:
                userData["currentHabit"]["dayPosts"].pop()[-1]
                with open(userPath, "w") as file:
                    file.write(json.dumps(userData, indent=2))
            except:
                pass
        else:
            pass
   
        if "postGoal" in request.FILES and request.method == "POST":
                myfile1 = request.FILES["postGoal"]
                fs1 = FileSystemStorage("/var/www/html/RHabit/GoalPosts")
                dataPath1 = "/var/www/html/RHabit/GoalPosts"

                Bilder1 = os.listdir(dataPath1)
                name1 = 0

                for pic1 in Bilder1:
                    numb1 = int(os.path.splitext(pic1)[0])
                    if numb1 > name1:
                        name1 = numb1

                myfile1.name = str(name1 + 1) + "." + myfile1.name.split(".")[-1]
                filename1 = fs1.save(myfile1.name, myfile1)


                #picType = os.path.splitext(myfile.name)[1]
                #myfile.name = f"img_{uid}{picType}"
                #filename = fs.save(myfile.name, myfile)

                imgPathPost1 = f"http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/RHabit/GoalPosts/{myfile1.name}"

                userData["currentHabit"]["finalPost"] = imgPathPost1
                with open(userPath, "w") as file:
                    file.write(json.dumps(userData, indent=2))

        
        if changeMail:
            userData["email"] = changeMail
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))

        if deletePic:
            userData["picture"] = deletePic
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent = 2))
        
        if "changePic" in request.FILES and request.method == "POST":
            
            myfile = request.FILES["changePic"]
            fs = FileSystemStorage("/var/www/html/RHabit/imgs/users")
            dataPath = "/var/www/html/RHabit/imgs/users"

            Bilder = os.listdir(dataPath)
            name = 0

            for pic in Bilder:
                numb = int(os.path.splitext(pic)[0])
                if numb > name:
                    name = numb

            myfile.name = str(name + 1) + "." + myfile.name.split(".")[-1]
            filename = fs.save(myfile.name, myfile)


            #picType = os.path.splitext(myfile.name)[1]
            #myfile.name = f"img_{uid}{picType}"
            #filename = fs.save(myfile.name, myfile)

            imgPath = f"http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/RHabit/imgs/users/{myfile.name}"

            userData["picture"] = imgPath
            with open(userPath, "w") as file:
                file.write(json.dumps(userData, indent=2))

        
        


        vars = {
            "Name": userData["name"],
            "Email": userData["email"],
            "Erstellungsdatum": userData["creation"],
            "Profilbild": imgPath,
            "Bio": userData["bio"],
            "AktuellerHabitName": userData["currentHabit"]["name"],
            "AktuellerHabitDays": userData["currentHabit"]["days"],
            "AktuellerHabitCDays": len(userData["currentHabit"]["dayPosts"]),
            "AktuellerHabitDayPosts": userData["currentHabit"]["dayPosts"],
            "AktuellerHabitFinalPost": userData["currentHabit"]["finalPost"],
            "Erfolgsliste": userData["habits"],
            "Erfolgszahl": len(userData["habits"]),
            "Followerliste": followerList,
            "Followerzahl": len(followerList),
            "Followingliste": followingList,
            "Followingzahl": len(followingList),
            "Passwort": userData["pwd"],
            "Passwort1": pwd,
            "FLWG": userData["following"],
            "FLWR": userData["followers"],
            "UID": uid,
            "FollowingCards": cards,
            "BackgrC": userData["currentHabit"]["color"]["backgrC"],
            "rowC": userData["currentHabit"]["color"]["rowC"],
            "blockC": userData["currentHabit"]["color"]["blockC"],
            "SearchContainer": SearchContainer,
            "Abschlussfoto": userData["currentHabit"]["finalPost"],
            "ifTrue": userData["finalPostAction"],
        }

        return render(request, "Rhabit/Sealed_Pages.html", vars)
    else:
        return HttpResponseRedirect("http://[2001:7c0:2320:2:f816:3eff:fe82:34b2]/RHabit/Seiten/Hoppla.html")
