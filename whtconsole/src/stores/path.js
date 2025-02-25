import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'
import { useSocketStore } from 'src/stores/socket'
import { exportToCSV } from 'src/utils/export'

export const usePathStore = defineStore('path', {
  state: () => ({
    paths: [],
    loading: false,
    pathData: {
      data: [],
      total: 0,
      loading: false
    },
    chartData: new Map(), // Store chart data for each path
    pendingUpdates: new Map(),
    webhookListener: null
  }),

  actions: {
    async fetchPaths() {
      console.log('Fetching paths...')
      this.loading = true
      try {
        const response = await api.get('/api/paths/')
        console.log('Paths response:', response)
        
        if (response.data.success) {
          this.paths = response.data.data || []
          console.log('Paths updated:', this.paths)
        } else {
          console.error('Failed to fetch paths:', response.data.error)
          throw new Error(response.data.error || 'Failed to fetch paths')
        }
      } catch (error) {
        console.error('Error fetching paths:', error)
        this.paths = []
        throw error.response?.data?.error || error.message || 'Failed to fetch paths'
      } finally {
        this.loading = false
      }
    },

    async createPath(path, description) {
      try {
        const response = await api.post('/api/paths/', { path, description })
        if (response.data.success) {
          this.paths.push(response.data.data)
          return response.data.data
        }
      } catch (error) {
        throw error.response?.data?.error || 'Failed to create path'
      }
    },

    async deletePath(pathId) {
      try {
        const response = await api.delete(`/api/paths/${pathId}`)
        if (response.data.success) {
          this.paths = this.paths.filter(p => p._id !== pathId)
        }
      } catch (error) {
        throw error.response?.data?.error || 'Failed to delete path'
      }
    },

    async fetchPathData(pathId, { limit = 10, skip = 0 } = {}) {
      console.log('Fetching path data for:', pathId)
      this.pathData.loading = true
      try {
        const response = await api.get(`/api/paths/${pathId}/data/`, {
          params: { limit, skip }
        })
        console.log('Path data response:', response)

        if (response.data.success) {
          this.pathData.data = response.data.data.data || []
          this.pathData.total = response.data.data.total_count || 0
          console.log('Path data updated:', this.pathData)
        } else {
          console.error('Failed to fetch path data:', response.data.error)
          throw new Error(response.data.error || 'Failed to fetch path data')
        }
      } catch (error) {
        console.error('Error fetching path data:', error)
        this.pathData.data = []
        this.pathData.total = 0
        throw error.response?.data?.error || error.message || 'Failed to fetch path data'
      } finally {
        this.pathData.loading = false
      }
    },

    setupWebhookListener() {
      console.log('Setting up webhook listener...')
      const socketStore = useSocketStore()
      
      if (!socketStore.socket) {
        console.warn('No socket connection available')
        return
      }

      // Remove existing listener if any
      this.cleanupWebhookListener()

      try {
        socketStore.socket.on('webhook_update', (data) => {
          console.log('Webhook update received:', data)
          this.handleWebhookUpdate(data)
        })
        console.log('Webhook listener setup complete')
      } catch (error) {
        console.error('Error setting up webhook listener:', error)
      }
    },

    handleWebhookUpdate(data) {
      try {
        if (!data || !data.path_id) {
          console.warn('Invalid webhook data received:', data)
          return
        }

        // Update path count in paths list
        const pathIndex = this.paths.findIndex(p => p._id === data.path_id)
        if (pathIndex !== -1) {
          const updatedPaths = [...this.paths]
          updatedPaths[pathIndex] = {
            ...updatedPaths[pathIndex],
            webhook_count: (updatedPaths[pathIndex].webhook_count || 0) + 1
          }
          this.paths = updatedPaths
        }

        // Update chart data if we have it for this path
        const existingChartData = this.chartData.get(data.path_id)
        if (existingChartData) {
          // Get current time rounded to the minute
          const now = new Date()
          now.setSeconds(0, 0)
          const timestamp = now.getTime()

          let newTimestamps = [...existingChartData.timestamps]
          let newCounts = [...existingChartData.counts]

          // Find or add the current minute
          const index = newTimestamps.findIndex(t => t === timestamp)
          if (index !== -1) {
            newCounts[index]++
          } else {
            newTimestamps.push(timestamp)
            newCounts.push(1)

            // Keep only last 480 minutes
            const cutoff = now.getTime() - (480 * 60 * 1000)
            while (newTimestamps[0] < cutoff) {
              newTimestamps.shift()
              newCounts.shift()
            }
          }

          // Update the store
          this.chartData.set(data.path_id, {
            timestamps: newTimestamps,
            counts: newCounts
          })
        } else {
          // If we don't have chart data yet, fetch it
          this.fetchPathChartData(data.path_id)
        }

        // Update path data if we're viewing this path
        if (this.pathData.data.length > 0 && 
            data.path_id === this.pathData.data[0].path_id) {
          this.pathData.data = [data, ...this.pathData.data]
          this.pathData.total++
        }
      } catch (error) {
        console.error('Error handling webhook update:', error)
      }
    },

    cleanupWebhookListener() {
      console.log('Cleaning up webhook listener...')
      const socketStore = useSocketStore()
      if (socketStore.socket) {
        try {
          socketStore.socket.off('webhook_update')
          console.log('Webhook listener cleaned up')
        } catch (error) {
          console.error('Error cleaning up webhook listener:', error)
        }
      }
    },

    async fetchPathChartData(pathId) {
      console.log('Fetching chart data for path:', pathId)
      try {
        const response = await api.get(`/api/paths/${pathId}/chart/`)
        if (response.data.success) {
          this.chartData.set(pathId, response.data.data)
          console.log('Successfully fetched and stored chart data')
          return response.data.data
        }
      } catch (error) {
        console.error('Error fetching chart data:', error)
        throw error
      }
    },

    async exportPathData(pathId, pathName) {
      try {
        const response = await api.get(`/api/paths/${pathId}/data/`, {
          params: { limit: 1000000 } // Get all data
        })
        if (response.data.success) {
          const filename = `webhook-data-${pathName}-${new Date().toISOString().split('T')[0]}.csv`
          exportToCSV(response.data.data.data, filename)
        }
      } catch (error) {
        console.error('Error exporting data:', error)
        throw error
      }
    }
  }
}) 