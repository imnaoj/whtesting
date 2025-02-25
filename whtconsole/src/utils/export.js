export function exportToCSV(data, filename) {
  // Convert webhook data to CSV format
  const headers = ['Received At (UTC)', 'Content Type', 'IP Address', 'Payload']
  const csvRows = [headers]

  data.forEach(item => {
    csvRows.push([
      new Date(item.received_at).toISOString(),
      item.content_type,
      item.ip_address,
      JSON.stringify(item.payload)
    ])
  })

  // Join fields with semicolon instead of comma
  const csvContent = csvRows.map(row => row.join(';')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  
  if (navigator.msSaveBlob) { // IE 10+
    navigator.msSaveBlob(blob, filename)
  } else {
    link.href = URL.createObjectURL(blob)
    link.download = filename
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  }
} 