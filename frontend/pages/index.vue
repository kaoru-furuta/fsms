<template>
  <v-layout column>
    <h1>管理 TOP</h1>
    <v-row>
      <v-col cols="4">
        <v-btn :to="{ name: 'fruits' }">果物マスタ管理</v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn :to="{ name: 'sales' }">販売情報管理</v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn :to="{ name: '' }">販売統計情報</v-btn>
      </v-col>
    </v-row>

    <snackbar ref="snackbar" />
  </v-layout>
</template>

<script>
import Snackbar from '~~/components/Snackbar'

export default {
  components: {
    Snackbar
  },
  mounted() {
    this.$refs.snackbar.open()
  }
}
</script>
