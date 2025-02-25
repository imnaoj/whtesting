<template>
  <q-page class="q-pa-md">
    <div class="row items-center q-mb-md">
      <div class="col">
        <h5 class="q-my-none">{{ $t('dashboard.title') }}</h5>
      </div>
      <div class="col-auto">
        <q-btn
          color="primary"
          icon="add"
          :label="$t('dashboard.addPath')"
          @click="showAddPathDialog = true"
        />
      </div>
    </div>

    <div v-if="error" class="q-mb-md">
      <q-banner class="bg-negative text-white">
        {{ error }}
        <template v-slot:action>
          <q-btn flat label="Retry" @click="loadData" />
        </template>
      </q-banner>
    </div>

    <div v-if="loading" class="flex flex-center q-pa-lg">
      <q-spinner color="primary" size="3em" />
      <span class="q-ml-sm">{{ $t('common.loading') }}</span>
    </div>
    
    <div v-else-if="paths.length === 0" class="text-center q-pa-lg">
      <p class="text-h6">{{ $t('dashboard.noPathsFound') }}</p>
      <p class="text-subtitle1">{{ $t('dashboard.createNewPath') }}</p>
    </div>

    <div v-else class="row q-col-gutter-md">
      <div v-for="path in paths" :key="path._id" class="col-12 col-md-6 col-lg-4">
        <q-card class="path-card">
          <q-card-section 
            class="cursor-pointer"
            @click="navigateToPath(path._id)"
          >
            <div class="text-h6"> {{ path.path }}</div>
            <div class="text-subtitle2">{{ path.description }}</div>
            <div class="text-body2 q-mt-sm">
              {{ $t('dashboard.webhookCount', { count: path.webhook_count || 0 }) }}
            </div>
            <webhook-mini-chart :path-id="path._id" />
          </q-card-section>

          <q-card-actions align="right">
            <q-btn
              flat
              color="primary"
              icon="download"
              @click.stop="exportData(path)"
            >
              <q-tooltip>{{ $t('dashboard.export') }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              color="negative"
              icon="delete"
              @click.stop="confirmDeletePath(path)"
            >
              <q-tooltip>{{ $t('dashboard.delete') }}</q-tooltip>
            </q-btn>
            <q-btn
              flat
              color="primary"
              icon="visibility"
              @click.stop="navigateToPath(path._id)"
            >
              <q-tooltip>{{ $t('dashboard.viewData') }}</q-tooltip>
            </q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </div>

    <!-- Add Path Dialog -->
    <q-dialog v-model="showAddPathDialog">
      <q-card style="min-width: 350px">
        <q-card-section>
          <div class="text-h6">{{ $t('dashboard.newPath') }}</div>
        </q-card-section>

        <q-card-section>
          <q-form @submit="onAddPath">
            <q-input
              v-model="newPath.path"
              :label="$t('dashboard.pathLabel')"
              :rules="[val => !!val || $t('dashboard.pathRequired')]"
            />
            <q-input
              v-model="newPath.description"
              :label="$t('dashboard.descriptionLabel')"
              type="textarea"
            />
          </q-form>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat :label="$t('dashboard.cancel')" color="primary" v-close-popup />
          <q-btn flat :label="$t('dashboard.add')" color="primary" @click="onAddPath" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { usePathStore } from 'src/stores/path'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import WebhookMiniChart from 'components/WebhookMiniChart.vue'

export default {
  components: {
    WebhookMiniChart
  },

  setup() {
    const router = useRouter()
    const $q = useQuasar()
    const pathStore = usePathStore()
    const { t } = useI18n()
    const { paths, loading } = storeToRefs(pathStore)
    const error = ref(null)
    const showAddPathDialog = ref(false)
    const newPath = ref({ path: '', description: '' })

    const navigateToPath = (pathId) => {
      router.push({
        name: 'path-details',
        params: { id: pathId }
      })
    }

    const loadData = async () => {
      error.value = null
      try {
        await pathStore.fetchPaths()
        pathStore.setupWebhookListener()
      } catch (err) {
        console.error('Error loading paths:', err)
        error.value = err.message || 'Failed to load paths'
        $q.notify({
          type: 'negative',
          message: error.value
        })
      }
    }

    const onAddPath = async () => {
      try {
        if (!newPath.value.path) {
          throw new Error('Path is required')
        }
        await pathStore.createPath(newPath.value.path, newPath.value.description)
        showAddPathDialog.value = false
        newPath.value = { path: '', description: '' }
        $q.notify({
          type: 'positive',
          message: t('dashboard.notifications.pathCreated')
        })
        await loadData()
      } catch (err) {
        console.error('Error adding path:', err)
        $q.notify({
          type: 'negative',
          message: t('dashboard.notifications.pathCreateError')
        })
      }
    }

    const confirmDeletePath = (path) => {
      $q.dialog({
        title: t('dashboard.delete'),
        message: t('dashboard.deleteConfirm', { path: path.path }),
        cancel: true,
        persistent: true
      }).onOk(async () => {
        try {
          await pathStore.deletePath(path._id)
          $q.notify({
            type: 'positive',
            message: t('dashboard.notifications.deleteSuccess')
          })
          await loadData()
        } catch {
          $q.notify({
            type: 'negative',
            message: t('dashboard.notifications.deleteError')
          })
        }
      })
    }

    const exportData = async (path) => {
      try {
        await pathStore.exportPathData(path._id, path.path)
        $q.notify({
          type: 'positive',
          message: t('dashboard.notifications.exportSuccess')
        })
      } catch {
        $q.notify({
          type: 'negative',
          message: t('dashboard.notifications.exportError')
        })
      }
    }

    onMounted(() => {
      loadData()
    })

    onUnmounted(() => {
      pathStore.cleanupWebhookListener()
    })

    return {
      paths,
      loading,
      error,
      showAddPathDialog,
      newPath,
      navigateToPath,
      loadData,
      onAddPath,
      confirmDeletePath,
      exportData,
      t
    }
  }
}
</script>

<style lang="scss">
.counter-number {
  display: inline-block;
  color: primary;
  font-weight: bold;
}

// Add Animate.css classes for counter animation
.animated {
  animation-duration: 0.5s;
  animation-fill-mode: both;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOut {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(10px); }
}

.path-card {
  height: 100%;
}

.cursor-pointer {
  cursor: pointer;
}
</style> 