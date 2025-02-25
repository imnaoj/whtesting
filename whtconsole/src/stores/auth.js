import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'
import { useSocketStore } from 'src/stores/socket'
import { nextTick } from 'vue'  // Import nextTick from Vue

export const useAuthStore = defineStore('auth', {
  // Initial state
  state: () => ({
    token: null,
    email: null,
    isAuthenticated: false
  }),

  // Getters
  getters: {
    isLoggedIn: (state) => state.isAuthenticated
  },

  // Actions
  actions: {
    /**
     * Login with email and two OTP codes
     * @param {string} email - User email
     * @param {string} code1 - First OTP code
     * @param {string} code2 - Second OTP code
     * @returns {Promise<{success: boolean, error?: string}>}
     */
    async login(email, code1, code2) {
      try {
        const response = await api.post('/api/auth/signin', {
          email,
          code1,
          code2
        })

        if (response.data.success) {
          // Store token and user data
          this.token = response.data.data.token
          this.email = response.data.data.email
          this.isAuthenticated = true
          
          // Store token in localStorage
          localStorage.setItem('token', this.token)
          localStorage.setItem('email', this.email)
          
          // Initialize WebSocket with token
          await nextTick() // Use imported nextTick
          const socketStore = useSocketStore()
          socketStore.initialize(this.token)
          
          return { success: true }
        }
        return { success: false, error: response.data.error }
      } catch (error) {
        console.error('Login error:', error)
        return { 
          success: false, 
          error: error.response?.data?.error || 'Authentication failed'
        }
      }
    },

    /**
     * Logout user and clear state
     */
    logout() {
      const socketStore = useSocketStore()
      socketStore.disconnect()
      
      // Clear auth state
      this.token = null
      this.email = null
      this.isAuthenticated = false
      
      // Remove data from localStorage
      localStorage.removeItem('token')
      localStorage.removeItem('email')
    },

    /**
     * Initialize auth state from localStorage
     */
    async initializeFromStorage() {
      try {
        const token = localStorage.getItem('token')
        const email = localStorage.getItem('email')
        
        if (token && email) {
          this.token = token
          this.email = email
          this.isAuthenticated = true
          
          // Initialize WebSocket with stored token
          await nextTick() // Add nextTick here too
          const socketStore = useSocketStore()
          socketStore.initialize(token)
        }
      } catch (error) {
        console.error('Error initializing from storage:', error)
        this.logout() // Clean up if there's an error
      }
    }
  }
}) 