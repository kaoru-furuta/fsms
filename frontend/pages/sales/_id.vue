<template>
  <v-layout column>
    <h1>販売情報編集</h1>
    <v-form @submit.prevent="updateSale">
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
          <v-btn color="primary" type="submit">編集</v-btn>
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
  async asyncData({ store, route }) {
    const sale = await store.dispatch('sales/getSale', {
      id: route.params.id
    })

    const fruits = await store.dispatch('fruits/getFruits')

    return {
      fruit: sale.fruit,
      number: sale.number,
      amount: sale.amount,
      sold_at: store
        .$moment(sale.sold_at)
        .format(store.$moment.HTML5_FMT.DATETIME_LOCAL),
      fruits
    }
  },
  methods: {
    async updateSale() {
      try {
        await this.$store.dispatch('sales/updateSale', {
          id: this.$route.params.id,
          fruit: this.fruit,
          number: this.number,
          amount: this.amount,
          sold_at: this.sold_at
        })
        this.$store.commit('snackbar/set', {
          message: '編集しました'
        })
        this.$router.push({ name: 'sales' })
      } catch (e) {}
    }
  }
}
</script>
