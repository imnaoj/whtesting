<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          {{ t('common.appTitle') }}
        </q-toolbar-title>

        <q-space />

        <!-- Language selector -->
        <language-selector class="q-mr-sm" />

        <!-- Show logout button only if authenticated -->
        <q-btn
          v-if="authStore.isLoggedIn"
          flat
          round
          dense
          icon="logout"
          @click="logout"
        >
          <q-tooltip>{{ t('common.logout') }}</q-tooltip>
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
import LanguageSelector from 'components/LanguageSelector.vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'AdminLayout',
  
  components: {
    SocketStatus,
    LanguageSelector
  },

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const $q = useQuasar()
    const { t } = useI18n()

    const logout = async () => {
      try {
        await authStore.logout()
        router.push('/admin/login')
        $q.notify({
          type: 'positive',
          message: t('auth.notifications.logoutSuccess')
        })
      } catch (error) {
        console.error('Error during logout:', error)
        $q.notify({
          type: 'negative',
          message: t('auth.notifications.logoutError')
        })
      }
    }

    return {
      authStore,
      logout,
      t
    }
  }
}
</script> 