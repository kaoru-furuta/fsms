import Cookies from 'js-cookie'

export const actions = {
  async getSales(_) {
    return await this.$axios.$get(`/api/sales/`)
  },

  async getSale(_, { id }) {
    return await this.$axios.$get(`/api/sales/${id}/`)
  },

  async createSale(_, { fruit, number, amount, sold_at }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    await this.$axios.$post(
      `/api/sales/`,
      { fruit, number, amount, sold_at },
      { headers }
    )
  },

  async updateSale(_, { id, fruit, number, amount, sold_at }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = { 'X-CSRFToken': csrfToken }
    await this.$axios.$put(
      `/api/sales/${id}/`,
      { fruit, number, amount, sold_at },
      { headers }
    )
  }
}
