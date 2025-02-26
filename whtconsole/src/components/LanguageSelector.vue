<template>
  <q-btn-dropdown
    no-caps
    flat
    dense
    :label="currentLanguage"
    size="md"
  >
    <q-list>
      <q-item
        v-for="lang in languages"
        :key="lang.value"
        clickable
        v-close-popup
        @click="changeLanguage(lang.value)"
      >
        <q-item-section>
          <q-item-label>{{ lang.label }}</q-item-label>
        </q-item-section>
      </q-item>
    </q-list>
  </q-btn-dropdown>
</template>

<script>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

export default {
  name: 'LanguageSelector',

  setup() {
    const { locale } = useI18n()

    const languages = [
      { value: 'es-ES', label: 'Español' },
      { value: 'en-US', label: 'English' }
    ]

    const currentLanguage = computed(() => {
      const lang = languages.find(l => l.value === locale.value)
      return lang ? lang.label : 'Language'
    })

    const changeLanguage = (lang) => {
      locale.value = lang
      localStorage.setItem('language', lang)
    }

    return {
      languages,
      currentLanguage,
      changeLanguage
    }
  }
}
</script> 