<template>
  <v-snackbar
    v-model="snackbar"
    :color="color"
    :timeout="timeout"
    top
    absolute
    >{{ message }}</v-snackbar
  >
</template>

<script>
export default {
  data() {
    return {
      snackbar: false,
      message: '',
      color: '',
      timeout: 0
    }
  },

  methods: {
    open() {
      if (this.$store.state.snackbar.message) {
        this.message = this.$store.state.snackbar.message
        this.color = this.$store.state.snackbar.color + ' lighten-1'
        this.timeout = this.$store.state.snackbar.timeout

        this.snackbar = true
        this.$store.commit('snackbar/reset')
      }
    }
  }
}
</script>
