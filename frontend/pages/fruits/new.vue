<template>
  <v-layout column>
    <h1>果物登録</h1>
    <v-form @submit.prevent="createFruit">
      <v-row>
        <v-col cols="4">
          <v-text-field v-model="name" label="名称"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-text-field v-model="price" label="価格"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-file-input @change="onImageChange" label="画像" />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="primary" type="submit">登録</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="info" :to="{ name: 'fruits' }">トップへ戻る</v-btn>
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
      name: '',
      price: null,
      image: ''
    }
  },
  methods: {
    async createFruit() {
      try {
        await this.$store.dispatch('fruits/createFruit', {
          name: this.name,
          price: this.price,
          image: this.image
        })
        this.$store.commit('snackbar/set', {
          message: '登録しました'
        })
        await this.$router.push({ name: 'fruits' })
      } catch (e) {}
    },
    onImageChange(image) {
      this.image = image
    }
  }
}
</script>
