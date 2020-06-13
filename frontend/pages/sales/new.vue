<template>
  <v-layout column>
    <h1>販売情報登録</h1>
    <v-form @submit.prevent="createSale">
      <v-row>
        <v-col cols="4">
          <v-select
            v-model="fruit"
            :items="fruits"
            :item-text="(item) => item.name"
            :item-value="(item) => item.id"
            label="果物"
          ></v-select>
        </v-col>
        <v-col cols="4">
          <v-text-field
            v-model="number"
            label="個数"
            type="number"
          ></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-text-field
            v-model="amount"
            label="売上"
            type="number"
          ></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-text-field
            v-model="sold_at"
            label="販売日時"
            type="datetime-local"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="primary" type="submit">登録</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="info" :to="{ name: 'sales' }">トップへ戻る</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-layout>
</template>

<script>
export default {
  components: {},
  data() {
    return {
      fruit: '',
      number: 0,
      amount: 0,
      sold_at: null
    }
  },
  async asyncData({ store }) {
    const fruits = await store.dispatch('fruits/getFruits')
    return { fruits }
  },
  methods: {
    async createSale() {
      try {
        await this.$store.dispatch('sales/createSale', {
          fruit: this.fruit,
          number: this.number,
          amount: this.amount,
          sold_at: this.sold_at
        })
        this.$store.commit('snackbar/set', {
          message: '登録しました'
        })
        await this.$router.push({ name: 'sales' })
      } catch (e) {}
    }
  }
}
</script>
