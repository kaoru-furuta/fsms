<template>
  <v-layout column>
    <h1>果物編集</h1>
    <v-form @submit.prevent="updateFruit">
      <v-row>
        <v-col cols="4">
          <v-text-field v-model="name" label="名称"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-text-field v-model="price" label="価格"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-file-input @change="onImageChange" label="画像" />
          <span>{{ imageName }}</span>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="primary" type="submit">編集</v-btn>
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
  async asyncData({ store, route }) {
    const fruit = await store.dispatch('fruits/getFruit', {
      id: route.params.id
    })
    return {
      name: fruit.name,
      price: fruit.price,
      image: '',
      imageName: fruit.image_name
    }
  },
  methods: {
    async updateFruit() {
      try {
        await this.$store.dispatch('fruits/updateFruit', {
          id: this.$route.params.id,
          name: this.name,
          price: this.price,
          image: this.image
        })
        this.$store.commit('snackbar/set', {
          message: '編集しました'
        })
        this.$router.push({ name: 'fruits' })
      } catch (e) {}
    },
    onImageChange(image) {
      this.image = image
    }
  }
}
</script>
