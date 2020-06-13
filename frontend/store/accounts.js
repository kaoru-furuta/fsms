import Cookies from 'js-cookie'

export const state = () => ({
  isAuthenticated: false
})

export const mutations = {
  setStatus: function(state, status) {
    state.isAuthenticated = status
  }
}

export const actions = {
  async getUser() {
    try {
      return await this.$axios.$get('/api/user/')
    } catch (e) {}
  },

  async login({ commit }, { username, password }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    try {
      await this.$axios.$post(
        '/api/login/',
        {
          username,
          password
        },
        { headers }
      )
      commit('setStatus', true)
    } catch (e) {}
  },

  async me({ commit }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    try {
      await this.$axios.$get('/api/me/', { headers })
      commit('setStatus', true)
    } catch (e) {}
  },

  async logout({ commit }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    try {
      await this.$axios.$delete('/api/logout/', { headers })
      commit('setStatus', false)
    } catch (e) {}
  }
}
