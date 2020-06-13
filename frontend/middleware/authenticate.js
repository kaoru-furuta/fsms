import Cookies from 'js-cookie'

function routeOption(route, key, value) {
  return route.matched.some((m) => {
    if (process.browser) {
      return Object.values(m.components).some(
        (component) => component.options[key] === value
      )
    } else {
      return Object.values(m.components).some((component) =>
        Object.values(component._Ctor).some(
          (ctor) => ctor.options && ctor.options[key] === value
        )
      )
    }
  })
}

export default async function(context) {
  const currentPath = context.route.path

  await context.store.dispatch('accounts/me')

  if (
    context.store.state.accounts.isAuthenticated &&
    currentPath === '/login'
  ) {
    context.redirect('/')
    return
  }

  if (
    !routeOption(context.route, 'auth', false) &&
    !context.store.state.accounts.isAuthenticated
  ) {
    context.redirect('/login')
    return
  }
}
