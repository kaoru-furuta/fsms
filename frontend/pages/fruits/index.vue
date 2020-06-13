<template>
  <v-layout column>
    <h1>果物マスタ管理</h1>
    <form action method="get">
      <v-row>
        <v-col cols="4">
          <v-text-field label="名称" hide-details="auto"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="primary">
            検索
            <v-icon right>mdi-magnify</v-icon>
          </v-btn>
        </v-col>
      </v-row>
    </form>
    <v-data-table :headers="headers" :items="fruits" :items-per-page="5">
      <template v-slot:item.created_at="{ item }">{{
        $moment(item.created_at).format('YYYY/MM/DD HH:mm')
      }}</template>
      <template v-slot:item.updated_at="{ item }">{{
        $moment(item.updated_at).format('YYYY/MM/DD HH:mm')
      }}</template>
      <template v-slot:item.id="{ item }">
        <v-btn
          :to="{ name: 'fruits-id', params: { id: item.id } }"
          fab
          small
          depressed
          outlined
          color="primary"
        >
          <v-icon small>mdi-pencil</v-icon>
        </v-btn>
      </template>
    </v-data-table>
    <v-row>
      <v-col>
        <v-btn color="primary" :to="{ name: 'fruits-new' }">新規登録</v-btn>
      </v-col>
    </v-row>

    <snackbar ref="snackbar" />
  </v-layout>
</template>

<script>
import Snackbar from '~/components/Snackbar'

export default {
  components: {
    Snackbar
  },
  async asyncData({ store }) {
    const fruits = await store.dispatch('fruits/getFruits')
    return { fruits }
  },
  data() {
    return {
      headers: [
        { text: '名称', value: 'name', width: '20%' },
        { text: '価格', value: 'price', width: '20%' },
        { text: '登録日時', value: 'created_at', width: '20%' },
        { text: '更新日時', value: 'updated_at', width: '20%' },
        { text: '操作', value: 'id', width: '20%' }
      ]
    }
  },
  mounted() {
    this.$refs.snackbar.open()
  }
}
</script>
