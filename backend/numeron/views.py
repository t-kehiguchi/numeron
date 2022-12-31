import json
import random
from datetime import datetime
from django.core import serializers
from django.db import connection
from django.http import JsonResponse
from django.http import HttpResponse
from numeron.models import Calling
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

# プレイ画面の初期設定
def play(request):
    # プレイヤーの答え
    player = getAnswer(int(request.GET.get("digit")))
    # CPU対戦
    if request.GET.get("playSelection") == "CPU":
        # CPUの答え
        # cpuがplayerと重複していたら再設定(未重複までループ)
        while True:
            cpu = getAnswer(int(request.GET.get("digit")))
            if player != cpu: break
        # プレイヤーに対するCPUコール情報生成(難易度によって異なる)
        cpuCallInfo = []
        # 易しい
        if request.GET.get("difficulty") == "易しい":
            # 1～8の中から6～8個を取得
            index = sorted(random.sample(list(range(1,9)), random.randint(6,8)))
        # 普通
        elif request.GET.get("difficulty") == "普通":
            # 1～8の中から4～6個を取得
            index = sorted(random.sample(list(range(1,9)), random.randint(4,6)))
        # 難しい
        elif request.GET.get("difficulty") == "難しい":
            # 4～8の中から2～4個を取得(level1～level3を除く)
            index = sorted(random.sample(list(range(4,9)), random.randint(2,4)))
        # 格納
        for i in range(0, len(index)):
            cpuCallInfo.append(getNumber(player, Calling.objects.filter(level=index[i])[0].call))
        # 最後はプレイヤーの答え(3EAT)
        cpuCallInfo.append(player)
        return JsonResponse(data={'answer':{'player':player, 'cpu':cpu, 'call':cpuCallInfo}})

# コール
def call(request):
    return JsonResponse(data={'result':callNumber(str(request.GET.get("answer")), str(request.GET.get("number")))})

# 対戦結果反映
def result(request):
    # プレイヤー情報
    player = User.objects.filter(id=request.GET.get("id"))
    # CPU対戦
    if request.GET.get("vs") == "cpu":
        win, win_count, lose, draw = player[0].win_cpu, player[0].win_count, player[0].lose_cpu, player[0].draw_cpu
        # 勝ち
        if request.GET.get("result") == "win":
            # 難易度によって加算するポイントが異なる(易しい:+1、普通:+2、難しい:+3)
            win = win + 1 if request.GET.get("difficulty") == "易しい" else win + 2 if request.GET.get("difficulty") == "普通" else win + 3
            # 勝ち数をインクリメント
            win_count = win_count + 1
        # 負け
        elif request.GET.get("result") == "lose":
            # 難易度によって加算するポイントが異なる(易しい:+3、普通:+2、難しい:+1)
            lose = lose + 3 if request.GET.get("difficulty") == "易しい" else lose + 2 if request.GET.get("difficulty") == "普通" else lose + 1
        # 引き分け(少なくともCPUが9ターン以内で決着するのであまり起きない)
        elif request.GET.get("result") == "draw":
            # 難易度によって加算するポイントが異なる(易しい:+1、普通:+2、難しい:+3)
            draw = draw + 1 if request.GET.get("difficulty") == "易しい" else draw + 2 if request.GET.get("difficulty") == "普通" else draw + 3
        # 一括更新
        msg = '対戦結果反映しました。' if player.update(win_cpu=win, win_count=win_count, lose_cpu=lose, draw_cpu=draw) == 1 else '対戦結果反映失敗しました。'
    return JsonResponse(data={'msg':msg})

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

# 0～9までのdigit桁までの重複なしデータ取得するメソッド
def getAnswer(digit):
    answer = ''
    while len(answer) < digit:
        number = str(random.randint(0, 9))
        answer = answer + number if not number in answer else answer
    return answer

# 与えたnumber(重複なしが前提)に対して「～EAT ～BITE」or「～EAT」をJSON形式で表示するメソッド
# 例1. callNumber('012', '104') → {'eat': 0, 'bite': 2}
# 例2. callNumber('456', '654') → {'eat': 1, 'bite': 2}
# 例3. callNumber('789', '789') → {'eat': 3}
def callNumber(answer, number):
    # 初期化
    eat, bite = 0, 0
    for i in range(0, len(number)):
        if number[i] in answer:
            (eat, bite) = (eat + 1, bite) if answer[i] == number[i] else (eat, bite + 1)
    return {'eat':eat} if bite == 0 and eat == len(answer) else {'eat':eat, 'bite':bite}

# answerから「～EAT ～BITE」に合うnumberを取得するメソッド
# 例1. getNumber('012', '1EAT 2BITE') → '021'
# 例2. getNumber('012', '0EAT 1BITE') → '426'
# 例3. getNumber('012', '0EAT 0BITE') → '837'
def getNumber(answer, call):
    # return値(answerの文字分空文字)とダミー
    number, tmp = [''] * len(answer), []
    # EATは先頭、BITEはスペースの直後の数字を求める
    eat, bite = int(call[0]), int(call[call.find(' ')+1])
    # answerの数字1文字ずつをダミーに入れる
    [tmp.append(answer[i]) for i in range(0, len(answer))]
    # まずは「0EAT 0BITE」
    if eat == 0 and bite == 0:
        # answerの数字以外の文字を求める
        other = list(set([str(i) for i in range(10)]) - set(tmp))
        # ランダムで無作為でanswerの文字数分求めて返す
        number = random.sample(other, len(answer))
    else:
        # まずはEAT
        # ランダムの数字(0～2)の昇順をEAT分入れる
        if eat > 0:
            temp = sorted(random.sample(list(range(0,len(answer))), eat))
            for i in range(0, len(temp)):
                number[temp[i]] = answer[temp[i]]
        # 次にBITE
        biteInfo = []
        # eat + bite = 1 → 「0EAT 1BITE」or「1EAT 0BITE」
        if (eat + bite) == 1:
            # 「0EAT 1BITE」
            if eat == 0 and bite == 1:
                for j in range(0, len(answer)):
                    if not number[j]:
                        biteInfo.append((j, answer[j]))
                select = biteInfo[random.randint(0, len(biteInfo)-1)]
                # select[0]以外のnumberの場所にselect[1]を入れる
                index = [0, 1, 2]
                index.remove(select[0])
                number[random.sample(index, bite)[0]] = select[1]
            # 残り2桁はその数以外のランダム
            other = random.sample(list(set([str(i) for i in range(10)]) - set(tmp)), 2)
            count = 0
            while number.count('') > 0:
                if not number[count]:
                    insert = random.sample(other, 1)[0]
                    number[count] = insert
                    # 重複を省く
                    other.remove(insert)
                count = count + 1
        # eat + bite = 2 → 「2EAT 0BITE」or「1EAT 1BITE」or「0EAT 2BITE」
        elif (eat + bite) == 2:
            # 「1EAT 1BITE」
            if eat == 1 and bite == 1:
                for j in range(0, len(answer)):
                    if not number[j]:
                        biteInfo.append((j, answer[j]))
                # 入れ替え
                exchange = []
                for k in range(0, len(biteInfo)):
                    exchange.append((biteInfo[k][0], biteInfo[len(biteInfo)-k-1][1]))
                select = exchange[random.randint(0, len(exchange)-1)]
                count = 0
                while number.count('') != 1:
                    if not number[count]:
                        if count == select[0]:
                            number[count] = str(select[1])
                    count = count + 1
            # 「0EAT 2BITE」
            elif eat == 0 and bite == 2:
                for j in range(0, len(answer)):
                    biteInfo.append(answer[j])
                # 念のためシャッフルした結果がシャッフルされていないことを考慮して
                biteInfo = random.sample(biteInfo, len(biteInfo))
                while tmp == biteInfo:
                    biteInfo = random.sample(biteInfo, len(biteInfo))
                count = 0
                while number.count('') != 1:
                    if answer[count] != biteInfo[count]:
                        number[count] = str(biteInfo[count])
                    count = count + 1
            # 残り1桁はその数以外のランダム
            for j in range(0, len(answer)):
                if not number[j]:
                    number[j] = random.sample(list(set([str(i) for i in range(10)]) - set(tmp) - set(number)), 1)[0]
        # eat + bite = 3 → 「0EAT 3BITE」or「1EAT 2BITE」
        elif (eat + bite) == 3:
            # 「1EAT 2BITE」
            if eat == 1 and bite == 2:
                for j in range(0, len(answer)):
                    if not number[j]:
                        biteInfo.append(answer[j])
                count = 0
                while number.count('') > 0:
                    if not number[count]:
                        for k in range(0, len(biteInfo)):
                            if answer[count] == biteInfo[k]:
                                number[count] = biteInfo[len(biteInfo)-k-1]
                            else:
                                number[count] = biteInfo[k]
                    count = count + 1
            # 「0EAT 3BITE」
            else:
                flag = False
                # 012 → 102 のようになるケースもあるため、try-except節を設ける
                while not flag:
                    try:
                        for k in range(0, len(tmp)):
                            number[k] = random.sample(list(filter(lambda x : x not in answer[k], list(set(tmp) - set(number)))), 1)[0]
                            flag = True
                    except ValueError as e:
                        number.clear
                        flag = False
    return ''.join(number)