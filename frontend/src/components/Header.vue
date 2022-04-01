<template>
  <div class="header">
    <header>
      <p id="logo">Numeron</p>
      <div v-if="login" id="button" style="float:right;">
        <div class="btn btn-danger">プレイ</div>
        <div class="btn btn-warning">ランキング</div>
        <div class="btn btn-primary">ログアウト</div>
      </div>
    </header>
  </div>
</template>

<script>
export default {
  name: 'Header',
  props: ['login']
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
</style>