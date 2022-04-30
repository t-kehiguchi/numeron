from django.db import models

class User(models.Model):
    id = models.CharField(verbose_name="ID", max_length=8, primary_key=True)
    name = models.CharField(verbose_name="氏名", max_length=50)
    email = models.CharField(verbose_name="メールアドレス", max_length=100, unique=True)
    win_cpu = models.IntegerField(verbose_name="勝ち数(CPU)", null=True, default=0)
    lose_cpu = models.IntegerField(verbose_name="負け数(CPU)", null=True, default=0)
    draw_cpu = models.IntegerField(verbose_name="引き分け数(CPU)", null=True, default=0)
    win_friend = models.IntegerField(verbose_name="勝ち数(フレンド)", null=True, default=0)
    lose_friend = models.IntegerField(verbose_name="負け数(フレンド)", null=True, default=0)
    draw_friend = models.IntegerField(verbose_name="引き分け数(フレンド)", null=True, default=0)
    flag = models.BooleanField(verbose_name="ユーザーフラグ", default=False)
    password = models.CharField(verbose_name="パスワード", max_length=50)
    recent_login_at = models.DateTimeField(verbose_name="最終ログイン日時", default='2022-01-01 00:00:00')
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        db_table = 'user'

class Ranking(models.Model):
    rank = models.CharField(verbose_name="ランク", primary_key=True, max_length=1)
    lower_limit = models.IntegerField(verbose_name="ポイント下限")
    upper_limit = models.IntegerField(verbose_name="ポイント上限")
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        db_table = 'ranking'

class Friend(models.Model):
    id_from = models.CharField(verbose_name="お気に入り元ID", max_length=8)
    id_to = models.CharField(verbose_name="お気に入り先ID", max_length=8)
    vs = models.IntegerField(verbose_name="対戦回数", default=0)
    created_at = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="更新日時", auto_now=True)

    class Meta:
        db_table = 'friend'
        constraints = [
            # id_fromとid_toでユニーク制約
            models.UniqueConstraint(fields=['id_from', 'id_to'], name='unique_stock')
        ]