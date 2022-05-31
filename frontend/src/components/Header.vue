<template>
  <div class="header">
    <header>
      <a href="/" id="logo">Numeron</a>
      <div v-if="login" id="button" style="float:right;">
        <div v-show="flag" class="btn btn-danger">プレイ</div>
        <div class="btn btn-warning">ランキング</div>
        <div class="btn btn-primary" @click="execLogout()">ログアウト</div>
      </div>
      <div id="inline" v-if="login">
        <p id="hello" style="float:left; clear:both;">ようこそ {{user.name}} さん</p>
        <p v-show="flag" style="float:right;">ランク : {{ranking}} (ポイント : {{point}})</p>
        <p style="float:right; clear:both;">最終ログイン : {{moment(user.recent_login_at)}}</p>
      </div>
    </header>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'Header',
  props: ['login', 'flag', 'user'],
  data: function() {
    return {
      ranking : '',
      point   : 0
    }
  },
  mounted: function() {
    this.$axios.get('http://localhost:8000/getRanking/',{params:{id:localStorage.getItem('id')}})
      .then(function(response){
        this.ranking = response.data['ranking'];
        this.point = response.data['point'];
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  methods: {
    execLogout: function(){
      // セッションを削除(クリア)
      localStorage.clear();
      // ログイン画面へ遷移
      this.$router.push('/');
      // 強制的にApp.vueのloginのGETメソッドを呼び出す
      this.$router.go({path: process.env.BASE_URL, force: true});
    },
    moment:function(date) {
      // 日本語対応
      moment.locale('ja');
      return moment(date).format('YYYY年MM月DD日(dd) HH:mm:ss')
    }
  }
}
</script>

<style scoped>
.header {
  width: 485px;
  display: inline-block;
}

div.btn {
  margin-top: 9px;
  margin-right: 10px;
}

#button button {
  margin-top: 38px;
  margin-right: 10px;
}

#logo {
  float: left;
  margin-left: 15px;
  font-size: 1.5em;
  color: #000;
  text-decoration: none;
  letter-spacing: -1px;
  padding-top: 9px;
  font-weight: bold;
  font-style: italic;
  font-family: auto;
}

#inline {
  display: inline-grid;
  float: right;
  text-align: end;
  margin-top: 10px;
}

#inline > p {
  margin-bottom: 10px;
}
</style>