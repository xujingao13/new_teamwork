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
from datetime import datetime
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
                    user.save()
                    current_user = User.objects.filter(username=name)[0].id
                    img = Image.open(request.FILES['image'])
                    width, height = img.size
                    img.thumbnail((width/size, height/size), Image.ANTIALIAS)
                    img.save('static/images/faceimage/' + user.username + '.' + img.format)
                    image_path = "/static/images/faceimage/" + user.username + '.' + img.format
                    current_player = ChessPlayer(
                        user = User.objects.filter(username=name)[0],
                        nick_name = nickname,
                        game_state = u'online',
                        image = image_path,
                    )
                    current_player.save()
                    validate(request,name,password)
                    online_players = ChessPlayer.objects.exclude(game_state=u'offline')
                    relation = Relationship.objects.all()
                    friends = []
                    for item in relation:
                        if item.user1_id == current_player.id:
                            friends.append(ChessPlayer.objects.filter(id=item.user2_id)[0])
                        elif item.user2_id == current_player.id:
                            friends.append(ChessPlayer.objects.filter(id=item.user1_id)[0])
                    friends.sort(key=lambda x:x.game_grade, reverse=True)
                    return render_to_response('index.html',{
                        'form_check_info':CheckUserInfo(),
                        'error':[],
                        'players':online_players,
                        'friends':friends,
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
                current_player.game_state = u'online'
                current_player.save()
                roomlist_str = getroomstate()
                online_players = ChessPlayer.objects.exclude(game_state=u'offline')
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
                    'players':online_players,
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
    current_player.game_state = u'offline'
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
    online_players = ChessPlayer.objects.exclude(game_state=u'offline')
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
        'players':online_players,
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
                            online_players = ChessPlayer.objects.exclude(game_state=u'offline')
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
                                'current_user':username,
                                'players':online_players,
                                'friends':friends,
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
    online_players = ChessPlayer.objects.exclude(game_state=u'离线')
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
        'players': online_players,
        'friends': friends,
        'id':current_player.id,
        'image':current_player.image,
    },context_instance=RequestContext(request))


def delete_friend(request, id, delete_id):
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    online_players = ChessPlayer.objects.exclude(game_state=u'offline')
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
        'players':online_players,
        'friends':friends,
        'id':current_player.id,
        'image':current_player.image,
    },context_instance=RequestContext(request))

def check_friend_info(request, id):
    error = ''
    rowlist = [0, 1, 2, 3, 4, 5]
    collist = [0, 1, 2]
    current_player = ChessPlayer.objects.filter(id = int(id))[0]
    current_user = current_player.user
    online_players = ChessPlayer.objects.exclude(game_state=u'offline')
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
        'players':online_players,
        'friends':friends,
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
    if room_ins.owner_id == 0:
        room_ins.owner_id = selfid
        ifowner = 'true'
        mycolor = 1
        enemycolor = 2
        enemyid = ''
        enemyimg = ''
        enemyname = ''
        ifmyturn = 'false'
        role = '1'
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
    room_ins.pausestart = datetime.now()
    room_ins.last_steptime = datetime.now()
    room_ins.save()
    #faxiaoxi gaosu suoyu ren
    current_player = ChessPlayer.objects.filter(id = int(selfid))[0]
    players = ChessPlayer.objects.filter(game_state = 'online')
    for player in players:
        content = 'ENTERROOM' + '&' + selfid + '_' + roomid + '_' + role
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
        'selfid': selfid,
        'current_player':current_player,
        'mycolor': mycolor, 
        'enemycolor': enemycolor,
        'ifmyturn': ifmyturn, 
        'ifowner': ifowner,
        'roomid': roomid,
        'enemyid': enemyid,
        'enemyimg': enemyimg,
        'enemyname': enemyname,
        })
def getroomstate():
    roomlist = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    for room in Room.objects.all():
        room_item = {}
        room_item['owner'] = room.owner_id
        room_item['guest'] = room.guest_id
        roomlist[room.id] = room_item
    return json.dumps(roomlist)
