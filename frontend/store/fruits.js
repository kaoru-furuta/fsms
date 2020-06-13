import Cookies from 'js-cookie'

export const actions = {
  async getFruits(_) {
    return await this.$axios.$get(`/api/fruits/`)
  },

  async getFruit(_, { id }) {
    return await this.$axios.$get(`/api/fruits/${id}/`)
  },

  async createFruit(_, { name, price }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    await this.$axios.$post(`/api/fruits/`, { name, price }, { headers })
  },

  async updateFruit(_, { id, name, price }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    await this.$axios.$put(`/api/fruits/${id}/`, { name, price }, { headers })
  }
}
