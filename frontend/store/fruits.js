import Cookies from 'js-cookie'

export const actions = {
  async getFruits(_) {
    return await this.$axios.$get(`/api/fruits/`)
  },

  async getFruit(_, { id }) {
    return await this.$axios.$get(`/api/fruits/${id}/`)
  },

  async createFruit(_, { name, price, image }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'multipart/form-data'
    }
    const form = new FormData()
    form.append('name', name)
    form.append('price', price)
    if (image) {
      form.append('image', image)
    }
    await this.$axios.$post(`/api/fruits/`, form, { headers })
  },

  async updateFruit(_, { id, name, price, image }) {
    const csrfToken = Cookies.get('csrftoken')
    const headers = {
      'X-CSRFToken': csrfToken,
      'Content-Type': 'multipart/form-data'
    }
    const form = new FormData()
    form.append('name', name)
    form.append('price', price)
    if (image) {
      form.append('image', image)
    }
    await this.$axios.$patch(`/api/fruits/${id}/`, form, { headers })
  }
}
