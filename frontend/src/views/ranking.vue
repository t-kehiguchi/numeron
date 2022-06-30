<template>
  <div class="ranking">
    <p id="title">ランキング(トップ10)</p>
    <div v-if="ranking">
      <table id="ranking" class="table-bordered table-condensed" style="margin:auto; width:90%;">
        <thead>
          <tr style="background-color:#ebebeb;">
            <th>順位</th>
            <th>プレイヤー名</th>
            <th>ポイント</th>
            <th>勝利数</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(rank, index) in ranking" :key="rank.pk" v-bind:id="id === rank['id'] ? 'myRank' : ''">
            <td>
              {{rank['id'] != null && index > 0 ? (ranking[index-1]['point'] == ranking[index]['point'] && ranking[index-1]['winningCount'] == ranking[index]['winningCount'] ? index : index+1) : index+1}}
            </td>
            <td style="width:60%; word-break:keep-all;">
              <a v-if="flag" v-bind:href="'detail/' + rank['id']">{{rank['id'] != null ? rank['name'] + ' さん' : ''}}</a>
              <p v-else style="margin:0px;">{{rank['id'] != null ? rank['name'] + ' さん' : ''}}</p>
            </td>
            <td>
              {{rank['point']}}
            </td>
            <td>
              {{rank['winningCount']}}
            </td>            
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>プレイヤーが存在しません。</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ranking',
  data: function() {
    return {
      ranking : [],
      flag    : false,
      id      : localStorage.getItem('id'),
    }
  },
  created: function(){
    // 全プレイヤー取得
    this.$axios.get('http://localhost:8000/ranking/',{params:{id:localStorage.getItem('id')}})
      .then(function(response){
        this.ranking = response.data['ranking'];
        this.flag = response.data['flag'];
      }.bind(this))
      .finally(function(){
        // ランキング表の行(tbody部)を取得
        var rowElems = document.getElementById('ranking').children[1].getElementsByTagName('tr');
        // 10行ループし、id指定がない場合のみid自体を削除する
        for (var i = 0, len = rowElems.length; i < len; i++) {
          if(!rowElems[i].getAttribute("id")) rowElems[i].removeAttribute("id");
        }
      }.bind(this))
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

#myRank {
  color: #0b62b0;
  background-color: #cee8ff;
  font-weight: bold;
}
</style>