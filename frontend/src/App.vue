<template>
  <div id="app">
    <Header :login="login" :flag="flag" :user="user"/>
    <router-view/>
  </div>
</template>

<script>
import Header from '@/components/Header';

export default {
  name: 'App',
  components: {
    Header
  },
  data: function() {
    return {
      login : false,
      flag  : false,
      user  : null
    }
  },
  mounted: function(){
    this.$axios.get('http://localhost:8000/login/',{params:{id:localStorage.getItem('id')}})
      .then(function(response){
        if(response.data['login']){
          // UserオブジェクトをJSON化
          var obj = JSON.parse(response.data['user']);
          this.login = response.data['login'];
          this.flag = response.data['playerFlag'];
          this.user = obj[0]['fields'];
          // ログイン画面には遷移せずに詳細(一覧)画面へ遷移
          response.data['playerFlag'] ? this.$router.push('/detail/' + localStorage.getItem('id')) : this.$router.push('/index/' + localStorage.getItem('id'));
        } else {
          this.login = false;
        }
      }.bind(this))
      .finally(function(){
      }.bind(this))
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
