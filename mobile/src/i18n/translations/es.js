export default {
  // Common
  common: {
    appName: 'IdentiCan',
    loading: 'Cargando...',
    error: 'Error',
    cancel: 'Cancelar',
    save: 'Guardar',
    delete: 'Eliminar',
    search: 'Buscar',
    back: 'Volver',
    ok: 'OK',
    close: 'Cerrar',
    share: 'Compartir',
    or: 'o',
    yes: 'Sí',
    no: 'No',
  },

  // Language names
  languages: {
    es: 'Español',
    en: 'English',
    pt: 'Português',
    selectLanguage: 'Idioma',
  },

  // Auth
  auth: {
    login: 'Iniciar Sesión',
    register: 'Crear Cuenta',
    logout: 'Cerrar Sesión',
    email: 'Email',
    password: 'Contraseña',
    confirmPassword: 'Confirmar contraseña',
    fullName: 'Nombre completo',
    phone: 'Teléfono (opcional)',
    subtitle: 'Identificación biométrica canina',
    noAccount: '¿No tenés cuenta? Registrate',
    hasAccount: 'Ya tengo cuenta, iniciar sesión',
    fillAllFields: 'Completá todos los campos',
    fillRequired: 'Completá los campos obligatorios',
    passwordMinLength: 'La contraseña debe tener al menos 6 caracteres',
    passwordsNoMatch: 'Las contraseñas no coinciden',
    loginError: 'Error al iniciar sesión',
    registerError: 'Error al registrarse',
  },

  // Navigation & Tabs
  nav: {
    myDogs: 'Mis Perros',
    verify: 'Verificar',
    myCan: 'Mi Can',
    addDog: 'Agregar Perro',
    profile: 'Perfil',
    vaccines: 'Vacunas',
    qrCode: 'Código QR',
    scanNose: 'Escanear Nariz',
    scanQR: 'Escanear QR',
    result: 'Resultado',
    createAccount: 'Crear Cuenta',
    settings: 'Ajustes',
  },

  // Home Screen
  home: {
    greeting: 'Hola, {{name}}',
    dogCount: '{{count}} perro(s) registrado(s)',
    dogCountOne: '1 perro registrado',
    dogCountOther: '{{count}} perros registrados',
    noDogs: 'No tenés perros registrados',
    noDogsHint: 'Tocá el botón + para agregar tu primer perro',
    errorLoading: 'Error al cargar los perros',
  },

  // Dog Card
  dog: {
    male: 'Macho',
    female: 'Hembra',
    noBreed: 'Sin raza',
    years: 'años',
    kg: 'kg',
  },

  // Add Dog
  addDog: {
    basicInfo: 'Datos básicos',
    additionalInfo: 'Información adicional',
    dogName: 'Nombre del perro',
    breed: 'Raza',
    sex: 'Sexo',
    origin: 'Origen',
    age: 'Edad (años)',
    weight: 'Peso (kg)',
    color: 'Color',
    microchip: 'ID Microchip',
    behavior: 'Comportamiento',
    likes: 'Le gusta...',
    allergies: 'Alergias',
    registerDog: 'Registrar Perro',
    nameRequired: 'El nombre es obligatorio',
    success: 'Listo',
    successMessage: '{{name}} fue registrado correctamente',
    errorRegistering: 'Error al registrar el perro',
    adopted: 'Adoptado',
    purchased: 'Comprado',
    rescued: 'Rescatado',
    other: 'Otro',
  },

  // Dog Profile
  dogProfile: {
    sex: 'Sexo',
    age: 'Edad',
    weight: 'Peso',
    color: 'Color',
    origin: 'Origen',
    microchip: 'Microchip',
    notes: 'Notas',
    behaviorLabel: 'Comportamiento',
    likesLabel: 'Le gusta',
    allergiesLabel: 'Alergias',
    vaccines: 'Vacunas',
    qrCode: 'Código QR',
    registeredOn: 'Registrado el {{date}}',
    notRegistered: 'No registrada',
    yearsUnit: '{{count}} años',
    kgUnit: '{{value}} kg',
  },

  // Vaccines
  vaccines: {
    title: 'Vacunas de {{name}}',
    noVaccines: 'No hay vacunas registradas',
    addVaccine: 'Agregar Vacuna',
    vaccineType: 'Tipo de vacuna',
    date: 'Fecha (AAAA-MM-DD)',
    vet: 'Veterinario',
    clinic: 'Clínica',
    notes: 'Notas',
    deleteTitle: 'Eliminar vacuna',
    deleteConfirm: '¿Estás seguro?',
    errorLoading: 'No se pudieron cargar las vacunas',
    errorSaving: 'Error al guardar',
    errorDeleting: 'No se pudo eliminar',
    fillRequired: 'Completá el tipo de vacuna y la fecha',
    dateFormat: 'Formato de fecha: AAAA-MM-DD',
    nextDose: 'Próxima dosis: {{date}}',
    vaccineTypePlaceholder: 'Ej: Antirrábica, Séxtuple',
    datePlaceholder: '2024-01-15',
  },

  // QR Screen
  qr: {
    title: 'Código QR',
    scanInstruction: 'Escaneá este código QR para identificar a {{name}}. Podés imprimirlo y colocarlo en su collar.',
    share: 'Compartir',
    downloadPDF: 'Descargar PDF',
    shareTitle: 'Compartir QR',
    shareMessage: 'La funcionalidad de compartir estará disponible próximamente.',
    pdfTitle: 'Descargar PDF',
    pdfMessage: 'La descarga de PDF estará disponible próximamente.',
  },

  // Scan Nose
  scanNose: {
    title: 'Escanear Nariz',
    description: 'Apuntá la cámara a la nariz del perro para identificarlo. Asegurate de que la nariz esté bien iluminada y enfocada.',
    step1: 'Acercá el celular a la nariz del perro',
    step2: 'Mantené la cámara estable',
    step3: 'Esperá el resultado de la verificación',
    startScan: 'Iniciar Escaneo',
    scanQRInstead: 'Escanear QR en su lugar',
    errorVerification: 'No se pudo realizar la verificación',
  },

  // Scan QR
  scanQR: {
    title: 'Escanear Código QR',
    description: 'Escaneá el código QR del collar del perro para ver su información.',
    openCamera: 'Abrir Cámara QR',
    cameraTitle: 'Cámara QR',
    cameraMessage: 'La cámara QR estará disponible próximamente. Usá la búsqueda manual.',
    manualEntry: 'o ingresá el código manualmente',
    qrPlaceholder: 'Código QR (ej: IDC-DOG-00001)',
    enterCode: 'Ingresá un código QR',
    errorSearch: 'No se pudo buscar el código QR',
  },

  // Result Screen
  result: {
    matchFound: 'Coincidencia Encontrada',
    noMatch: 'Sin Coincidencia',
    dogData: 'Datos del Perro',
    name: 'Nombre',
    id: 'ID',
    confidence: 'Confianza',
    dailyUsage: 'Uso del día',
    remainingVerifications: 'Te quedan {{count}} verificaciones hoy',
    unlimitedVerifications: 'Verificaciones ilimitadas',
    newVerification: 'Nueva Verificación',
    dogFoundByQR: 'Perro encontrado por QR',
    dogNotFoundByQR: 'No se encontró un perro con ese código QR',
  },

  // Limit Modal
  limit: {
    title: 'Límite Diario Alcanzado',
    description: 'Alcanzaste el máximo de verificaciones gratuitas por hoy.',
    usageCount: '{{used}} / {{limit}} verificaciones usadas',
    upgradeText: 'Upgrade a Premium para verificaciones ilimitadas y más beneficios.',
    viewPremium: 'Ver Premium',
    dailyLimitReached: 'Límite diario alcanzado',
  },

  // Vaccine Card
  vaccineCard: {
    vet: 'Vet',
    clinic: 'Clínica',
    nextDose: 'Próxima dosis',
  },
};
