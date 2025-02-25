<template>
  <div class="socket-status q-pa-sm">
    <div class="row items-center q-gutter-x-sm">
      <span class="text-caption">Socket:</span>
      <q-chip
        :color="socketStore.connected ? 'positive' : 'negative'"
        text-color="white"
        size="sm"
      >
        {{ socketStore.connected ? 'Connected' : 'Disconnected' }}
      </q-chip>
      <q-chip
        :color="socketStore.authenticated ? 'positive' : 'warning'"
        text-color="white"
        size="sm"
      >
        {{ socketStore.authenticated ? 'Authenticated' : 'Not Authenticated' }}
      </q-chip>
      <q-btn
        flat
        round
        dense
        size="sm"
        icon="refresh"
        @click="reconnect"
        :loading="reconnecting"
      >
        <q-tooltip>Reconnect Socket</q-tooltip>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useSocketStore } from 'src/stores/socket'
import { useAuthStore } from 'src/stores/auth'

export default {
  setup() {
    const socketStore = useSocketStore()
    const authStore = useAuthStore()
    const reconnecting = ref(false)

    const reconnect = async () => {
      reconnecting.value = true
      try {
        socketStore.initialize(authStore.token)
        await new Promise(resolve => setTimeout(resolve, 1000))
      } finally {
        reconnecting.value = false
      }
    }

    return {
      socketStore,
      reconnect,
      reconnecting
    }
  }
}
</script> 