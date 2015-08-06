from django.shortcuts import render
#coding:utf-8
# Create your views here.
import random
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
from datetime import datetime
from othermodule.game import *
import json
# Create your views here.
size = 10

def validate(request,username,password):
    flag = False
    user = authenticate(username=username,password=password)
    if user is not None:
        if user.is_active:
            return True
    return flag


def user_reg(request):
    error = []
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
                    user.save()
                    img = Image.open(request.FILES['image'])
                    width, height = img.size
                    img.thumbnail((width/size, height/size), Image.ANTIALIAS)
                    img.save('static/images/faceimage/' + user.username + '.' + img.format)
                    image_path = "/static/images/faceimage/" + user.username + '.' + img.format
                    current_player = ChessPlayer(
                        user = User.objects.filter(username=name)[0],
                        nick_name = nickname,
                        game_state = 'online',
                        image = image_path,
                    )
                    current_player.save()
                    validate(request,name,password)
                    return render_to_response('login.html',{
                            'error':[],
                            'form':LoginForm(),
                    },context_instance=RequestContext(request))
                else:
                    error.append('请输入相同密码')
            else:
                error.append('用户名已经存在，请更改你的用户名')
        else:
            error.append('注册信息未填写完整，请检查')
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
            if validate(request, username, password):
                current_user = User.objects.filter(username=username)[0].id
                current_player = ChessPlayer.objects.filter(user_id=current_user)[0]
                current_player.game_state = 'online'
                current_player.save()
                current_roomid = getRoomidByid(current_player.id)
                if current_roomid != 0:
                    current_player.game_state = 'gaming'
                    return enterroom(request, current_roomid, current_player.id)

                roomlist_str = getroomstate()
                ranking = []
                players = ChessPlayer.objects.all()
                for player in players:
                    ranking.append(player)
                ranking.sort(key=lambda x:x.game_grade, reverse=True)
                relation = Relationship.objects.all()
                friends = []
                for item in relation:
                    if item.user1_id == current_player.id:
                        friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
                    elif item.user2_id == current_player.id:
                        friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
                friends.sort(key=lambda x:x.game_grade, reverse=True)
                return render_to_response("index.html",{
                    'form_check_info':CheckUserInfo(),
                    'error':[],
                    'current_player':current_player,
                    'players':ranking,
                    'friends':friends,
                    'rowlist': rowlist,
                    'collist': collist,
                    'id':current_player.id,
                    'form':AddFriend(),
                    'image':current_player.image,
                    'selfid': current_player.id,
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
    current_player.game_state = 'offline'
    current_player.save()
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
        'current_player': current_player,
        'error':error,
        'form':form,
    },context_instance=RequestContext(request))


def to_index(request, id):
    current_player = ChessPlayer.objects.filter(id=int(id))[0]
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
    friends.sort(key=lambda x:x.game_grade, reverse=True)
    return render_to_response("index.html", {
        'form_check_info':CheckUserInfo(),
        'error':[],
        'current_player':current_player,
        'friends':friends,
        'players':ranking,
        'rowlist': rowlist,
        'collist': collist,
        'id':current_player.id,
        'form':AddFriend(),
        'image':current_player.image,
        'selfid':current_player.id,
    },context_instance=RequestContext(request))

def update_password(request, id):
    error = []
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id=int(id))[0]
    if request.method == 'POST':
        form = UpdatePasswordForm(request.POST)
        username = current_player.user.username
        if form.is_valid():
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
                            ranking = []
                            players = ChessPlayer.objects.all()
                            for player in players:
                                ranking.append(player)
                            ranking.sort(key=lambda x:x.game_grade, reverse=True)
                            relation = Relationship.objects.all()
                            friends = []
                            for item in relation:
                                if item.user1_id == current_player.id:
                                    friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
                                elif item.user2_id == current_player.id:
                                    friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
                            friends.sort(key=lambda x:x.game_grade, reverse=True)
                            return render_to_response("index.html",{
                                'error':[],
                                'form':AddFriend(),
                                'form_check_info':CheckUserInfo(),
                                'current_user':username,
                                'players':ranking,
                                'friends':friends,
                                'rowlist': rowlist,
                                'collist': collist,
                                'id':current_player.id,
                                'image':current_player.image,
                                'selfid':current_player.id,
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
            error.append(u"信息不完整，请检查")
    else:
        form = UpdatePasswordForm()
    return render_to_response("update_password.html",{
        'id':id,
        'current_player':current_player,
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
            img.save('static/images/faceimage/' + current_user.username + '.' + img.format)
            current_player.image = '/static/images/faceimage/' + current_user.username + '.' + img.format
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
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
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
        else:
            error = '请输入要添加的好友的账户'
    friends.sort(key=lambda x:x.game_grade, reverse=True)
    return render_to_response("index.html",{
        'error':error,
        'form_check_info':CheckUserInfo(),
        'form':AddFriend(),
        'friend_request':friend_request,
        'current_user':current_user.username,
        'rowlist': rowlist,
        'collist': collist,
        'players': ranking,
        'friends': friends,
        'id':current_player.id,
        'image':current_player.image,
        'selfid':current_player.id,
    },context_instance=RequestContext(request))


def delete_friend(request, id, delete_id):
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    delete_relation = Relationship.objects.filter(user1_id=int(id), user2_id=int(delete_id))
    if delete_relation != []:
        delete_relation.delete()
    delete_relation =  Relationship.objects.filter(user1_id=int(delete_id), user2_id=int(id))
    if delete_relation != []:
        delete_relation.delete()
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
    friends.sort(key=lambda x:x.game_grade, reverse=True)
    return render_to_response("index.html",{
        'error':[],
        'form_check_info':CheckUserInfo(),
        'form':AddFriend(),
        'rowlist': rowlist,
        'collist': collist,
        'current_player':current_player,
        'players':ranking,
        'friends':friends,
        'id':current_player.id,
        'image':current_player.image,
        'selfid':current_player.id,
    },context_instance=RequestContext(request))

def check_friend_info(request, id):
    error = ''
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
    if request.method == 'POST':
        form = CheckUserInfo(request.POST)
        if form.is_valid():
            friend = User.objects.filter(username = form.cleaned_data['username'])
            if friend:
                player = ChessPlayer.objects.filter(user_id = friend[0].id)[0]
                if not friend[0].is_active:
                    player.game_state = 'offline'
                return render_to_response('friend_info.html',{
                    'player':player,
                    'id':current_player.id,
                },context_instance=RequestContext(request))
            else:
                error = '用户不存在！'
        else:
            error = '请输入要查看好友的账户'
    friends.sort(key=lambda x:x.game_grade, reverse=True)
    return render_to_response("index.html",{
        'error':error,
        'form_check_info':CheckUserInfo(),
        'form':AddFriend(),
        'rowlist': rowlist,
        'collist': collist,
        'current_user':current_user.username,
        'players':ranking,
        'friends':friends,
        'id':current_player.id,
        'image':current_player.image,
        'selfid':current_player.id,
    },context_instance=RequestContext(request))


def random_match(request, id):
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    error = []
    candidates = Room.objects.filter(guest_id=0)
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
    friends.sort(key=lambda x:x.game_grade, reverse=True)
    rooms = Room.objects.all()
    for room in rooms:
        if room.owner_id == int(id) or room.guest_id == int(id):
            if room.owner_id == int(id):
                return render_to_response('room.html', {
                        'static': STATIC_URL,
                        'canvasWidth': canvasWidth,
                        'canvasHeight': canvasHeight,
                        'boardheight': boardheight,
                        'boardwidth': boardwidth,
                        'gridwidth': gridwidth,
                        'delta': delta,
                        'selfid': int(id),
                        'roomid':room.id,
                        'enemyid': '=' + str(room.guest_id),
                        'mycolor': 1,
                        'enemycolor':2,
                        'enemyimg': ChessPlayer.objects.filter(id=room.guest_id)[0].image,
                        'enemyname': ChessPlayer.objects.filter(id=room.guest_id)[0].user.username,
                        'ifmyturn': 'true',
                        'ifowner': 'true',
                        'current_player':current_player,
                },context_instance=RequestContext(request))
            else:
                return render_to_response('room.html', {
                                'static': STATIC_URL,
                                'canvasWidth': canvasWidth,
                                'canvasHeight': canvasHeight,
                                'boardheight': boardheight,
                                'boardwidth': boardwidth,
                                'gridwidth': gridwidth,
                                'delta': delta,
                                'selfid': int(id),
                                'roomid':room.id,
                                'enemyid': '=' + str(room.owner_id),
                                'mycolor': 2,
                                'enemycolor':1,
                                'enemyimg': ChessPlayer.objects.filter(id=room.owner_id)[0].image,
                                'enemyname': ChessPlayer.objects.filter(id=room.owner_id)[0].user.username,
                                'ifmyturn': 'false',
                                'ifowner': 'false',
                                'current_player':current_player,
                    },context_instance=RequestContext(request))

    if candidates == []:
        error.append(u"房间已满!")
        return render_to_response("index.html",{
            'error':error,
            'form_check_info':CheckUserInfo(),
            'form':AddFriend(),
            'rowlist': rowlist,
            'collist': collist,
            'current_user':current_user.username,
            'players':ranking,
            'friends':friends,
            'id':current_player.id,
            'image':current_player.image,
            'selfid':current_player.id,
        },context_instance=RequestContext(request))
    else:
        owner_candidates = []
        no_owner_candidates = []
        for room in candidates:
            if room.owner_id != 0:
                owner_candidates.append(room)
            no_owner_candidates.append(room)
        current_player.game_state = 'pregame'
        current_player.save()
        if owner_candidates == []:
            random.shuffle(no_owner_candidates)
            no_owner_candidates[0].owner_id = int(id)
            no_owner_candidates[0].game_state = 'pregame'
            no_owner_candidates[0].last_steptime=datetime.now()
            no_owner_candidates[0].pausestart =datetime.now()
            no_owner_candidates[0].save()
            enemyimg = ''
            enemyname = ''
            online_players = ChessPlayer.objects.filter(game_state='online')
            for player in online_players:
                content = 'ENTERROOM' + '&' + id + '_' + str(no_owner_candidates[0].id) + '_1'
                m = Message(publisher_id = 0, receiver_id = player.id, type = 'ENTERROOM', content = content)
                m.save()
            return render_to_response('room.html', {
                'static': STATIC_URL,
                'canvasWidth': canvasWidth,
                'canvasHeight': canvasHeight,
                'boardheight': boardheight,
                'boardwidth': boardwidth,
                'gridwidth': gridwidth,
                'delta': delta,
                'selfid': int(id),
                'roomid':no_owner_candidates[0].id,
                'enemyid': '',
                'mycolor': 1,
                'enemycolor':2,
                'enemyimg': enemyimg,
                'enemyname': enemyname,
                'ifmyturn': 'true',
                'ifowner': 'true',
                'current_player':current_player,
            },context_instance=RequestContext(request))
        else:
            random.shuffle(owner_candidates)
            owner_candidates[0].guest_id = int(id)
            owner_candidates[0].game_state='pregame'
            owner_candidates[0].last_steptime=datetime.now()
            owner_candidates[0].pausestart=datetime.now()
            owner_candidates[0].save()
            enemy = ChessPlayer.objects.filter(id=owner_candidates[0].owner_id)[0]
            enemyimg = enemy.image.url
            enemyname = enemy.user.username
            content = 'ENEMY' + '&' + id + '_' + current_player.image.url + '_' + current_player.user.username
            m = Message(publisher_id = 0, receiver_id = owner_candidates[0].owner_id, type = 'ENEMY', content = content)
            m.save()
            online_players = ChessPlayer.objects.filter(game_state='online')
            for player in online_players:
                content = 'ENTERROOM' + '&' + id + '_' + str(owner_candidates[0].id) + '_2'
                m = Message(publisher_id = 0, receiver_id = player.id, type = 'ENTERROOM', content = content)
                m.save()
            return render_to_response('room.html', {
                'static': STATIC_URL,
                'canvasWidth': canvasWidth,
                'canvasHeight': canvasHeight,
                'boardheight': boardheight,
                'boardwidth': boardwidth,
                'gridwidth': gridwidth,
                'delta': delta,
                'selfid': int(id),
                'roomid':owner_candidates[0].id,
                'enemyid': '=' + str(owner_candidates[0].owner_id),
                'mycolor': 2,
                'current_player':current_player,
                'enemycolor': 1,
                'enemyimg': enemyimg,
                'enemyname': enemyname,
                'ifmyturn': 'false',
                'ifowner': 'false',
                'current_player':current_player,
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
    self = ChessPlayer.objects.get(id = id_sender)
    self.last_ask = datetime.now()
    if self.game_state == 'offline':
        self.game_state = 'online'
    self.save()
    allplayers = ChessPlayer.objects.all()
    for player in allplayers:
        aware_dt = player.last_ask
        naive_dt = aware_dt.replace(tzinfo = None)
        time_past = timedelta_ms(datetime.now() - naive_dt)
        print (time_past)
        if time_past > 5000:
            m_off(str(player.id))
    list_msend = []
    if messagelist != '':
        print (1)
        messagesToHandle = messagelist.split('+')
        for mr in messagesToHandle:
            print (mr)
            head, body = mr.split('&')
            if head == 'ONESTEP':
                m_oneStep(body)
            if head == 'RGAMESTART':
                m_rGameStart(body)
            if head == 'AGAMESTART':
                m_aGameStart(body)
            if head == 'NAGAMESTART':
                m_naGameStart(body)
            if head == 'RFRIEND':
                m_rFriend(body)
            if head == 'AFRIEND':
                m_aFriend(body)
            if head == 'NAFRIEND':
                m_naFriend(body)
            if head == 'RREGRET':
                m_rRegret(body)
            if head == 'AREGRET':
                m_aRegret(body)
            if head == 'NAREGRET':
                m_naRegret(body)
            if head == 'RTIE':
                m_rTie(body)
            if head == 'ATIE':
                m_aTie(body)
            if head == 'NATIE':
                m_naTie(body)
            if head == 'ROOMINFO':
                rs = getroomstate()
                print(rs)
                list_msend.append('ROOMINFO' + '&' + getroomstate())
            if head == 'ENTERROOM':
                m_enterRoom(body)
            if head == 'GG':
                m_gg(body)
            if head == 'OFF':
                m_off(body)
    
    for ms in Message.objects.filter(receiver_id = id_sender):
        print (2)
        list_msend.append(ms.content)
        ms.delete()
    id_room = getRoomidByid(id_sender)
    if id_room != 0:
        room_ins = Room.objects.get(id = id_room)
        if room_ins.game_state == 'pause':
            time_past = timedelta_ms(room_ins.pausestart - room_ins.last_steptime)
            time_remain = 60000 - time_past
            time_remain = int(time_remain)
            m_time = 'TIME' + '&' + str(time_remain)
            list_msend.append(m_time)
        if room_ins.game_state == 'gaming':
            aware_dt = room_ins.last_steptime
            naive_dt = aware_dt.replace(tzinfo = None)
            time_past = timedelta_ms(datetime.now() - naive_dt)
            time_remain = 60000 - time_past
            time_remain = int(time_remain)
            m_time = 'TIME' + '&' + str(time_remain)
            list_msend.append(m_time)
            if time_remain <= 0:
                winner = room_ins.owner_id + room_ins.guest_id - room_ins.whose_turn
                loser = room_ins.whose_turn
                g_EndGame(False, winner, loser, id_room)
                
    response = '+'.join(list_msend)
    print(response, id_sender)
    return HttpResponse(response)

def timedelta_ms(td):
    return td.days * 86400000 + td.seconds * 1000 + td.microseconds / 1000

def enterroom(request, roomid, selfid):
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    room_ins = Room.objects.get(id = roomid);
    if room_ins.game_state == 'gaming':
        boardinit = room_ins.chess_board
    else:
        boardinit = ''
    if room_ins.owner_id == 0  or (room_ins.owner_id==int(selfid) and room_ins.guest_id == 0):
        room_ins.owner_id = selfid
        ifowner = 'true'
        mycolor = 1
        enemycolor = 2
        enemyid = ''
        enemyimg = ''
        enemyname = ''
        ifmyturn = 'false'
        role = '1'
    elif room_ins.owner_id==int(selfid) and room_ins.guest_id != 0:
        room_ins.owner_id = selfid
        ifowner = 'true'
        mycolor = 1
        enemycolor = 2
        enemy = ChessPlayer.objects.get(id = room_ins.guest_id)
        enemyid = '=' + str(room_ins.guest_id)
        enemyimg = enemy.image.url
        enemyname = enemy.user.username
        ifmyturn = 'true'
        role = '1'
    elif room_ins.guest_id == int(selfid):
        room_ins.guest_id = selfid
        ifowner = 'false'
        mycolor = 2
        enemycolor = 1
        enemy = ChessPlayer.objects.get(id = room_ins.owner_id)
        enemyid = '=' + str(room_ins.owner_id)
        enemyimg = enemy.image.url
        enemyname = enemy.user.username
        ifmyturn = 'false'
        role = '2'
    else:
        room_ins.guest_id = selfid
        ifowner = 'false'
        mycolor = 2
        enemycolor = 1
        self = ChessPlayer.objects.get(id = selfid)
        content = 'ENEMY' + '&' + selfid + '_' + self.image.url + '_' + self.user.username
        m = Message(publisher_id = 0, receiver_id = room_ins.owner_id, type = 'ENEMY', content = content)
        m.save()
        enemy = ChessPlayer.objects.get(id = room_ins.owner_id)
        enemyid = '=' + str(room_ins.owner_id)
        enemyimg = enemy.image.url
        enemyname = enemy.user.username
        ifmyturn = 'false'
        role = '2'
    if room_ins.game_state != 'gaming':
        room_ins.pausestart = datetime.now()
        room_ins.last_steptime = datetime.now()
        room_ins.game_state = 'pregame'
    room_ins.save()
    #faxiaoxi gaosu suoyu ren
    room_owner = ChessPlayer.objects.filter(id = int(room_ins.owner_id))[0]
    current_player = ChessPlayer.objects.filter(id = int(selfid))[0]
    current_player.game_state = 'pregame'
    current_player.save()
    online_players = ChessPlayer.objects.filter(game_state = 'online')
    for player in online_players:
        content = 'ENTERROOM' + '&' + str(selfid) + '_' + str(roomid) + '_' + role
        m = Message(publisher_id = 0, receiver_id = player.id, type = 'ENTERROOM', content = content)
        m.save()
    if room_ins.game_state == 'gaming':
        current_player.game_state = 'gaming'
        current_player.save()
        if selfid == room_ins.whose_turn:
            ifmyturn = 'true'
        else:
            ifmyturn = 'false'
    return render_to_response('room.html', {
        'static': STATIC_URL,
        'canvasWidth': canvasWidth, 
        'canvasHeight': canvasHeight, 
        'boardheight': boardheight, 
        'boardwidth': boardwidth, 
        'gridwidth': gridwidth, 
        'delta': delta, 
        'selfid': selfid,
        'current_player':current_player,
        'room_owner':room_owner,
        'mycolor': mycolor, 
        'enemycolor': enemycolor,
        'ifmyturn': ifmyturn, 
        'ifowner': ifowner,
        'roomid': str(roomid),
        'enemyid': enemyid,
        'enemyimg': enemyimg,
        'enemyname': enemyname,
        'boardinit': boardinit,
        })
def exit_room(request, room_id, id):
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    room = Room.objects.get(id=int(room_id))
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_player.game_state = 'online'
    current_player.save()
    ranking = []
    players = ChessPlayer.objects.all()
    for player in players:
        ranking.append(player)
    ranking.sort(key=lambda x:x.game_grade, reverse=True)
    relation = Relationship.objects.all()
    friends = []
    for item in relation:
        if item.user1_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
        elif item.user2_id == current_player.id:
            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
    if room.owner_id == int(id):
        room.owner_id = room.guest_id
    if room.game_state == 'gaming':
        winner = ChessPlayer.objects.filter(id=room.owner_id)[0]
        winner.game_state = 'pregame'
        winner.game_num = winner.game_num + 1
        winner.game_grade = winner.game_grade + 2
        winner.save()
        m = Message(publisher_id = 0, receiver_id = room.owner_id, type = 'WIN', content = 'WIN')
        m.save()
    content = 'ENEMY' + '&0__'
    m = Message(publisher_id = 0, receiver_id = room.owner_id, type = 'ENEMY', content = content)
    m.save()
    if room.owner_id != 0:
        owner = ChessPlayer.objects.filter(id=room.owner_id)[0]
        content = 'OWNER'+'&'+str(owner.user.username)
        m = Message(publisher_id = 0, receiver_id = room.owner_id, type = 'OWNER', content = content)
        m.save()
    room.guest_id = 0
    room.whose_turn = 0
    room.game_state = 'pregame'
    room.whose_turn = 0
    room.last_steptime = datetime.now()
    room.pausestart = datetime.now()
    room.save()
    online_players = ChessPlayer.objects.exclude(game_state='offline')
    for player in online_players:
        content = 'EXITROOM' + '&' + str(room.owner_id) + '_' + room_id
        m = Message(publisher_id = 0, receiver_id = player.id, type = 'EXITROOM', content = content)
        m.save()
    return render_to_response("index.html",{
        'form_check_info':CheckUserInfo(),
        'error':[],
        'current_player':current_player,
        'players':ranking,
        'friends':friends,
        'rowlist': rowlist,
        'collist': collist,
        'id':current_player.id,
        'form':AddFriend(),
        'image':current_player.image,
        'selfid': current_player.id,
        },context_instance=RequestContext(request))

def letgo(request, roomid, id):
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    room = Room.objects.filter(id=int(roomid))[0]
    if room.owner_id == int(id):
        content = 'ENEMY' + '&0__'
        m = Message(publisher_id = 0, receiver_id = room.owner_id, type = 'ENEMY', content = content)
        m.save()
        content = 'LETGO' + '&' +  str(room.guest_id)
        m = Message(publisher_id = 0, receiver_id = room.guest_id, type = 'LETGO', content = content)
        m.save()
        room.guest_id = 0
        room.whose_turn = 0
        room.game_state = 'pregame'
        room.whose_turn = 0
        room.last_steptime = datetime.now()
        room.pausestart = datetime.now()
        room.save()
        online_players = ChessPlayer.objects.filter(game_state='online')
        for player in online_players:
            content = 'EXITROOM' + '&' + str(room.owner_id) + '_' + roomid
            m = Message(publisher_id = 0, receiver_id = player.id, type = 'EXITROOM', content = content)
            m.save()
        return render_to_response('room.html', {
            'static': STATIC_URL,
            'canvasWidth': canvasWidth,
            'canvasHeight': canvasHeight,
            'boardheight': boardheight,
            'boardwidth': boardwidth,
            'gridwidth': gridwidth,
            'delta': delta,
            'selfid': int(id),
            'current_player':ChessPlayer.objects.filter(id=int(id))[0],
            'room_owner':ChessPlayer.objects.filter(id=int(room.owner_id))[0],
            'mycolor': 1,
            'enemycolor': 2,
            'ifmyturn': 'false',
            'ifowner': 'true',
            'roomid': str(roomid),
            'enemyid': '',
            'enemyimg': '',
            'enemyname': '',
            })

def hostchange(request, roomid, id):
    canvasWidth = 537
    canvasHeight = 537
    boardwidth = 490
    boardheight = 490
    gridwidth = boardheight / 14
    delta = 23
    room = Room.objects.filter(id=int(roomid))[0]
    if room.owner_id == int(id):
        if room.guest_id != 0:
            temp = room.guest_id
            room.guest_id = room.owner_id
            room.owner_id = temp
            room.save()
            owner = ChessPlayer.objects.filter(id=room.owner_id)[0]
            content = 'OWNER'+'&'+str(owner.user.username)
            m = Message(publisher_id = 0, receiver_id = room.owner_id, type = 'OWNER', content = content)
            m.save()
            guest = ChessPlayer.objects.filter(id=room.guest_id)[0]
            content = 'GUEST'+'&'+str(owner.user.username)
            m = Message(publisher_id = 0, receiver_id = room.guest_id, type = 'GUEST', content = content)
            m.save()
            online_players = ChessPlayer.objects.filter(game_state='online')
            for player in online_players:
                content = 'HOSTCHANGE' + '&' + roomid
                m = Message(publisher_id = 0, receiver_id = player.id, type = 'HOSTCHANGE', content = content)
                m.save()
        return render_to_response('room.html', {
            'static': STATIC_URL,
            'canvasWidth': canvasWidth,
            'canvasHeight': canvasHeight,
            'boardheight': boardheight,
            'boardwidth': boardwidth,
            'gridwidth': gridwidth,
            'delta': delta,
            'selfid': int(id),
            'current_player':ChessPlayer.objects.filter(id=int(id))[0],
            'room_owner':ChessPlayer.objects.filter(id=int(room.owner_id))[0],
            'mycolor': 2,
            'enemycolor': 1,
            'ifmyturn': 'false',
            'ifowner': 'false',
            'roomid': str(roomid),
            'enemyid': '=' + str(owner.id),
            'enemyimg': owner.image.url,
            'enemyname': owner.user.username,
            })


def getroomstate():
    roomlist = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for room in Room.objects.all():
        room_item = {}
        room_item['owner'] = room.owner_id
        room_item['guest'] = room.guest_id
        roomlist[room.id] = room_item
    return json.dumps(roomlist)
