import { defineStore } from 'pinia'
import { io } from 'socket.io-client'

export const useSocketStore = defineStore('socket', {
  state: () => ({
    socket: null,
    connected: false,
    authenticated: false,
    reconnectAttempts: 0
  }),

  actions: {
    initialize(token) {
      // Clean up existing connection first
      this.disconnect()

      console.log('Initializing socket connection...')

      try {
        this.socket = io('http://localhost:5000', {
          path: '/ws/socket.io',
          autoConnect: false,
          reconnection: true,
          reconnectionDelay: 1000,
          reconnectionDelayMax: 5000,
          reconnectionAttempts: 5,
          transports: ['websocket'],
          auth: {
            token: token
          }
        })

        // Setup event handlers
        this.socket.on('connect', () => {
          console.log('Socket connected, sending authentication...')
          this.connected = true
          this.reconnectAttempts = 0
          // Send authentication immediately after connection
          this.socket.emit('authenticate', token)
        })

        this.socket.on('authenticated', (response) => {
          console.log('Authentication response:', response)
          if (response.status === 'success') {
            this.authenticated = true
            console.log('Socket authenticated successfully')
          } else {
            console.error('Socket authentication failed:', response.message)
            this.authenticated = false
            this.disconnect()
          }
        })

        this.socket.on('disconnect', () => {
          console.log('Socket disconnected')
          this.connected = false
          this.authenticated = false
        })

        this.socket.on('connect_error', (error) => {
          console.error('Socket connection error:', error)
          this.connected = false
          this.authenticated = false
          this.reconnectAttempts++
          
          if (this.reconnectAttempts >= 5) {
            console.error('Max reconnection attempts reached')
            this.disconnect()
          }
        })

        // Debug all events
        this.socket.onAny((event, ...args) => {
          console.log('Socket event:', event, args)
        })

        // Start connection
        this.connect()
      } catch (error) {
        console.error('Socket initialization error:', error)
        this.disconnect()
      }
    },

    connect() {
      if (this.socket && !this.connected) {
        console.log('Attempting socket connection...')
        try {
          this.socket.connect()
        } catch (error) {
          console.error('Socket connect error:', error)
          this.disconnect()
        }
      }
    },

    disconnect() {
      if (this.socket) {
        console.log('Disconnecting socket...')
        try {
          this.socket.disconnect()
        } catch (error) {
          console.error('Error during socket disconnect:', error)
        } finally {
          this.socket = null
          this.connected = false
          this.authenticated = false
          this.reconnectAttempts = 0
        }
      }
    }
  }
}) 