<template>
  <div class="detail">
    <div v-if="session !== param">
      <p id="title">{{name}} さんの情報</p>
    </div>
    <div style="float:left; width:40%;">
      <li>プレイヤー情報</li>
      <p style="margin-top:10px; padding-left:50px; text-align:left;">CPU対戦</p>
      <p style="text-indent:25%;">勝利数&nbsp;&nbsp;&nbsp;&nbsp;{{count['cpu']['win']}}回</p>
      <p style="text-indent:25%;">敗北数&nbsp;&nbsp;&nbsp;&nbsp;{{count['cpu']['lose']}}回</p>
      <p style="text-indent:25%;">引分数&nbsp;&nbsp;&nbsp;&nbsp;{{count['cpu']['draw']}}回</p>
      <p style="margin-top:10px; padding-left:50px; text-align:left;">フレンド対戦</p>
      <p style="text-indent:25%;">勝利数&nbsp;&nbsp;&nbsp;&nbsp;{{count['friend']['win']}}回</p>
      <p style="text-indent:25%;">敗北数&nbsp;&nbsp;&nbsp;&nbsp;{{count['friend']['lose']}}回</p>
      <p style="text-indent:25%;">引分数&nbsp;&nbsp;&nbsp;&nbsp;{{count['friend']['draw']}}回</p>
    </div>
    <li style="text-align:left; margin-bottom:10px;">フレンド(上位10件)</li>
    <div v-if="friends.length !== 0" style="float:right; width:60%;">
      <table class="table-bordered table-condensed" style="margin:auto; width:80%;">
        <thead>
          <tr style="background-color:#ebebeb;">
            <th style="word-break:keep-all;">プレイヤー名</th>
            <th>対戦回数</th>
            <th>勝率(%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="friend in friends" :key="friend.pk">
            <td style="width:60%; word-break:break-all;">
              <a @click="transition(friend['id_to'])" class="transition">{{friend['name']}} さん</a>
            </td>
            <td style="width:20%;">
              {{friend['vs']}}
            </td>
            <td style="width:20%;">
              {{friend['winningRate']}}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>フレンド情報がありません。</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'detail',
  data: function() {
    return {
      count   : {
        cpu : {
          win  : 0,
          lose : 0,
          draw : 0
        },
        friend : {
          win  : 0,
          lose : 0,
          draw : 0
        }
      },
      friends : [],
      name    : '',
      session : localStorage.getItem('id'),
      param   : this.$route.params.id
    }
  },
  watch: {
    $route() {
      location.reload();
    }
  },
  created: function(){
    // プレイヤー情報取得
    this.$axios.get('http://localhost:8000/detail/',{params:{id:this.$route.params.id}})
      .then(function(response){
        // 対戦回数
        this.count = response.data['count'];
        // フレンド情報
        this.friends = response.data['friends'];
        this.name = response.data['name'];
      }.bind(this))
      .finally(function(){
      }.bind(this))
  },
  methods: {
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
  padding-left: 15px;
  padding-bottom: 15px;
}
</style>