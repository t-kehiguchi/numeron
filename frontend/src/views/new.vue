<template>
  <div class="new">
    <div class="margin">
      <div class="row">
        <div class="col-md-6 col-md-offset-3">
          <p id="label" style="font-weight:boid; color:red;">※ 全て必須</p>
          <p id="label" style="clear:both;">ID</p>
          <p id="id">{{id}}</p>
          <p id="label">名前</p>
          <input type="name" v-model="name" class="form-control">
          <p id="label">メールアドレス</p>
          <input type="email" v-model="email" class="form-control">
          <p id="label">パスワード</p>
          <input type="password" v-model="password" class="form-control">
          <p id="label">パスワード確認</p>
          <input type="password" v-model="passwordConfirm" class="form-control">
          <div class="btn" @click="createPlayer()">新規作成</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'new',
  data: function() {
    return {
      id              : '',
      name            : '',
      email           : '',
      password        : '',
      passwordConfirm : ''
    }
  },
  created: function() {
    this.$axios.get('http://localhost:8000/new/')
      .then(function(response){
        this.id = response.data['id'];
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  methods: {
    createPlayer:function() {
      var inputFlag = true;
      // 入力されているか
      if(this.nullCheck(this.name, this.email, this.password, this.passwordConfirm)) {
        // 正しくメールアドレス入力しているか
        if(!this.emailCheck(this.email)) {
          inputFlag = false;
          alert('メールアドレス形式で入力してください');
        }
        // パスワードとパスワード確認が一致しているか
        if(this.password != this.passwordConfirm) {
          inputFlag = false;
          alert('パスワードとパスワード確認は一致してください');
        }
      } else {
        inputFlag = false;
      }
      if(inputFlag) {
        // 呼び出す
        this.$axios.post('http://localhost:8000/new/',{
            id       : this.id,
            name     : this.name,
            email    : this.email,
            password : this.password
        })
        .then(function(response){
          alert(response.data['msg']);
          if(response.data['flag']) {
            // 成功したらログイン画面へ遷移
            this.$router.push('/');
          } else {
            this.reset();
          }
        }.bind(this))
        .finally(function(){
        }.bind(this));
      } else {
        this.reset();
      }
    },
    nullCheck:function(name, email, password, passwordConfirm) {
      var flag = true;
      // 氏名
      if(!name) {
        alert('名前は必須です。');
        flag = false;
      }
      // メールアドレス
      if(!email) {
        alert('メールアドレスは必須です。');
        flag = false;
      }
      // パスワード(パスワード確認)
      if(!password || !passwordConfirm) {
        var msg = !password && passwordConfirm ? 'パスワード' : password && !passwordConfirm ? 'パスワード確認' : 'パスワードとパスワード確認';
        alert(msg + 'は必須です。');
        flag = false;
      }
      return flag;
    },
    emailCheck:function(email) {
      var re = /^[a-zA-Z0-9_.+-]+@([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$/i;
      return re.test(email);
    },
    reset:function() {
      this.name = '';
      this.email = '';
      this.password = '';
      this.passwordConfirm = '';
    }
  }
}
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

#id {
  clear: both;
  display: flex;
  font-size: x-large;
  font-weight: bold;
}

.btn {
  width: 100%;
  margin-top: 25px;
  margin-bottom: 25px;
  color: #000;
  background-color: #FFFF00;
  border-color: #FFFF00;
}
</style>