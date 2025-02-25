export default {
  auth: {
    title: 'Acceso Administrador',
    login: {
      title: 'Iniciar Sesión',
      email: 'Correo electrónico',
      emailRequired: 'El correo electrónico es obligatorio',
      firstCode: 'Primer código OTP',
      secondCode: 'Segundo código OTP',
      codeRequired: 'El código es obligatorio',
      codeMustBe6Digits: 'El código debe tener 6 dígitos',
      codesMustBeDifferent: 'Los códigos deben ser diferentes',
      button: 'Iniciar Sesión',
      success: 'Inicio de sesión exitoso',
      error: 'Ocurrió un error durante el inicio de sesión'
    },
    signup: {
      title: 'Registrarse',
      button: 'Registrarse',
      success: 'Cuenta creada exitosamente',
      error: 'Error al crear la cuenta'
    },
    qrcode: {
      title: 'Configurar Autenticación 2FA',
      subtitle: 'Escanee este código QR con su aplicación de autenticación (Google Authenticator, Authy, etc.)',
      secretKey: 'Clave secreta:',
      close: 'Cerrar'
    },
    notifications: {
      logoutSuccess: 'Sesión cerrada correctamente'
    }
  },
  dashboard: {
    title: 'Rutas Webhook',
    addPath: 'Añadir Ruta',
    newPath: 'Nueva Ruta Webhook',
    pathLabel: 'Ruta',
    pathRequired: 'La ruta es obligatoria',
    descriptionLabel: 'Descripción',
    webhookCount: 'Webhooks recibidos: {count}',
    viewData: 'Ver Detalles',
    delete: 'Eliminar Ruta',
    deleteConfirm: '¿Está seguro de que desea eliminar la ruta "{path}"?',
    deleteSuccess: 'Ruta eliminada correctamente',
    deleteError: 'Error al eliminar la ruta',
    export: 'Exportar Datos',
    exportSuccess: 'Datos exportados correctamente',
    exportError: 'Error al exportar los datos',
    noPathsFound: 'No se encontraron rutas',
    createNewPath: 'Cree una nueva ruta para comenzar',
    cancel: 'Cancelar',
    add: 'Añadir',
    notifications: {
      pathCreated: 'Ruta creada correctamente',
      pathCreateError: 'Error al crear la ruta',
      deleteSuccess: 'Ruta eliminada correctamente',
      deleteError: 'Error al eliminar la ruta',
      exportSuccess: 'Datos exportados correctamente',
      exportError: 'Error al exportar los datos'
    }
  },
  pathDetails: {
    title: 'Detalles de la Ruta',
    ipAddress: 'Dirección IP',
    payload: 'Datos',
    headers: 'Cabeceras',
    noData: 'Aún no se han recibido datos webhook',
    receivedAt: 'Recibido el',
    export: 'Exportar Datos',
    exportSuccess: 'Datos exportados correctamente',
    exportError: 'Error al exportar los datos',
    webhookUrl: 'URL del Webhook',
    copyUrl: 'Copiar URL del webhook al portapapeles',
    notifications: {
      loadError: 'Error al cargar los datos de la ruta',
      exportSuccess: 'Datos exportados correctamente',
      exportError: 'Error al exportar los datos',
      urlCopied: 'URL del webhook copiada al portapapeles',
      copyError: 'Error al copiar la URL al portapapeles'
    }
  },
  common: {
    cancel: 'Cancelar',
    save: 'Guardar',
    close: 'Cerrar',
    back: 'Volver',
    loading: 'Cargando...',
    actions: 'Acciones'
  },
  failed: 'Acción fallida',
  success: 'Acción exitosa'
} 