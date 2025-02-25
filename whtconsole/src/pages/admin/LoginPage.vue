<template>
  <q-page class="flex flex-center">
    <q-card class="login-card">
      <q-card-section class="text-center">
        <h5 class="q-mt-none q-mb-md">{{ $t('auth.title') }}</h5>
      </q-card-section>

      <q-card-section>
        <!-- Mode Toggle -->
        <div class="text-center q-mb-md">
          <q-btn-toggle
            v-model="mode"
            spread
            no-caps
            toggle-color="primary"
            :options="[
              { label: $t('auth.login.title'), value: 'login' },
              { label: $t('auth.signup.title'), value: 'signup' }
            ]"
          />
        </div>

        <!-- Login Form -->
        <q-form v-if="mode === 'login'" @submit="onLogin" class="q-gutter-md">
          <q-input
            v-model="email"
            :label="$t('auth.login.email')"
            type="email"
            :rules="[val => !!val || $t('auth.login.emailRequired')]"
          />

          <div class="row q-gutter-md">
            <q-input
              v-model="code1"
              :label="$t('auth.login.firstCode')"
              class="col"
              :rules="[
                val => !!val || $t('auth.login.codeRequired'),
                val => val.length === 6 || $t('auth.login.codeMustBe6Digits')
              ]"
            />
            <q-input
              v-model="code2"
              :label="$t('auth.login.secondCode')"
              class="col"
              :rules="[
                val => !!val || $t('auth.login.codeRequired'),
                val => val.length === 6 || $t('auth.login.codeMustBe6Digits'),
                val => val !== code1 || $t('auth.login.codesMustBeDifferent')
              ]"
            />
          </div>

          <div class="text-center q-mt-md">
            <q-btn
              type="submit"
              color="primary"
              :label="$t('auth.login.button')"
              :loading="loading"
            />
          </div>
        </q-form>

        <!-- Signup Form -->
        <q-form v-else @submit="onSignup" class="q-gutter-md">
          <q-input
            v-model="email"
            :label="$t('auth.login.email')"
            type="email"
            :rules="[val => !!val || $t('auth.login.emailRequired')]"
          />

          <div class="text-center q-mt-md">
            <q-btn
              type="submit"
              color="primary"
              :label="$t('auth.signup.button')"
              :loading="loading"
            />
          </div>
        </q-form>

        <!-- QR Code Dialog -->
        <q-dialog v-model="showQRDialog">
          <q-card style="min-width: 350px">
            <q-card-section class="text-center">
              <h6 class="q-mt-none q-mb-md">{{ $t('auth.qrcode.title') }}</h6>
              <p class="text-caption q-mb-md">
                {{ $t('auth.qrcode.subtitle') }}
              </p>
              <div class="text-center q-mb-md">
                <QRCodeVue3
                  :value="otpAuthUrl"
                  :size="200"
                  level="M"
                  render-as="svg"
                  :dot-scale="1"
                  :background-color="'#ffffff'"
                  :foreground-color="'#444444'"
                  :dots-options="{ type: 'dots' }"
                />
              </div>
              <p class="text-caption q-mb-none">
                {{ $t('auth.qrcode.secretKey') }} {{ secretKey }}
              </p>
            </q-card-section>
            <q-card-actions align="center">
              <q-btn flat :label="$t('auth.qrcode.close')" color="primary" v-close-popup />
            </q-card-actions>
          </q-card>
        </q-dialog>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Notify } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { api } from 'src/boot/axios'
import QRCodeVue3 from 'qrcode-vue3'
import { useI18n } from 'vue-i18n'

export default {
  components: {
    QRCodeVue3
  },

  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const { t } = useI18n()

    const mode = ref('login')
    const email = ref('')
    const code1 = ref('')
    const code2 = ref('')
    const loading = ref(false)
    const showQRDialog = ref(false)
    const secretKey = ref('')

    // Compute the OTP Auth URL when needed
    const otpAuthUrl = computed(() => {
      if (!secretKey.value || !email.value) return ''
      return `otpauth://totp/WHT:${email.value}?secret=${secretKey.value}&issuer=WHT`
    })

    const showNotification = (type, message) => {
      Notify.create({
        type,
        message,
        position: 'top',
        timeout: 3000
      })
    }

    const onLogin = async () => {
      loading.value = true
      try {
        const result = await authStore.login(email.value, code1.value, code2.value)
        if (result.success) {
          showNotification('positive', t('auth.login.success'))
          router.push('/admin')
        } else {
          showNotification('negative', result.error)
        }
      } catch {
        showNotification('negative', t('auth.login.error'))
      } finally {
        loading.value = false
      }
    }

    const onSignup = async () => {
      loading.value = true
      try {
        const response = await api.post('/api/auth/signup', {
          email: email.value
        })

        if (response.data.success) {
          const { secret_key } = response.data.data
          secretKey.value = secret_key
          showNotification('positive', t('auth.signup.success'))
          showQRDialog.value = true
          mode.value = 'login'
        } else {
          showNotification('negative', response.data.error)
        }
      } catch (err) {
        showNotification('negative', 
          err.response?.data?.error || t('auth.signup.error'))
      } finally {
        loading.value = false
      }
    }

    return {
      mode,
      email,
      code1,
      code2,
      loading,
      showQRDialog,
      secretKey,
      otpAuthUrl,
      onLogin,
      onSignup
    }
  }
}
</script>

<style scoped>
.login-card {
  width: 100%;
  max-width: 400px;
  padding: 20px;
}
</style> 