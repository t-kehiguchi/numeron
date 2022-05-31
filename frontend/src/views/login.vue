<template>
  <div class="login">
    <div class="margin">
      <div class="row">
        <div class="col-md-6 col-md-offset-3">
          <p id="label">メールアドレス</p>
          <input type="email" v-model="email" class="form-control">
          <p id="label">パスワード</p>
          <input type="password" v-model="password" class="form-control">
          <br>
          <div>
            <div class="btn btn-primary" @click="execLogin()">ログイン</div>
            <br>
            <a href="/new" id="link" style="margin-top:15px; clear:both;">プレイヤー新規</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'login',
  data: function() {
    return {
      email     : '',
      password  : ''
    }
  },
  methods: {
    execLogin:function(){
      var inputFlag = true;
      // 入力されているか
      if(this.nullCheck(this.email, this.password)) {
        // 正しくメールアドレス入力しているか
        if(!this.emailCheck(this.email)) {
          inputFlag = false;
          alert('メールアドレス形式で入力してください');
        }
      } else {
        inputFlag = false;
      }
      if(inputFlag) {
        // 呼び出す
        this.$axios.post('http://localhost:8000/login/',{
            email    : this.email,
            password : this.password
        })
        .then(function(response){
          if(response.data['flag']) {
            // UserオブジェクトをJSON化
            var obj = JSON.parse(response.data['user']);
            // idをセッション保持
            localStorage.setItem('id', obj[0]['pk']);
            // 成功したら詳細(一覧)画面へ遷移
            obj[0]['fields']['flag'] ? this.$router.push('/index/') : this.$router.push('/detail/' + obj[0]['pk']);
            // 強制的にApp.vueのloginのGETメソッドを呼び出す
            this.$router.go({path: process.env.BASE_URL, force: true});
          } else {
            alert(response.data['msg']);
          }
        }.bind(this))
        .finally(function(){
        }.bind(this));
      }
    },
    nullCheck:function(email, password) {
      var flag = true;
      // メールアドレス
      if(!email) {
        alert('メールアドレスは必須です。');
        flag = false;
      }
      // パスワード
      if(!password) {
        alert('パスワードは必須です。');
        flag = false;
      }
      return flag;
    },
    emailCheck:function(email) {
      var re = /^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/i;
      return re.test(email);
    }
  }
};
</script>

<style scoped>
.margin {
  margin-left: 50px;
  margin-right: 50px;
}

#label {
  float: left;
  margin-top: 10px;
  margin-bottom: 10px;
}

.btn, #link {
  float: right;
}
</style>