export const state = () => ({
  message: '',
  color: 'success',
  timeout: 2000
})

export const mutations = {
  set(state, payload) {
    state.message = payload.message
    if (payload.color) {
      state.color = payload.color
    }
    if (payload.timeout) {
      state.timeout = payload.timeout
    }
  },

  reset(state) {
    state.message = ''
    state.color = 'success'
    state.timeout = 2000
  }
}
