import { boot } from 'quasar/wrappers'
import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'

let i18n

export default boot(({ app }) => {
  // Get stored language or default to en-US, but only in browser environment
  const storedLang = process.env.CLIENT 
    ? window.localStorage.getItem('language') 
    : null

  i18n = createI18n({
    locale: storedLang || 'en-US',
    legacy: false,
    globalInjection: true,
    messages
  })

  // Set i18n instance on app
  app.use(i18n)
})

// Export composed i18n instance
export { i18n }
