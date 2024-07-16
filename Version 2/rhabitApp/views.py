import json
import math
import os
from datetime import date, datetime

from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render


def user_page(request):
  return render(request, 'rhabitApp/user_page.html', {})

def profile_page(request):
  if 'uid' in request.session:
    uid = request.session['uid']
    vars = { 'private': True, 'uid': uid }
    action = request.POST.get('action', '')
    milestoneIndex = request.POST.get('milestoneIndex', '')
    habitIndex = request.POST.get('habitIndex', '')
    uname = request.POST.get('uname', '')
    pwd = request.POST.get('pwd', '')
    habitEnd = request.POST.get('habitEnd', '')
    habitStart = request.POST.get('habitStart', '')
    habitName = request.POST.get('habitName', '')
    milestoneName = request.POST.get('milestoneName', '')
    bio = request.POST.get('bio', '')
    email = request.POST.get('email', '')
    if action != '':
      data = {}
      with open(f'data/users/{uid}.json', 'r') as file:
        data = json.load(file)
      if action == 'deleteMilestone':
        del data['currentHabits'][int(habitIndex)]['milestones'][int(milestoneIndex)]
      elif action == 'editMilestone':
        data['currentHabits'][int(habitIndex)]['milestones'][int(milestoneIndex)]['content'] = milestoneName
      elif action == 'deleteHabit':
        del data['currentHabits'][int(habitIndex)]
      elif action == 'changeUsername':
        data['name'] = uname
      elif action == 'changePassword':
        data['pwd'] = pwd
      elif action == 'changePicture':
        fileUpload = request.FILES['picture']
        fs = FileSystemStorage('rhabitApp/static/profiles')
        if os.path.isfile(f'rhabitApp/static/profiles/{uid}.png'):
          os.remove(f'rhabitApp/static/profiles/{uid}.png')
        fs.save(f'{uid}.png', fileUpload)
        data['picture'] = True
      elif action == 'deletePicture':
        if os.path.isfile(f'rhabitApp/static/profiles/{uid}.png'):
          os.remove(f'rhabitApp/static/profiles/{uid}.png')
        data['picture'] = False
      elif action == 'addHabit':
        data['currentHabits'].append({
          'name': habitName,
          'startDate': habitStart,
          'endDate': habitEnd,
          'milestones': []
        })
      elif action == 'changeEmail':
        data['email'] = email
      elif action == 'addMilestone':
        data['currentHabits'][int(habitIndex)]['milestones'].append({
          'content': milestoneName,
          'completedDate': ''
        })
      elif action == 'editBio':
        data['bio'] = bio
      elif action == 'logout':
        del request.session['uid']
        return redirect(login_page)
      with open(f'data/users/{uid}.json', 'w') as file:
        file.write(json.dumps(data, indent = 2))
    with open(f'data/users/{uid}.json', 'r') as file:
      vars.update(json.load(file))
    pictureUrl = 'imgs/Logo.png'
    if vars['picture']:
      pictureUrl = f'profiles/{uid}.png'
    vars.update({
      'followingAmount': len(vars['following']),
      'followerAmount': len(vars['followers']),
      'habitsAmount': len(vars['habits']),
      'pictureUrl': pictureUrl,
    })
    for habit in vars['currentHabits']:
      endDate = datetime.strptime(habit['endDate'], '%Y-%m-%d')
      startDate = datetime.strptime(habit['startDate'], '%Y-%m-%d')
      currentDate = datetime.now()
      totalDays = (endDate - startDate).days
      elapsedDays = (currentDate - startDate).days
      percentage = math.ceil(min((elapsedDays / totalDays) * 100, 100))
      habit['percentage'] = percentage
    for i in range(len(vars['followers'])):
      with open(f'data/users/{vars["followers"][i]}.json', 'r') as file:
        data = json.load(file)
      vars['followers'][i] = data['name']
    for i in range(len(vars['following'])):
      with open(f'data/users/{vars["following"][i]}.json', 'r') as file:
        data = json.load(file)
      vars['following'][i] = data['name']
    return render(request, 'rhabitApp/user_page.html', vars)
  else:
    return redirect(login_page)

def home_page(request):
  if 'uid' in request.session:
    uid = request.session['uid']
    vars = { 'users': [] }
    users = []
    with open(f'data/users/{uid}.json', 'r') as file:
      users = json.load(file)['following']
    for user in users:
      userData = {}
      with open(f'data/users/{user}.json', 'r') as file:
        userData.update(json.load(file))
      pictureUrl = 'imgs/Logo.png'
      if userData['picture']:
        pictureUrl = f'profiles/{user}.png'
      userData.update({
        'followingAmount': len(userData['following']),
        'followerAmount': len(userData['followers']),
        'habitsAmount': len(userData['habits']),
        'pictureUrl': pictureUrl,
        'uid': user
      })
      for i in range(len(userData['followers'])):
        with open(f'data/users/{userData["followers"][i]}.json', 'r') as file:
          data = json.load(file)
        userData['followers'][i] = data['name']
      for i in range(len(userData['following'])):
        with open(f'data/users/{userData["following"][i]}.json', 'r') as file:
          data = json.load(file)
        userData['following'][i] = data['name']
      for habit in userData['currentHabits']:
        endDate = datetime.strptime(habit['endDate'], '%Y-%m-%d')
        startDate = datetime.strptime(habit['startDate'], '%Y-%m-%d')
        currentDate = datetime.now()
        totalDays = (endDate - startDate).days
        elapsedDays = (currentDate - startDate).days
        percentage = math.ceil(min((elapsedDays / totalDays) * 100, 100))
        habit['percentage'] = percentage
      vars['users'].append(userData)
    return render(request, 'rhabitApp/home_page.html', vars)
  else:
    return redirect(login_page)

def search_page(request):
  if 'uid' in request.session:
    uid = request.session['uid']
    followUid = request.POST.get('followUid', '')
    unfollowUid = request.POST.get('unfollowUid', '')
    search = request.POST.get('search', '')
    if followUid != '':
      with open(f'data/users/{uid}.json', 'r') as file:
        data = json.load(file)
      data['following'].append(followUid)
      with open(f'data/users/{uid}.json', 'w') as file:
        file.write(json.dumps(data, indent = 2))
      with open(f'data/users/{followUid}.json', 'r') as file:
        data = json.load(file)
      data['followers'].append(uid)
      with open(f'data/users/{followUid}.json', 'w') as file:
        file.write(json.dumps(data, indent = 2))
    elif unfollowUid != '':
      with open(f'data/users/{uid}.json', 'r') as file:
        data = json.load(file)
      data['following'].remove(unfollowUid)
      with open(f'data/users/{uid}.json', 'w') as file:
        file.write(json.dumps(data, indent = 2))
      with open(f'data/users/{unfollowUid}.json', 'r') as file:
        data = json.load(file)
      data['followers'].remove(uid)
      with open(f'data/users/{unfollowUid}.json', 'w') as file:
        file.write(json.dumps(data, indent = 2))
    vars = { 'users': [], 'following': [] }
    users = os.listdir('data/users')
    for user in users:
      userData = {}
      with open(f'data/users/{user}', 'r') as file:
        userData.update(json.load(file))
      pictureUrl = 'imgs/Logo.png'
      if userData['picture']:
        pictureUrl = f'profiles/{user.split(".")[0]}.png'
      userData.update({
        'followingAmount': len(userData['following']),
        'followerAmount': len(userData['followers']),
        'habitsAmount': len(userData['habits']),
        'pictureUrl': pictureUrl,
        'uid': user.split(".")[0]
      })
      for i in range(len(userData['followers'])):
        if userData["followers"][i] == uid:
          vars['following'].append(user.split(".")[0])
        with open(f'data/users/{userData["followers"][i]}.json', 'r') as file:
          data = json.load(file)
        userData['followers'][i] = data['name']
      for i in range(len(userData['following'])):
        with open(f'data/users/{userData["following"][i]}.json', 'r') as file:
          data = json.load(file)
        userData['following'][i] = data['name']
      vars['users'].append(userData)
      for i in range(len(vars['users'])):
        if search not in vars['users'][i]['name']:
          del vars['users'][i]
    return render(request, 'rhabitApp/search_page.html', vars)
  else:
    return redirect(login_page)

def login_page(request):
  if len(request.POST) > 0:
    uname = request.POST.get('uname', '')
    pwd = request.POST.get('pwd', '')
    uid = ''
    for file in os.listdir(f'data/users/'):
      with open(f'data/users/{file}', 'r') as fileContents:
        fileContents = json.load(fileContents)
        if fileContents['name'] == uname and fileContents['pwd'] == pwd:
          uid = file.split('.')[0]
    if uid != '':
      request.session['uid'] = uid
      return redirect(profile_page)
    else:
      return render(request, 'rhabitApp/error_page.html', { 'error': 'login' })
  else:
    return render(request, 'rhabitApp/login_page.html', { 'mode': 'login'})

def signup_page(request):
  if len(request.POST) > 0:
    uname = request.POST.get('uname', '')
    email = request.POST.get('email', '')
    pwd = request.POST.get('pwd', '')
    duplicate = False
    for file in os.listdir(f'data/users/'):
      with open(f'data/users/{file}', 'r') as fileContents:
        fileContents = json.load(fileContents)
        if fileContents['name'] == uname or fileContents['email'] == email:
          duplicate = True
    if not duplicate:
      uid = 0
      for item in os.listdir('data/users'):
        item_uid = int((item.split('.')[0])[1:])
        if item_uid > uid:
          uid = item_uid
      uid = 'u' + f'000{uid + 1}'[-4:]
      newData = {
        'name': uname,
        'email': email,
        'pwd': pwd,
        'creation': date.today().strftime('%Y-%m-%d'),
        'bio': '',
        'picture': False,
        'followers': [],
        'following': [],
        'currentHabits': [],
        'habits': []
      }
      with open(f'data/users/{uid}.json', 'w') as file:
        file.write(json.dumps(newData, indent = 2))
      request.session['uid'] = uid
      return redirect(profile_page)
    else:
      return render(request, 'rhabitApp/error_page.html', { 'error': 'signup' })
  else:
    return render(request, 'rhabitApp/login_page.html', { 'mode': 'signup'})
  
def about_us_page(request):
  return render(request, 'rhabitApp/aboutUs.html', {})

# def home(request):
#   if 'user' in request.session:
#     user = request.session['user']
#     return render(request, 'rhabitApp/home.html', { 'name': user })
#   else:
#     return render(request, 'rhabitApp/home.html', { 'name': 'Bitte einloggen!' })

# def login(request):
#   request.session['user'] = 'User1'
#   return render(request, 'rhabitApp/home.html', { 'name': 'Login Page' })

# def logout(request):
#   user = ''
#   try:
#     user = request.session['user']
#     del request.session['user']
#   except:
#     return render(request, 'rhabitApp/home.html', { 'name': 'Bitte einloggen!' })
#   return render(request, 'rhabitApp/home.html', { 'name': user + ' wurde ausgeloggt!' })