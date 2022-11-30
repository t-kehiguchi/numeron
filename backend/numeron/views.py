import json
import random
from datetime import datetime
from django.core import serializers
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from numeron.models import Ranking
from numeron.models import User

def hello(request):
    return HttpResponse('Hello World ' + str(request.GET.get("greet")))

def login(request):
    # ローカル変数
    user = None
    isLogin = False
    playerFlag = False
    # ログインしているか、ログイン画面 or メイン画面へ遷移
    if request.method == "GET":
        if request.GET.get("id"):
            user = User.objects.filter(id=request.GET.get("id"))
            if user.exists():
                isLogin = True
                # プレイヤーの場合
                if not user[0].flag:
                    playerFlag = True
            return JsonResponse(data={'user':serializers.serialize("json", user),'login':isLogin,'playerFlag':playerFlag})
        else:
            return JsonResponse(data={'login':isLogin})
    # 実際にログイン
    else:
        try:
            # パラメータ取得
            param = json.loads(request.body)
            user = User.objects.filter(email=param.get('email'),password=param.get('password'))
            if user.exists():
                # 最終ログイン日時を現在日付を設定して一括更新
                user.update(recent_login_at=datetime.now())
                return JsonResponse(data={'user':serializers.serialize("json", user),'flag':True,'msg':''})
            else:
                return JsonResponse(data={'user':None,'flag':False,'msg':'ログインできませんでした。'})
        except:
            return JsonResponse(data={'user':None,'flag':False,'msg':'ユーザ更新失敗しました。'})

def new(request):
    # ログインしているか、ログイン画面 or メイン画面へ遷移
    if request.method == "GET":
        # 新規登録するIDを取得(ランダム8桁)
        id = random.randint(10000000, 99999999)
        # すでに登録されているIDが存在しないまで取得し続ける
        while User.objects.filter(id=id).count() == 1:
            id = random.randint(10000000, 99999999)
        return JsonResponse(data={'id':id})
    # 新規作成
    else:
        try:
            # パラメータ取得
            param = json.loads(request.body)
            # 登録前にメールアドレスが重複していないかチェック
            if User.objects.filter(email=str((param.get('email')))).count() > 0:
                return JsonResponse(data={'flag':False, 'msg':'メールアドレス重複しています。'})
            user = User(
                id = param.get('id'),
                name = param.get('name'),
                email = param.get('email'),
                password = param.get('password')
            )
            # 実際に登録
            user.save()
            return JsonResponse(data={'flag':True, 'msg':'ユーザ登録成功しました。'})
        except:
            return JsonResponse(data={'flag':False, 'msg':'ユーザ登録失敗しました。'})

def detail(request):
    # 該当プレイヤー取得
    user = User.objects.filter(id=request.GET.get("id"))[0]
    # 対戦回数(CPU、フレンド)
    count = {
      'cpu' : {
          'win'  : user.win_cpu,
          'lose' : user.lose_cpu,
          'draw' : user.draw_cpu
      },
      'friend' : {
          'win'  : user.win_friend,
          'lose' : user.lose_friend,
          'draw' : user.draw_friend
      }
    }
    # フレンド情報(対戦回数上位10件まで)
    # ID、氏名、対戦回数、勝率を取得できるように直SQLにて取得する
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_to, name, vs, CAST(win*100/vs AS SIGNED) AS winningRate\
                        FROM friend INNER JOIN user ON user.id = friend.id_to\
                        WHERE friend.id_from = %s order by vs desc, winningRate desc limit 10', str(request.GET.get("id")))
        columns = [col[0] for col in cursor.description]
        friends = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(data={'count':count,'friends':friends,'name':user.name})

def index(request):
    # プレイヤー情報を最終ログイン日時の新しい順に取得
    user = User.objects.filter(flag=0).order_by('-recent_login_at')
    return JsonResponse(data={'user':serializers.serialize("json", user)})

def ranking(request):
    # ID、氏名、総ポイント、勝利数を取得できるように直SQLにて取得する
    with connection.cursor() as cursor:
        cursor.execute('SELECT id, name,\
                        SUM(win_cpu*10+lose_cpu*(-5)+draw_cpu+win_friend*10+lose_friend*(-5)+draw_friend) AS point,\
                        SUM(win_count) AS winningCount\
                        FROM user WHERE flag = 0 GROUP BY name ORDER BY point DESC, winningCount DESC LIMIT 10')
        columns = [col[0] for col in cursor.description]
        ranking = [dict(zip(columns, row)) for row in cursor.fetchall()]
    # 10位分表示するために上記取得したrankingの件数の残分を空のレコード追加
    [ranking.append({'id': None, 'name': None, 'point': None, 'winningCount': None}) for i in range(10-len(ranking))]
    # フラグ取得
    flag = User.objects.filter(id=request.GET.get("id"))[0].flag
    return JsonResponse(data={'ranking':ranking, 'flag':flag})

def setting(request):
    # ID、氏名を対戦回数の多い順に取得
    with connection.cursor() as cursor:
        cursor.execute('SELECT id_to AS id, name\
                        FROM friend INNER JOIN user ON user.id = friend.id_to\
                        WHERE friend.id_from = %s ORDER BY vs DESC', str(request.GET.get("id")))
        columns = [col[0] for col in cursor.description]
        friends = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return JsonResponse(data={'friends':friends})

# ランキング情報取得するメソッド
def getRanking(request):
    if request.GET.get("id"):
        user = User.objects.filter(id=request.GET.get("id"))[0]
        # 直叩き対策(意図的にIDが変わった時の対策)
        if user:
            # プレイヤーのみ
            if not user.flag:
                # ポイント合算(計算上マイナスの場合0に変換)
                point = getScore(user)
                point = 0 if point <= 0 else point
                # ランク
                ranking = Ranking.objects.raw('SELECT * FROM ranking WHERE %i BETWEEN lower_limit and upper_limit' % point)[0].rank
                return JsonResponse(data={'ranking':ranking, 'point':point})
    return JsonResponse(data={'ranking':'', 'point':0})

# ポイント合算するメソッド(勝ち数×10、負け数×(-5)、引き分け数×1)
def getScore(user):
    return user.win_cpu * 10 + user.lose_cpu * (-5) + user.draw_cpu\
           + user.win_friend * 10 + user.lose_friend * (-5) + user.draw_friend