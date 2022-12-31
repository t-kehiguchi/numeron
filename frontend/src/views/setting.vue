<template>
  <div class="setting">
    <p id="title">プレイ設定</p>
    <table style="margin:auto; width:75%; margin-bottom:25px;">
      <tr>
        <td style="width:40%; text-align:left;">プレイ選択</td>
        <td>
          <select id="playSelection" @change="onChange($event)">
            <option>CPU</option>
            <option>フレンド</option>
          </select>
        </td>
      </tr>
      <tr>
        <td style="text-align:left;">難易度(CPUのみ)</td>
        <td>
          <select id="difficulty">
            <option>易しい</option>
            <option>普通</option>
            <option>難しい</option>
          </select>
        </td>
      </tr>
      <tr>
        <td style="text-align:left;">フレンド</td>
        <td>
          <select id="selectedFriends" v-model="selectedFriends" disabled>
            <option v-for="friend in friends" v-bind:value="friend.id" v-bind:key="friend.id">{{ friend.name }} さん</option>
          </select>
        </td>
      </tr>
    </table>
    <div class="btn btn-primary" id="play" @click="play()">LET'S PLAY Numeron</div>
  </div>
</template>

<script>
export default {
  name: 'setting',
  data: function() {
    return {
      selectedFriends : '',
      friends         : [],
      onChange(e) {
        const difficulty = document.getElementById('difficulty');
        const friend = document.getElementById('selectedFriends');
        if(e.target.value == "フレンド") {
          // フレンドプルダウンは選択肢がある場合に活性化、ない場合はない旨を警告
          if(this.friends.length > 0) {
            friend.disabled = false;
          } else {
            alert('フレンドがいません。');
          }
          // 難易度プルダウンは非活性
          difficulty.disabled = true;
        } else {
          // フレンドプルダウンは非活性、難易度プルダウンは活性化
          difficulty.disabled = false;
          friend.disabled = true;
        }
      }
    }
  },
  created: function(){
    // フレンド情報(全件)取得
    this.$axios.get('http://localhost:8000/setting/',{params:{id:localStorage.getItem('id')}})
      .then(function(response){
        // フレンド(全件)情報
        this.friends = response.data['friends'];
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  methods: {
    play: function(){
      // プレイ選択
      var type = document.getElementById('playSelection').value;
      // オプション(難易度 or フレンドID)
      var option = type == "CPU" ? document.getElementById('difficulty').value : document.getElementById('selectedFriends').value;
      // フレンド選択でフレンドIDが指定なしの場合は選択し直す
      if(type == "フレンド" && !option) {
        alert('フレンド選択の場合はフレンドを選択してください。');
      } else {
        // プレイ画面へ遷移
        this.$router.push({path:'/play' + '/' + type + '/' + option});
      }
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

select {
  width: 90%;
}

#play {
  width: 80%;
  background-color: purple;
  font-style: italic;
  font-weight: 900;
}
</style>