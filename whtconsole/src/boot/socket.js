import { boot } from 'quasar/wrappers'
import { useSocketStore } from 'src/stores/socket'
import { useAuthStore } from 'src/stores/auth'

export default boot(() => {
  const authStore = useAuthStore()
  const socketStore = useSocketStore()

  if (authStore.isAuthenticated) {
    socketStore.initialize(authStore.token)
  }
}) 