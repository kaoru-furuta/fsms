<template>
  <v-layout column>
    <h1>ログイン</h1>
    <v-form @submit.prevent="login">
      <v-row>
        <v-col cols="4">
          <v-text-field v-model="username" label="ユーザー名"></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-text-field
            v-model="password"
            label="パスワード"
            type="password"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="4">
          <v-btn color="primary" type="submit">ログイン</v-btn>
        </v-col>
      </v-row>
    </v-form>
  </v-layout>
</template> 

<script>
export default {
  auth: false,

  components: {},

  data() {
    return {
      username: '',
      password: ''
    }
  },

  methods: {
    async login() {
      try {
        await this.$store.dispatch('accounts/login', {
          username: this.username,
          password: this.password
        })
        this.$store.commit('snackbar/set', {
          message: 'ログインしました'
        })
        this.$router.push({ name: 'index' })
      } catch (e) {}
    }
  }
}
</script>
