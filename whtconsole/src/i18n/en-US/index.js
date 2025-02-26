export default {
  auth: {
    title: 'Admin Access',
    login: {
      title: 'Login',
      email: 'Email',
      emailRequired: 'Email is required',
      firstCode: 'First OTP Code',
      secondCode: 'Second OTP Code',
      codeRequired: 'Code is required',
      codeMustBe6Digits: 'Code must be 6 digits',
      codesMustBeDifferent: 'Codes must be different',
      button: 'Login',
      success: 'Login successful',
      error: 'An error occurred during login'
    },
    signup: {
      title: 'Sign Up',
      button: 'Sign Up',
      success: 'Account created successfully',
      error: 'Failed to create account'
    },
    qrcode: {
      title: 'Setup 2FA Authentication',
      subtitle: 'Scan this QR code with your authenticator app (Google Authenticator, Authy, etc.)',
      secretKey: 'Secret key:',
      close: 'Close'
    },
    notifications: {
      logoutSuccess: 'Logged out successfully'
    }
  },
  dashboard: {
    title: 'Webhook Paths',
    addPath: 'Add Path',
    newPath: 'New Webhook Path',
    pathLabel: 'Path',
    pathRequired: 'Path is required',
    descriptionLabel: 'Description',
    webhookCount: 'Webhooks received: {count}',
    viewData: 'View Details',
    delete: 'Delete Path',
    deleteConfirm: 'Are you sure you want to delete the path "{path}"?',
    deleteSuccess: 'Path deleted successfully',
    deleteError: 'Failed to delete path',
    export: 'Export Data',
    exportSuccess: 'Data exported successfully',
    exportError: 'Failed to export data',
    noPathsFound: 'No paths found',
    createNewPath: 'Create a new path to get started',
    cancel: 'Cancel',
    add: 'Add',
    notifications: {
      pathCreated: 'Path created successfully',
      pathCreateError: 'Failed to create path',
      deleteSuccess: 'Path deleted successfully',
      deleteError: 'Failed to delete path',
      exportSuccess: 'Data exported successfully',
      exportError: 'Failed to export data'
    }
  },
  pathDetails: {
    title: 'Path Details',
    ipAddress: 'IP Address',
    payload: 'Payload',
    headers: 'Headers',
    noData: 'No webhook data received yet',
    receivedAt: 'Received at',
    export: 'Export Data',
    exportSuccess: 'Data exported successfully',
    exportError: 'Failed to export data',
    webhookUrl: 'Webhook URL',
    copyUrl: 'Copy webhook URL to clipboard',
    notifications: {
      loadError: 'Failed to load path data',
      exportSuccess: 'Data exported successfully',
      exportError: 'Failed to export data',
      urlCopied: 'Webhook URL copied to clipboard',
      copyError: 'Failed to copy URL to clipboard'
    }
  },
  common: {
    appTitle: 'WHT Admin',
    logout: 'Logout',
    cancel: 'Cancel',
    save: 'Save',
    close: 'Close',
    back: 'Back',
    loading: 'Loading...',
    actions: 'Actions'
  },
  failed: 'Action failed',
  success: 'Action was successful',
  splash: {
    title: 'Webhook Testing Console',
    subtitle: 'Test webhook data endpoints with ease',
    startButton: 'GET STARTED'
  }
}
