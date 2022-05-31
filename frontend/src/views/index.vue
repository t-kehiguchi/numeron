<template>
  <div class="index">
    <p id="title">プレイヤー一覧(最近ログインしたプレイヤーの降順)</p>
    <div v-if="users">
      <table class="table-bordered table-condensed" style="margin:auto; width:90%;">
        <thead>
          <tr style="background-color:#ebebeb;">
            <th style="width:30%;">プレイヤー名</th>
            <th style="width:10%;">勝</th>
            <th style="width:10%;">負</th>
            <th style="width:50%;">最終ログイン</th>
          </tr>
        </thead>
        <tbody style="height:250px; width:90%; overflow-y:scroll; position:absolute;">
          <tr v-for="user in users" :key="user.pk">
            <td style="width:30%; word-break:keep-all;"><a @click="transition(user.pk)" class="transition">{{user['fields']['name']}} さん</a></td>
            <td style="width:10%;">{{user['fields']['win_cpu'] + user['fields']['win_friend']}}</td>
            <td style="width:10%;">{{user['fields']['lose_cpu'] + user['fields']['lose_friend']}}</td>
            <td style="width:50%;">{{moment(user['fields']['recent_login_at'])}}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>ユーザーが存在しません。</p>
    </div>
  </div>
</template>

<script>
import moment from 'moment';

export default {
  name: 'index',
  data: function() {
    return {
      users : []
    }
  },
  created: function(){
    // 全プレイヤー取得
    this.$axios.get('http://localhost:8000/index/')
      .then(function(response){
        // UserオブジェクトをJSON化
        var obj = JSON.parse(response.data['user']);
        this.users = obj;
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  methods: {
    moment:function(date) {
      // 日本語対応
      moment.locale('ja');
      return moment(date).format('YYYY年MM月DD日(dd) HH:mm:ss')
    },
    transition:function(id) {
      this.$router.push({path:'/detail' + '/' + id});
    }
  }
}
</script>

<style>
#title {
  font-size: large;
  text-align: left;
  margin: 0px;
  padding-left: 10px;
  padding-bottom: 10px;
}
</style>