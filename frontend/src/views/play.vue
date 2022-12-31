<template>
  <div class="play">
    <p id="title">プレイ</p>
    <div style="float:left; padding-left:40px; text-align:left; margin-bottom:20px;">
      <li>タイプ : {{$route.params.type}}</li>
      <li v-if="$route.params.type=='CPU'">難易度 : {{$route.params.option}}</li>
      <li v-if="$route.params.type=='フレンド'">フレンド : {{$route.params.option}}</li>
      <li v-if="$route.params.type=='CPU'">プレイヤーの答え : {{playerInfo['answer']}}</li>
    </div>
    <div>
      <p>残り {{countdown}} 秒</p>
      <p style="margin-bottom:5px; color:red; font-size:x-small; font-weight:700;">コールした数字と異なる3桁の数字を入れてね</p>
      <input type="text" maxlength="3" oninput="value = value.replace(/[^0-9]+/i,'');" id="calling">
      <input type="button" value="コール" style="margin-left:10px; margin-bottom:10px;" id="call" @click="execCall()">
    </div>
    <div id="left">
      <div>
        <p style="text-align: left; margin-left: 25px;">プレイヤー</p>
        <table id="myCall" style="display:none; margin:auto 25px;">
          <tbody id="myCallBody"></tbody>
        </table>
      </div>
    </div>
    <div class="border"></div>
    <div id="right" style="float:right; width:50%;">
        <p v-if="$route.params.type=='CPU'" style="text-align: left; margin-left: 25px;">CPU</p>
        <table id="cpuCall" style="display:none; margin:auto 25px;">
          <tbody id="cpuCallBody"></tbody>
        </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'play',
  data: function() {
    return {
      playerInfo : {
        answer     : '',
        call       : '',
        callCount  : 0,
        innerHtml  : ''
      },
      cpuInfo    : {
        answer     : '',
        call       : '',
        callInfo   : [],
        callCount  : 0,
        innerHtml  : ''
      },
      timer       : null,
      countdown   : 0,
      defailtTime : 0, // タイマーとは別に保持するための変数
      turn        : null, // true : プレイヤー、false : CPU
      callResult  : '', // 毎回上書きされる(3EATになるかを確認するために使用)
      result      : null // 「勝ち : 0、負け : 1、引き分け : 2」
    }
  },
  created: function(){
    // 初期設定
    // タイマー設定
    this.countdown = this.$route.params.option == '易しい' ? 50 : this.$route.params.option == '普通' ? 35 : 15;
    this.defailtTime = this.countdown;
    this.$axios.get('http://localhost:8000/play/',
                    {
                      params : {
                        digit : 3, // デフォルトは3桁
                        playSelection : this.$route.params.type,
                        difficulty : this.$route.params.option
                      }
                    })
      .then(function(response){
        // お互いの答え
        this.playerInfo['answer'] = response.data['answer']['player'];
        this.cpuInfo['answer'] = response.data['answer']['cpu'];
        // CPUのコール情報(最初から分かっている)
        this.cpuInfo['callInfo'] = response.data['answer']['call'];
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  computed: {
    target: function() {
      return [this.callResult, this.turn]
    }
  },
  watch: {
    countdown: function() {
      // すでにタイマー設定している場合は止めて再設定する
      if(this.timer) clearTimeout(this.timer);
      this.timer = setTimeout(this.getCountdown, 1000);
      // タイムアップの場合はプレイヤーの負け決定(CPUは必ずタイムアップにはならない)
      if(this.countdown == 0) {
        // アラーム出す前にタイマー止める
        clearTimeout(this.timer);
        alert(this.defailtTime + '秒過ぎたのであなたの負けです。');
        this.result = '1'; // 負け
      }
    },
    target: async function() {
      if(this.callResult == '3EAT !!!!!') {
        if(this.turn) {
          alert('あなたの勝ちです。');
          this.result = '0';
        } else if(this.turn == false) {
          alert('あなたの負けです。');
          this.result = '1';
        }
      }
    },
    turn: async function() {
      if(this.turn == true) {
        if(!this.result) {
          alert('あなたのターンです。');
          this.countdown = this.defailtTime;
          // テキストを入力可能にする
          document.getElementById('calling').removeAttribute("disabled");
          //「コール」ボタンも押せるようにする
          document.getElementById('call').removeAttribute("disabled");
        }
      } else if(this.turn == false) {
        if(!this.result) {
          alert('CPUのターンです。');
          this.countdown = this.defailtTime;
          var sleepTime = this.getSleepTime(this.$route.params.option);
          await this.sleep(sleepTime * 1000);
          this.execCall();
        }
      }
      // ターン回した後は一旦nullにする(毎度alertが出ないように)
      this.turn = null;
    },
    result: function() {
      this.$axios.get('http://localhost:8000/result/',
                      {
                        params : {
                          id         : localStorage.getItem('id'),
                          vs         : "cpu",
                          difficulty : this.$route.params.option,
                          result     : this.result == '0' ? "win" : this.result == '1' ? "lose" : "draw"
                        }
                      })
      .then(function(response){
        alert(response.data['msg']);
      }.bind(this))
      .finally(function(){
      }.bind(this))
      // 「プレイヤー詳細」画面へ遷移
      this.$router.push('/detail/' + localStorage.getItem('id'));
      // 強制的にdetail.vueのdetailのGETメソッドを呼び出す
      this.$router.go({path: process.env.BASE_URL, force: true});
    }
  },
  methods: {
    execCall: function(){
      var number = document.getElementById('calling').value;
      if(number) {
        // プレイヤーのコール
        var check = this.numberCheck(number, 3);
        // 入力チェック
        if(!check['result']) {
          alert(check['msg']);
        }
        this.$axios.get('http://localhost:8000/call/',{params:{answer:this.cpuInfo['answer'], number:number}})
          .then(function(response){
            this.playerInfo['callCount']++;
            // 初回コールのみコール行を表示
            if(this.playerInfo['callCount'] == 1) {
              var row = document.getElementById("myCall");
              row.style.display = '';
            }
            // コールしたナンバーを保持
            this.playerInfo['call'] = number;
            var tmp = response.data['result'];
            this.callResult = tmp['bite'] == null ? tmp['eat'] + 'EAT !!!!!' : tmp['eat'] + 'EAT ' + tmp['bite'] + 'BITE';
            var temp = this.getText(this.playerInfo['callCount'], number, this.callResult);
            this.playerInfo['innerHtml'] = this.playerInfo['innerHtml'] + temp;
            var newRow = document.getElementById("myCallBody");
            newRow.innerHTML = this.playerInfo['innerHtml'];
            // コール(結果3EAT以外)したらCPUのターン(false)へ渡す
            // 3EATの場合はコールしたプレイヤーのターン(true)へ渡す
            this.turn = this.callResult != '3EAT !!!!!' ? false : true;
            // 入力したテキストをクリアし、入力不可にする
            document.getElementById('calling').value = '';
            document.getElementById('calling').setAttribute("disabled", true);
            //「コール」ボタンも押せないようにする
            document.getElementById('call').setAttribute("disabled", true);
          }.bind(this))
          .finally(function(){
          }.bind(this))
      } else {
        // CPUのコール
        this.$axios.get('http://localhost:8000/call/',{params:{answer:this.playerInfo['answer'], number:this.cpuInfo['callInfo'][this.cpuInfo['callCount']]}})
          .then(function(response){
            this.cpuInfo['callCount']++;
            // 初回コールのみコール行を表示
            if(this.cpuInfo['callCount'] == 1) {
              var row = document.getElementById("cpuCall");
              row.style.display = '';
            }
            // コールしたナンバーを保持
            this.cpuInfo['call'] = this.cpuInfo[this.callCount];
            var tmp = response.data['result'];
            this.callResult = tmp['bite'] == null ? tmp['eat'] + 'EAT !!!!!' : tmp['eat'] + 'EAT ' + tmp['bite'] + 'BITE';
            var temp = this.getText(this.cpuInfo['callCount'], this.cpuInfo['callInfo'][this.cpuInfo['callCount']-1], this.callResult);
            this.cpuInfo['innerHtml'] = this.cpuInfo['innerHtml'] + temp;
            var newRow = document.getElementById("cpuCallBody");
            newRow.innerHTML = this.cpuInfo['innerHtml'];
            // コール(結果3EAT以外)したらプレイヤーのターン(true)へ渡す
            // 3EATの場合はコールしたCPUのターン(false)へ渡す
            this.turn = this.callResult != '3EAT !!!!!' ? true : false;
          }.bind(this))
          .finally(function(){
          }.bind(this))
      }
    },
    numberCheck: function(number, digit){
      if(number.length != digit) {
        return {"result":false, "msg":digit+"桁で入力してね"};
      }
      var s = new Set(number);
      if(s.size != number.length) {
        return {"result":false, "msg":"重複ダメ"};
      }
      return {"result":true};
    },
    getText: function(count, number, result){
      return '<tr><li>' + count + '回目のコール' + '</li></tr>' +
             '<p style="margin-left:25px; margin-bottom:0px;">' + number + ' → ' + result + '</p>';
    },
    getCountdown: function(){
      this.countdown--;
    },
    sleep: function(time){
      return new Promise(resolve => setTimeout(resolve, time));
    },
    getSleepTime: function(difficulty){
      // 難易度によってターンごとに変わる
      if(difficulty == '易しい') {
        return this.getRandomIntInclusive(20,30); // 20～30秒
      } else if(difficulty == '普通') {
        return this.getRandomIntInclusive(10,20); // 10～20秒
      } else {
        return this.getRandomIntInclusive(5,10); // 5～10秒
      }
    },
    getRandomIntInclusive: function(min, max){
      min = Math.ceil(min);
      max = Math.floor(max);
      return Math.floor(Math.random() * (max - min + 1) + min);
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
#calling {
  width: 25%;
}
#left {
  clear: both;
  float: left;
  width: 50%;
}
.border {
  position: absolute;
  left: 50%;
  background:#000000;
  width: 2.5px;
  height: 75%;
  margin-top: 5px;
}
</style>