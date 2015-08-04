from django.shortcuts import render
#coding:utf-8
# Create your views here.
from django.template.loader import get_template
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response,RequestContext
from django.template import RequestContext
from player.models import *
from player.forms import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from othermodule.message import *
from django.template import Context
from my_project.settings import STATIC_URL
from PIL import Image
# Create your views here.
size = 1

def validate(request,username,password):
    flag = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            login(request,user)
            return True
    return flag


def user_reg(request):
    error = []
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    if request.method == 'POST':
        form = RegForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['username']
            nickname = form.cleaned_data['nickname']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if not User.objects.all().filter(username=name):
                if form.validate(password, password2):
                    user = User.objects.create_user(username=name,password=password)
                    user.save
                    current_user = User.objects.filter(username=name)[0].id
                    img = Image.open(request.FILES['image'])
                    width, height = img.size
                    img.thumbnail((width/size, height/size), Image.ANTIALIAS)
                    img.save('static/images/face_image/' + user.username + '.' + img.format)
                    image_path = "/static/images/face_image/" + user.username + '.' + img.format
                    current_player = ChessPlayer(
                        user = User.objects.filter(username=name)[0],
                        nick_name = nickname,
                        game_state = u'在线',
                        image = image_path,
                    )
                    current_player.save()
                    request.session['id'] = current_user
                    validate(request,name,password)
                    players = ChessPlayer.objects.all()
                    return render_to_response('index.html',{
                        'form_check_info':CheckUserInfo(),
                        'error':[],
                        'players':players,
                        'rowlist': rowlist,
                        'collist': collist,
                        'id':current_player.id,
                        'form':AddFriend(),
                        'current_player':current_player,
                        'image':current_player.image,
                    },context_instance=RequestContext(request))
                else:
                    error.append('Please input the same password')
            else:
                error.append('The username has existed,please change your username')
    else:
        form = RegForm()
    return render_to_response("addplayer.html", {
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))


@csrf_protect
def user_login(request):
    error = []
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            players = ChessPlayer.objects.all()
            if validate(request, username, password):
                current_user = User.objects.filter(username=username)[0].id
                current_player = ChessPlayer.objects.filter(user_id=current_user)[0]
                current_player.game_state = u'在线'
                current_player.save()
                return render_to_response("index.html",{
                    'form_check_info':CheckUserInfo(),
                    'error':[],
                    'current_player':current_player,
                    'players':players,
                    'rowlist': rowlist,
                    'collist': collist,
                    'id':current_player.id,
                    'form':AddFriend(),
                    'image':current_player.image,
                    },context_instance=RequestContext(request))
            else:
                error.append(u'请输入正确的密码')
        else:
            error.append(u'请输入账号和密码')
    else:
        form = LoginForm()
    return render_to_response("login.html",{
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))


def user_logout(request, id):
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_player.game_state = u'离线'
    current_player.save()
    logout(request)
    error = []
    form = LoginForm()
    return render_to_response("login.html",{
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))


def to_user_reg(request):
    error = []
    form = RegForm()
    return render_to_response("addplayer.html", {
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))

def to_update_password(request, id):
    error = []
    form = UpdatePasswordForm()
    current_player = ChessPlayer.objects.filter(id=int(id))[0]
    return render_to_response("update_password.html", {
        'id':current_player.id,
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))


def to_index(request, id):
    current_player = ChessPlayer.objects.filter(id=int(id))[0]
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    return render_to_response("index.html", {
        'form_check_info':CheckUserInfo(),
        'error':[],
        'current_player':current_player,
        'players':ChessPlayer.objects.all(),
        'rowlist': rowlist,
        'collist': collist,
        'id':current_player.id,
        'form':AddFriend(),
        'image':current_player.image,
    },context_instance=RequestContext(request))

def update_password(request, id):
    error = []
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id=int(id))[0]
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['origin_password']
            new_password = form.cleaned_data['new_password']
            new_password2 = form.cleaned_data['new_password2']
            if User.objects.all().filter(username=username):
                if User.objects.all().filter(username=username)[0].id == current_player.user.id:
                    if validate(request, username, password):
                        if form.validate(new_password, new_password2):
                            user = User.objects.all().filter(username=username)[0]
                            user.set_password(new_password)
                            user.save()
                            current_player = ChessPlayer.objects.filter(user_id=user.id)[0]
                            return render_to_response("index.html",{
                                'error':[],
                                'current_user':username,
                                'players':ChessPlayer.objects.all(),
                                'rowlist': rowlist,
                                'collist': collist,
                                'id':current_player.id,
                                'image':current_player.image,
                            },context_instance=RequestContext(request))
                        else:
                            error.append(u"请输入相同的新密码!")
                    else:
                        error.append(u"密码错误!")
                else:
                    error.append(u'请输入与当前用户匹配的用户名!')
            else:
                error.append(u"用户不存在!")
    else:
        form = UpdatePasswordForm()
    return render_to_response("update_password.html",{
        'id':id,
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))

def info(request, id):
    error = []
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    if request.method == 'POST':
        form = UpdateInfo(request.POST, request.FILES)
        image_flag = form.is_valid()
        nickname = form.cleaned_data['nickname']
        current_player.nick_name = nickname
        if image_flag:
            img = Image.open(request.FILES['image'])
            width, height = img.size
            img.thumbnail((width/size, height/size), Image.ANTIALIAS)
            img.save('static/images/face_image/' + current_user.username + '.' + img.format)
            current_player.image = '/static/images/face_image/' + current_user.username + '.' + img.format
        current_player.save()

    return render_to_response('info.html',{
        'error':error,
        'current_player':current_player,
        'form':UpdateInfo({'image':current_player.image,'nickname':current_player.nick_name}),
        'image':current_player.image,
    },context_instance=RequestContext(request))


def add_friend(request, id):
    error = ''
    friend_request = ''
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    if request.method == 'POST':
        form = AddFriend(request.POST)
        if form.is_valid():
            friend = User.objects.filter(username = form.cleaned_data['username'])
            if friend:
                if friend[0].id != current_user.id:
                    message = Message(
                        publisher_id = current_user.id,
                        receiver_id = friend[0].id,
                        type = 'friend_request',
                        content = 'RFRIEND&' + str(current_user.id),
                    )
                    message.save()
                    friend_request = '请求已发出'
                else:
                    error = '你不能添加自己为好友！'
            else:
                error = '用户不存在！'
    return render_to_response("index.html",{
        'error':error,
        'form_check_info':CheckUserInfo(),
        'form':AddFriend(),
        'friend_request':friend_request,
        'current_user':current_user.username,
        'rowlist': rowlist,
        'collist': collist,
        'players':ChessPlayer.objects.all(),
        'id':current_player.id,
        'image':current_player.image,
    },context_instance=RequestContext(request))

def check_friend_info(request, id):
    error = ''
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    if request.method == 'POST':
        form = CheckUserInfo(request.POST)
        if form.is_valid():
            friend = User.objects.filter(username = form.cleaned_data['username'])
            if friend:
                player = ChessPlayer.objects.filter(user_id = friend[0].id)[0]
                if not friend[0].is_active:
                    player.game_state = '离线'
                return render_to_response('friend_info.html',{
                    'player':player,
                },context_instance=RequestContext(request))
            else:
                error = '用户不存在！'
    return render_to_response("index.html",{
        'error':error,
        'form_check_info':CheckUserInfo(),
        'form':AddFriend(),
        'rowlist': rowlist,
        'collist': collist,
        'current_user':current_user.username,
        'players':ChessPlayer.objects.all(),
        'id':current_player.id,
        'image':current_player.image,
    },context_instance=RequestContext(request))

def gamehall(request):
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    return render_to_response("gamehall.html", {'rowlist': rowlist, 'collist': collist})

def player1(request):
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    t = get_template('current_datetime.html')
    html = t.render(Context({'static': STATIC_URL, 'canvasWidth': canvasWidth, 'canvasHeight': canvasHeight, 'boardheight': boardheight, 'boardwidth': boardwidth, 'gridwidth': gridwidth, 'delta': delta, 'selfid': '33', 'enemyid': '37', 'mycolor': '2', 'enemycolor': '1', 'ifmyturn': 'true', 'ifowner': 'true'}))
    return HttpResponse(html)

def player2(request):
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    t = get_template('current_datetime.html')
    html = t.render(Context({'static': STATIC_URL, 'canvasWidth': canvasWidth, 'canvasHeight': canvasHeight, 'boardheight': boardheight, 'boardwidth': boardwidth, 'gridwidth': gridwidth, 'delta': delta, 'selfid': '37', 'enemyid': '33', 'mycolor': '1', 'enemycolor': '2', 'ifmyturn': 'false', 'ifowner': 'false'}))
    return HttpResponse(html)

def message(request, message):
    print (message)
    id_sender, messagelist = message.split('@')
    id_sender = eval(id_sender)
    print('idsender:', id_sender, 'messagelist:', messagelist)
    if messagelist != '':
        print (1)
        messagesToHandle = messagelist.split(',')
        for mr in messagesToHandle:
            print (mr)
            head, body = mr.split('&')
            if head == 'ONESTEP':
                m_oneStep(body)
            if head == 'RGAMESTART':
                m_rGameStart(body)
            if head == 'AGAMESTART':
                m_aGameStart(body)
            if head == 'RFRIEND':
                m_rFriend(body)
            if head == 'AFRIEND':
                m_aFriend(body)

    list_msend = []
    for ms in Message.objects.filter(receiver_id = id_sender):
        print (2)
        list_msend.append(ms.content)
        ms.delete()
    response = ','.join(list_msend)
    print(response, id_sender)
    return HttpResponse(response)