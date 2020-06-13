<template>
  <v-layout column>
    <h1>販売情報管理</h1>
    <form action method="get">
      <v-row>
        <v-col cols="4">
          <v-text-field label="果物" hide-details="auto"></v-text-field>
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
    <v-data-table :headers="headers" :items="sales" :items-per-page="5">
      <template v-slot:item.sold_at="{ item }">{{
        $moment(item.sold_at).format('YYYY/MM/DD HH:mm')
      }}</template>
      <template v-slot:item.id="{ item }">
        <v-btn
          :to="{ name: 'sales-id', params: { id: item.id } }"
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
        <v-btn color="primary" :to="{ name: 'sales-new' }">新規登録</v-btn>
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
  async asyncData({ store }) {
    const sales = await store.dispatch('sales/getSales')
    return { sales }
  },
  data() {
    return {
      headers: [
        { text: '果物', value: 'fruit_name', width: '20%' },
        { text: '個数', value: 'number', width: '20%' },
        { text: '売上', value: 'amount', width: '20%' },
        { text: '販売日時', value: 'sold_at', width: '20%' },
        { text: '操作', value: 'id', width: '20%' }
      ]
    }
  },
  mounted() {
    this.$refs.snackbar.open()
  }
}
</script>
