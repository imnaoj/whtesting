<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          WHT Admin
        </q-toolbar-title>

        <q-space />

        <!-- Show logout button only if authenticated -->
        <q-btn
          v-if="authStore.isLoggedIn"
          flat
          round
          dense
          icon="logout"
          @click="logout"
        >
          <q-tooltip>Logout</q-tooltip>
        </q-btn>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
      <socket-status />
    </q-page-container>
  </q-layout>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'
import { useQuasar } from 'quasar'
import SocketStatus from 'components/SocketStatus.vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'AdminLayout',
  components: {
    SocketStatus
  },

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const $q = useQuasar()
    const { t } = useI18n()

    const logout = async () => {
      authStore.logout()
      router.push({ name: 'login' })
      $q.notify({
        type: 'positive',
        message: t('auth.notifications.logoutSuccess')
      })
    }

    return {
      authStore,
      logout,
      t
    }
  }
}
</script> 