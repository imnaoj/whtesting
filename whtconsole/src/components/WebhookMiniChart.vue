<template>
  <div class="webhook-mini-chart">
    <apexchart
      v-if="mounted && chartSeries.length > 0"
      ref="chart"
      :key="updateKey"
      type="line"
      height="100"
      :options="chartOptions"
      :series="chartSeries"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { usePathStore } from 'src/stores/path'
import { storeToRefs } from 'pinia'
import VueApexCharts from 'vue3-apexcharts'

export default {
  components: {
    apexchart: VueApexCharts
  },
  
  props: {
    pathId: {
      type: String,
      required: true
    }
  },

  setup(props) {
    const pathStore = usePathStore()
    const { chartData } = storeToRefs(pathStore)
    const mounted = ref(false)
    const chart = ref(null)
    const updateKey = ref(0)
    
    const chartSeries = computed(() => {
      const data = chartData.value.get(props.pathId)
      if (!data || !data.timestamps || !data.counts) return []
      
      return [{
        name: 'Webhooks',
        data: data.timestamps.map((timestamp, index) => ({
          x: timestamp,
          y: data.counts[index]
        }))
      }]
    })
    
    const chartOptions = {
      chart: {
        type: 'line',
        sparkline: {
          enabled: true
        },
        animations: {
          enabled: true,
          easing: 'linear',
          dynamicAnimation: {
            speed: 300
          }
        },
        toolbar: {
          show: false
        }
      },
      colors: ['#1976d2'], // Primary blue color
      stroke: {
        curve: 'smooth',
        width: 2,
        colors: ['#1976d2'] // Ensure line color is set here too
      },
      fill: {
        type: 'solid', // Changed from gradient to solid
        opacity: 0.95,  // Light fill for contrast
        colors: ['#1976d2']
      },
      tooltip: {
        x: {
          formatter: function(val) {
            return new Date(val).toLocaleString(localStorage.getItem('language') || 'en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: false,
              timeZone: "UTC"
            })
          }
        },
        y: {
          title: {
            formatter: () => 'Hits'
          },
          formatter: function(val) {
            return Math.round(val)
          }
        }
      },
      xaxis: {
        type: 'datetime',
        labels: {
          datetimeUTC: false,
          format: 'HH:mm'
        }
      },
      yaxis: {
        min: 0,
        forceNiceScale: true
      },
      markers: {
        size: 0,
        hover: {
          size: 3,
          colors: ['#1976d2']
        }
      },
      grid: {
        show: false
      }
    }

    const updateChart = () => {
      const now = new Date()
      const cutoffTime = now.getTime() - (60 * 60 * 1000) // 60 minutes ago

      if (chart.value && chart.value.chart) {
        const data = chartData.value.get(props.pathId)
        if (data) {
          // Filter out data older than 60 minutes
          const filteredData = {
            timestamps: data.timestamps.filter(t => t >= cutoffTime),
            counts: data.counts.slice(-(60)) // Keep last 60 points
          }

          // Update the chart
          chart.value.chart.updateSeries([{
            name: 'Webhooks',
            data: filteredData.timestamps.map((timestamp, index) => ({
              x: timestamp,
              y: filteredData.counts[index]
            }))
          }], true)
        }
      }
      
      // Force re-render for good measure
      updateKey.value++
    }

    const loadChartData = async () => {
      if (!mounted.value) return
      
      try {
        await pathStore.fetchPathChartData(props.pathId)
      } catch (err) {
        console.error('Error loading chart data:', err)
      }
    }

    // Watch for changes in the chartData Map
    watch(
      () => chartData.value.get(props.pathId),
      (newData) => {
        if (newData) {
          console.log('Chart data updated, triggering refresh')
          updateChart()
        }
      },
      { deep: true }
    )

    onMounted(() => {
      mounted.value = true
      loadChartData()
    })

    onUnmounted(() => {
      mounted.value = false
    })

    return {
      chartOptions,
      chartSeries,
      mounted,
      chart,
      updateKey
    }
  }
}
</script>

<style scoped>
.webhook-mini-chart {
  width: 100%;
  height: 100px;
  margin-top: 8px;
}
</style> 