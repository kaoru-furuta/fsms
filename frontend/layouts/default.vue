<template>
  <v-app>
    <v-app-bar app elevation="1" color="teal lighten-3">
      <nuxt-link :to="{ name: 'index' }" class="title">
        <v-toolbar-title>
          {{ title }}
        </v-toolbar-title>
      </nuxt-link>
      <v-spacer />
      <v-btn
        v-if="$store.state.accounts.isAuthenticated"
        depressed
        dark
        color="teal lighten-3"
        @click="logout"
      >
        ログアウト
      </v-btn>
    </v-app-bar>
    <v-content>
      <v-container class="pt-5">
        <nuxt />
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
export default {
  comments: {},
  data() {
    return {
      title: '果物管理システム'
    }
  },
  methods: {
    async logout() {
      try {
        await this.$store.dispatch('accounts/logout')
        this.$router.push({ name: 'login' })
      } catch (e) {}
    }
  }
}
</script>

<style lang="stylus" scoped>
.title {
  text-decoration: none;
  color: white;

  :hover {
    opacity: 0.8;
  }
}
</style>
