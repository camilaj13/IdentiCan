export default {
  // Common
  common: {
    appName: 'IdentiCan',
    loading: 'Carregando...',
    error: 'Erro',
    cancel: 'Cancelar',
    save: 'Salvar',
    delete: 'Excluir',
    search: 'Buscar',
    back: 'Voltar',
    ok: 'OK',
    close: 'Fechar',
    share: 'Compartilhar',
    or: 'ou',
    yes: 'Sim',
    no: 'Não',
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
    login: 'Entrar',
    register: 'Criar Conta',
    logout: 'Sair',
    email: 'Email',
    password: 'Senha',
    confirmPassword: 'Confirmar senha',
    fullName: 'Nome completo',
    phone: 'Telefone (opcional)',
    subtitle: 'Identificação biométrica canina',
    noAccount: 'Não tem conta? Cadastre-se',
    hasAccount: 'Já tenho conta, entrar',
    fillAllFields: 'Preencha todos os campos',
    fillRequired: 'Preencha os campos obrigatórios',
    passwordMinLength: 'A senha deve ter pelo menos 6 caracteres',
    passwordsNoMatch: 'As senhas não coincidem',
    loginError: 'Erro ao entrar',
    registerError: 'Erro ao cadastrar',
  },

  // Navigation & Tabs
  nav: {
    myDogs: 'Meus Cães',
    verify: 'Verificar',
    myCan: 'Meu Cão',
    addDog: 'Adicionar Cão',
    profile: 'Perfil',
    vaccines: 'Vacinas',
    qrCode: 'Código QR',
    scanNose: 'Escanear Nariz',
    scanQR: 'Escanear QR',
    result: 'Resultado',
    createAccount: 'Criar Conta',
    settings: 'Configurações',
  },

  // Home Screen
  home: {
    greeting: 'Olá, {{name}}',
    dogCount: '{{count}} cão(es) registrado(s)',
    dogCountOne: '1 cão registrado',
    dogCountOther: '{{count}} cães registrados',
    noDogs: 'Nenhum cão registrado',
    noDogsHint: 'Toque no botão + para adicionar seu primeiro cão',
    errorLoading: 'Erro ao carregar os cães',
  },

  // Dog Card
  dog: {
    male: 'Macho',
    female: 'Fêmea',
    noBreed: 'Sem raça',
    years: 'anos',
    kg: 'kg',
  },

  // Add Dog
  addDog: {
    basicInfo: 'Dados básicos',
    additionalInfo: 'Informações adicionais',
    dogName: 'Nome do cão',
    breed: 'Raça',
    sex: 'Sexo',
    origin: 'Origem',
    age: 'Idade (anos)',
    weight: 'Peso (kg)',
    color: 'Cor',
    microchip: 'ID Microchip',
    behavior: 'Comportamento',
    likes: 'Gosta de...',
    allergies: 'Alergias',
    registerDog: 'Registrar Cão',
    nameRequired: 'O nome é obrigatório',
    success: 'Pronto',
    successMessage: '{{name}} foi registrado com sucesso',
    errorRegistering: 'Erro ao registrar o cão',
    adopted: 'Adotado',
    purchased: 'Comprado',
    rescued: 'Resgatado',
    other: 'Outro',
  },

  // Dog Profile
  dogProfile: {
    sex: 'Sexo',
    age: 'Idade',
    weight: 'Peso',
    color: 'Cor',
    origin: 'Origem',
    microchip: 'Microchip',
    notes: 'Notas',
    behaviorLabel: 'Comportamento',
    likesLabel: 'Gosta de',
    allergiesLabel: 'Alergias',
    vaccines: 'Vacinas',
    qrCode: 'Código QR',
    registeredOn: 'Registrado em {{date}}',
    notRegistered: 'Não registrada',
    yearsUnit: '{{count}} anos',
    kgUnit: '{{value}} kg',
  },

  // Vaccines
  vaccines: {
    title: 'Vacinas de {{name}}',
    noVaccines: 'Nenhuma vacina registrada',
    addVaccine: 'Adicionar Vacina',
    vaccineType: 'Tipo de vacina',
    date: 'Data (AAAA-MM-DD)',
    vet: 'Veterinário',
    clinic: 'Clínica',
    notes: 'Notas',
    deleteTitle: 'Excluir vacina',
    deleteConfirm: 'Tem certeza?',
    errorLoading: 'Não foi possível carregar as vacinas',
    errorSaving: 'Erro ao salvar',
    errorDeleting: 'Não foi possível excluir',
    fillRequired: 'Preencha o tipo de vacina e a data',
    dateFormat: 'Formato da data: AAAA-MM-DD',
    nextDose: 'Próxima dose: {{date}}',
    vaccineTypePlaceholder: 'Ex: Antirrábica, V10',
    datePlaceholder: '2024-01-15',
  },

  // QR Screen
  qr: {
    title: 'Código QR',
    scanInstruction: 'Escaneie este código QR para identificar {{name}}. Você pode imprimi-lo e colocá-lo na coleira.',
    share: 'Compartilhar',
    downloadPDF: 'Baixar PDF',
    shareTitle: 'Compartilhar QR',
    shareMessage: 'A funcionalidade de compartilhamento estará disponível em breve.',
    pdfTitle: 'Baixar PDF',
    pdfMessage: 'O download de PDF estará disponível em breve.',
  },

  // Scan Nose
  scanNose: {
    title: 'Escanear Nariz',
    description: 'Aponte a câmera para o nariz do cão para identificá-lo. Certifique-se de que o nariz esteja bem iluminado e focado.',
    step1: 'Aproxime o celular do nariz do cão',
    step2: 'Mantenha a câmera estável',
    step3: 'Aguarde o resultado da verificação',
    startScan: 'Iniciar Escaneamento',
    scanQRInstead: 'Escanear QR em vez disso',
    errorVerification: 'Não foi possível realizar a verificação',
  },

  // Scan QR
  scanQR: {
    title: 'Escanear Código QR',
    description: 'Escaneie o código QR da coleira do cão para ver suas informações.',
    openCamera: 'Abrir Câmera QR',
    cameraTitle: 'Câmera QR',
    cameraMessage: 'A câmera QR estará disponível em breve. Use a busca manual.',
    manualEntry: 'ou insira o código manualmente',
    qrPlaceholder: 'Código QR (ex: IDC-DOG-00001)',
    enterCode: 'Insira um código QR',
    errorSearch: 'Não foi possível buscar o código QR',
  },

  // Result Screen
  result: {
    matchFound: 'Correspondência Encontrada',
    noMatch: 'Sem Correspondência',
    dogData: 'Dados do Cão',
    name: 'Nome',
    id: 'ID',
    confidence: 'Confiança',
    dailyUsage: 'Uso diário',
    remainingVerifications: '{{count}} verificações restantes hoje',
    unlimitedVerifications: 'Verificações ilimitadas',
    newVerification: 'Nova Verificação',
    dogFoundByQR: 'Cão encontrado por QR',
    dogNotFoundByQR: 'Nenhum cão encontrado com esse código QR',
  },

  // Limit Modal
  limit: {
    title: 'Limite Diário Atingido',
    description: 'Você atingiu o máximo de verificações gratuitas por hoje.',
    usageCount: '{{used}} / {{limit}} verificações usadas',
    upgradeText: 'Faça upgrade para Premium para verificações ilimitadas e mais benefícios.',
    viewPremium: 'Ver Premium',
    dailyLimitReached: 'Limite diário atingido',
  },

  // Vaccine Card
  vaccineCard: {
    vet: 'Vet',
    clinic: 'Clínica',
    nextDose: 'Próxima dose',
  },
};
