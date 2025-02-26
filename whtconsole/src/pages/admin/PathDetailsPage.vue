<template>
  <q-page padding>
    <!-- Header with back button and actions -->
    <div class="row items-center q-mb-lg">
      <div class="col">
        <div class="row items-center">
          <div>
            <h5 class="q-my-none">{{ $t('pathDetails.title') }} /{{ path?.path }}</h5>
            <p class="text-caption q-my-none">{{ path?.description }}</p>
            <div class="row items-center q-mt-sm">
              <p class="text-caption text-grey-8 q-my-none">
                <span class="gt-sm">{{ $t('pathDetails.webhookUrl') }}: </span><b>{{ webhookUrl }}</b>
              <q-btn
                flat
                dense
                icon="content_copy"
                @click="copyPath"
                class="q-ml-sm"
                color="grey-8"
                size="sm"
              >
                <q-tooltip>
                  {{ $t('pathDetails.copyUrl') }}
                </q-tooltip>
              </q-btn>
            </p>
            </div>
          </div>
        </div>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="download"
          :loading="exporting"
          @click="exportData"
        >
          <span class="gt-sm">{{ $t('pathDetails.export') }}</span>
          <q-tooltip>
            {{ $t('pathDetails.export') }}
          </q-tooltip>
        </q-btn>
        <q-btn
          color="primary"
          icon="arrow_back"
          to="/admin"
          class="q-ml-md"
        >
          <span class="gt-sm">{{ $t('common.back') }}</span>
          <q-tooltip>
            {{ $t('common.back') }}
          </q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="loading" class="row justify-center q-pa-md">
      <q-spinner color="primary" size="3em" />
      <span class="q-ml-sm">{{ $t('common.loading') }}</span>
    </div>

    <!-- Data list with accordion -->
    <div v-else>
      <q-list separator>
        <transition-group
          name="webhook-list"
          appear
        >
          <q-expansion-item
            v-for="item in webhookData"
            :key="item.webhook_id"
            expand-separator
            :label="formatDate(item.received_at)"
            :caption="item.content_type"
          >
            <template v-slot:header>
              <q-item-section>
                <q-item-label>{{ formatDate(item.received_at) }}</q-item-label>
                <q-item-label caption>
                  {{ $t('pathDetails.ipAddress') }}: {{ item.ip_address }}
                </q-item-label>
              </q-item-section>
            </template>

            <q-card>
              <q-card-section>
                <div class="row items-start q-mb-sm">
                  <div class="col-1 text-caption text-grey">
                    {{ $t('pathDetails.payload') }}:
                  </div>
                  <q-card class="col bg-grey-1">
                    <q-card-section class="q-pa-sm">
                      <pre class="json-content">{{ formatPayload(item.payload) }}</pre>
                    </q-card-section>
                  </q-card>
                </div>

              </q-card-section>
            </q-card>
          </q-expansion-item>
        </transition-group>
      </q-list>

      <!-- Pagination -->
      <div class="row justify-center q-mt-md">
        <q-pagination
          v-model="currentPage"
          :max="totalPages"
          :max-pages="6"
          boundary-numbers
          direction-links
        />
      </div>
    </div>

    <!-- No data message -->
    <div v-if="!loading && webhookData.length === 0" class="text-center q-pa-md">
      {{ $t('pathDetails.noData') }}
    </div>
  </q-page>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { usePathStore } from 'src/stores/path'
import { useQuasar, copyToClipboard } from 'quasar'
import { useI18n } from 'vue-i18n'
import { api } from 'src/boot/axios'
// import { date } from 'quasar'

export default {
  name: 'PathDetailsPage',

  setup() {
    const route = useRoute()
    const pathStore = usePathStore()
    const $q = useQuasar()
    const { t } = useI18n()
    const loading = ref(true)
    const exporting = ref(false)
    const currentPage = ref(1)
    const itemsPerPage = 10
    const showHeaders = ref({})

    // Get path ID from route
    const pathId = route.params.id

    // Computed properties
    const path = computed(() => 
      pathStore.paths.find(p => p._id === pathId)
    )

    const webhookData = computed(() => 
      pathStore.pathData.data
    )

    const totalPages = computed(() => 
      Math.ceil(pathStore.pathData.total / itemsPerPage)
    )

    // Compute the webhook URL
    const webhookUrl = computed(() => {
      if (!path.value?.base || !path.value?.path) return ''
      
      // Get the base URL from the API configuration
      const baseUrl = api.defaults.baseURL
        .replace('/api', '') // Remove /api from the end
        .replace(/\/$/, '') // Remove trailing slash if present
      
      return `${baseUrl}/api/webhook/${path.value.base}/${path.value.path}`
    })

    // Methods
    const loadData = async () => {
      loading.value = true
      try {
        if (pathStore.paths.length === 0) {
          await pathStore.fetchPaths()
        }
        await pathStore.fetchPathData(pathId, {
          skip: (currentPage.value - 1) * itemsPerPage,
          limit: itemsPerPage
        })
      } catch (err) {
        console.error(err)
        $q.notify({
          type: 'negative',
          message: t('pathDetails.notifications.loadError')
        })
      } finally {
        loading.value = false
      }
    }

    const exportData = async () => {
      exporting.value = true
      try {
        await pathStore.exportPathData(pathId, path.value?.path || 'path')
        $q.notify({
          type: 'positive',
          message: t('pathDetails.notifications.exportSuccess')
        })
      } catch {
        $q.notify({
          type: 'negative',
          message: t('pathDetails.notifications.exportError')
        })
      } finally {
        exporting.value = false
      }
    }

    const formatDate = (dateStr) => {
      return dateStr
    }

    const formatPayload = (payload) => {
      return JSON.stringify(payload, null, 2)
    }

    const toggleHeaders = (itemId) => {
      showHeaders.value[itemId] = !showHeaders.value[itemId]
    }

    const copyPath = () => {
      copyToClipboard(webhookUrl.value)
        .then(() => {
          $q.notify({
            type: 'positive',
            message: t('pathDetails.notifications.urlCopied')
          })
        })
        .catch(() => {
          $q.notify({
            type: 'negative',
            message: t('pathDetails.notifications.copyError')
          })
        })
    }

    // Watch for page changes
    watch(currentPage, () => {
      loadData()
    })

    // Initial load
    onMounted(async () => {
      await loadData()
      pathStore.setupWebhookListener()
    })

    onUnmounted(() => {
      pathStore.cleanupWebhookListener()
    })

    return {
      path,
      loading,
      exporting,
      webhookData,
      currentPage,
      totalPages,
      showHeaders,
      formatDate,
      formatPayload,
      toggleHeaders,
      exportData,
      t,
      webhookUrl,
      copyPath
    }
  }
}
</script>

<style lang="scss" scoped>
.json-content {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: monospace;
  font-size: 0.9em;
}

.webhook-list-enter-active,
.webhook-list-leave-active {
  transition: all 0.5s ease;
}

.webhook-list-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.webhook-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.webhook-list-move {
  transition: transform 0.5s ease;
}
</style> 