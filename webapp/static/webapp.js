// ── IdentiCan Web Application ────────────────────────────
// Full SPA matching the mobile app: same API, same roles, same features.
(function () {
  'use strict';

  const API_BASE = window.location.origin;

  // ── State ───────────────────────────────────────────────
  let token = localStorage.getItem('identican_token');
  let currentUser = null;
  let currentLang = localStorage.getItem('identican_lang') || 'es';
  let screenHistory = [];
  let currentScreen = 'home';
  let currentTab = 'mican';

  // Temp state for sub-screens
  let currentDog = null;          // dog profile context
  let currentDogVaccines = null;  // vaccines list
  let currentResult = null;       // verification result
  let deleteVaccineId = null;     // vaccine to delete

  // ── Translations ────────────────────────────────────────
  const TRANSLATIONS = {
    es: {
      'auth.subtitle': 'Identificación biométrica canina',
      'auth.email': 'Email',
      'auth.password': 'Contraseña',
      'auth.confirmPassword': 'Confirmar contraseña',
      'auth.fullName': 'Nombre completo',
      'auth.phone': 'Teléfono (opcional)',
      'auth.login': 'Iniciar Sesión',
      'auth.register': 'Crear Cuenta',
      'auth.noAccount': '¿No tenés cuenta? Registrate',
      'auth.hasAccount': 'Ya tengo cuenta, iniciar sesión',
      'auth.fillAllFields': 'Completá todos los campos',
      'auth.fillRequired': 'Completá los campos obligatorios',
      'auth.passwordMinLength': 'La contraseña debe tener al menos 6 caracteres',
      'auth.passwordsNoMatch': 'Las contraseñas no coinciden',
      'nav.createAccount': 'Crear Cuenta',
      'nav.myCan': 'Mi Can',
      'nav.verify': 'Verificar',
      'nav.myDogs': 'Mis Perros',
      'nav.addDog': 'Agregar Perro',
      'nav.profile': 'Perfil',
      'nav.vaccines': 'Vacunas',
      'nav.qrCode': 'Código QR',
      'nav.scanNose': 'Escanear Nariz',
      'nav.scanQR': 'Escanear QR',
      'nav.result': 'Resultado',
      'home.greeting': 'Hola, {name}',
      'home.dogCountOne': '1 perro registrado',
      'home.dogCountOther': '{count} perros registrados',
      'home.noDogs': 'No tenés perros registrados',
      'home.noDogsHint': 'Tocá el botón + para agregar tu primer perro',
      'home.errorLoading': 'Error al cargar los perros',
      'dog.male': 'Macho',
      'dog.female': 'Hembra',
      'dog.noBreed': 'Sin raza',
      'dog.years': 'años',
      'dog.kg': 'kg',
      'addDog.basicInfo': 'Datos básicos',
      'addDog.additionalInfo': 'Información adicional',
      'addDog.dogName': 'Nombre del perro',
      'addDog.breed': 'Raza',
      'addDog.sex': 'Sexo',
      'addDog.origin': 'Origen',
      'addDog.age': 'Edad (años)',
      'addDog.weight': 'Peso (kg)',
      'addDog.color': 'Color',
      'addDog.microchip': 'ID Microchip',
      'addDog.behavior': 'Comportamiento',
      'addDog.likes': 'Le gusta...',
      'addDog.allergies': 'Alergias',
      'addDog.registerDog': 'Registrar Perro',
      'addDog.nameRequired': 'El nombre es obligatorio',
      'addDog.success': 'Listo',
      'addDog.successMessage': '{name} fue registrado correctamente',
      'addDog.errorRegistering': 'Error al registrar el perro',
      'addDog.adopted': 'Adoptado',
      'addDog.purchased': 'Comprado',
      'addDog.rescued': 'Rescatado',
      'addDog.other': 'Otro',
      'dogProfile.sex': 'Sexo',
      'dogProfile.age': 'Edad',
      'dogProfile.weight': 'Peso',
      'dogProfile.color': 'Color',
      'dogProfile.origin': 'Origen',
      'dogProfile.microchip': 'Microchip',
      'dogProfile.notes': 'Notas',
      'dogProfile.behaviorLabel': 'Comportamiento',
      'dogProfile.likesLabel': 'Le gusta',
      'dogProfile.allergiesLabel': 'Alergias',
      'dogProfile.vaccines': 'Vacunas',
      'dogProfile.qrCode': 'Código QR',
      'dogProfile.registeredOn': 'Registrado el {date}',
      'dogProfile.notRegistered': 'No registrada',
      'dogProfile.yearsUnit': '{count} años',
      'dogProfile.kgUnit': '{value} kg',
      'vaccines.title': 'Vacunas de {name}',
      'vaccines.noVaccines': 'No hay vacunas registradas',
      'vaccines.addVaccine': 'Agregar Vacuna',
      'vaccines.vaccineType': 'Tipo de vacuna',
      'vaccines.date': 'Fecha (AAAA-MM-DD)',
      'vaccines.vet': 'Veterinario',
      'vaccines.clinic': 'Clínica',
      'vaccines.notes': 'Notas',
      'vaccines.deleteTitle': 'Eliminar vacuna',
      'vaccines.deleteConfirm': '¿Estás seguro?',
      'vaccines.errorLoading': 'No se pudieron cargar las vacunas',
      'vaccines.errorSaving': 'Error al guardar',
      'vaccines.errorDeleting': 'No se pudo eliminar',
      'vaccines.fillRequired': 'Completá el tipo de vacuna y la fecha',
      'vaccines.dateFormat': 'Formato de fecha: AAAA-MM-DD',
      'vaccines.vaccineTypePlaceholder': 'Ej: Antirrábica, Séxtuple',
      'vaccines.datePlaceholder': '2024-01-15',
      'qr.scanInstruction': 'Escaneá este código QR para identificar a {name}. Podés imprimirlo y colocarlo en su collar.',
      'qr.share': 'Compartir',
      'qr.downloadPDF': 'Descargar PDF',
      'scanNose.title': 'Escanear Nariz',
      'scanNose.description': 'Apuntá la cámara a la nariz del perro para identificarlo. Asegurate de que la nariz esté bien iluminada y enfocada.',
      'scanNose.step1': 'Acercá el celular a la nariz del perro',
      'scanNose.step2': 'Mantené la cámara estable',
      'scanNose.step3': 'Esperá el resultado de la verificación',
      'scanNose.startScan': 'Iniciar Escaneo',
      'scanNose.scanQRInstead': 'Escanear QR en su lugar',
      'scanNose.errorVerification': 'No se pudo realizar la verificación',
      'scanQR.title': 'Escanear Código QR',
      'scanQR.description': 'Escaneá el código QR del collar del perro para ver su información.',
      'scanQR.openCamera': 'Abrir Cámara QR',
      'scanQR.manualEntry': 'o ingresá el código manualmente',
      'scanQR.qrPlaceholder': 'Código QR (ej: IDC-DOG-00001)',
      'scanQR.enterCode': 'Ingresá un código QR',
      'scanQR.errorSearch': 'No se pudo buscar el código QR',
      'result.matchFound': 'Coincidencia Encontrada',
      'result.noMatch': 'Sin Coincidencia',
      'result.dogData': 'Datos del Perro',
      'result.name': 'Nombre',
      'result.id': 'ID',
      'result.confidence': 'Confianza',
      'result.dailyUsage': 'Uso del día',
      'result.remainingVerifications': 'Te quedan {count} verificaciones hoy',
      'result.unlimitedVerifications': 'Verificaciones ilimitadas',
      'result.newVerification': 'Nueva Verificación',
      'result.dogFoundByQR': 'Perro encontrado por QR',
      'result.dogNotFoundByQR': 'No se encontró un perro con ese código QR',
      'limit.title': 'Límite Diario Alcanzado',
      'limit.description': 'Alcanzaste el máximo de verificaciones gratuitas por hoy.',
      'limit.usageCount': '{used} / {limit} verificaciones usadas',
      'limit.upgradeText': 'Upgrade a Premium para verificaciones ilimitadas y más beneficios.',
      'limit.viewPremium': 'Ver Premium',
      'limit.dailyLimitReached': 'Límite diario alcanzado',
      'vaccineCard.vet': 'Vet',
      'vaccineCard.clinic': 'Clínica',
      'vaccineCard.nextDose': 'Próxima dosis',
      'common.cancel': 'Cancelar',
      'common.save': 'Guardar',
      'common.delete': 'Eliminar',
      'common.search': 'Buscar',
      'common.back': 'Volver',
      'common.close': 'Cerrar',
      'common.error': 'Error',
    },
    en: {
      'auth.subtitle': 'Canine biometric identification',
      'auth.email': 'Email',
      'auth.password': 'Password',
      'auth.confirmPassword': 'Confirm password',
      'auth.fullName': 'Full name',
      'auth.phone': 'Phone (optional)',
      'auth.login': 'Log In',
      'auth.register': 'Create Account',
      'auth.noAccount': "Don't have an account? Sign up",
      'auth.hasAccount': 'I already have an account, log in',
      'auth.fillAllFields': 'Please fill in all fields',
      'auth.fillRequired': 'Please fill in the required fields',
      'auth.passwordMinLength': 'Password must be at least 6 characters',
      'auth.passwordsNoMatch': 'Passwords do not match',
      'nav.createAccount': 'Create Account',
      'nav.myCan': 'My Dog',
      'nav.verify': 'Verify',
      'nav.myDogs': 'My Dogs',
      'nav.addDog': 'Add Dog',
      'nav.profile': 'Profile',
      'nav.vaccines': 'Vaccines',
      'nav.qrCode': 'QR Code',
      'nav.scanNose': 'Scan Nose',
      'nav.scanQR': 'Scan QR',
      'nav.result': 'Result',
      'home.greeting': 'Hello, {name}',
      'home.dogCountOne': '1 registered dog',
      'home.dogCountOther': '{count} registered dogs',
      'home.noDogs': 'No registered dogs',
      'home.noDogsHint': 'Tap the + button to add your first dog',
      'home.errorLoading': 'Error loading dogs',
      'dog.male': 'Male',
      'dog.female': 'Female',
      'dog.noBreed': 'No breed',
      'dog.years': 'years',
      'dog.kg': 'kg',
      'addDog.basicInfo': 'Basic information',
      'addDog.additionalInfo': 'Additional information',
      'addDog.dogName': 'Dog name',
      'addDog.breed': 'Breed',
      'addDog.sex': 'Sex',
      'addDog.origin': 'Origin',
      'addDog.age': 'Age (years)',
      'addDog.weight': 'Weight (kg)',
      'addDog.color': 'Color',
      'addDog.microchip': 'Microchip ID',
      'addDog.behavior': 'Behavior',
      'addDog.likes': 'Likes...',
      'addDog.allergies': 'Allergies',
      'addDog.registerDog': 'Register Dog',
      'addDog.nameRequired': 'Name is required',
      'addDog.success': 'Done',
      'addDog.successMessage': '{name} was registered successfully',
      'addDog.errorRegistering': 'Error registering dog',
      'addDog.adopted': 'Adopted',
      'addDog.purchased': 'Purchased',
      'addDog.rescued': 'Rescued',
      'addDog.other': 'Other',
      'dogProfile.sex': 'Sex',
      'dogProfile.age': 'Age',
      'dogProfile.weight': 'Weight',
      'dogProfile.color': 'Color',
      'dogProfile.origin': 'Origin',
      'dogProfile.microchip': 'Microchip',
      'dogProfile.notes': 'Notes',
      'dogProfile.behaviorLabel': 'Behavior',
      'dogProfile.likesLabel': 'Likes',
      'dogProfile.allergiesLabel': 'Allergies',
      'dogProfile.vaccines': 'Vaccines',
      'dogProfile.qrCode': 'QR Code',
      'dogProfile.registeredOn': 'Registered on {date}',
      'dogProfile.notRegistered': 'Not registered',
      'dogProfile.yearsUnit': '{count} years',
      'dogProfile.kgUnit': '{value} kg',
      'vaccines.title': "{name}'s Vaccines",
      'vaccines.noVaccines': 'No vaccines recorded',
      'vaccines.addVaccine': 'Add Vaccine',
      'vaccines.vaccineType': 'Vaccine type',
      'vaccines.date': 'Date (YYYY-MM-DD)',
      'vaccines.vet': 'Veterinarian',
      'vaccines.clinic': 'Clinic',
      'vaccines.notes': 'Notes',
      'vaccines.deleteTitle': 'Delete vaccine',
      'vaccines.deleteConfirm': 'Are you sure?',
      'vaccines.errorLoading': 'Could not load vaccines',
      'vaccines.errorSaving': 'Error saving',
      'vaccines.errorDeleting': 'Could not delete',
      'vaccines.fillRequired': 'Fill in the vaccine type and date',
      'vaccines.dateFormat': 'Date format: YYYY-MM-DD',
      'vaccines.vaccineTypePlaceholder': 'E.g.: Rabies, DHPP',
      'vaccines.datePlaceholder': '2024-01-15',
      'qr.scanInstruction': 'Scan this QR code to identify {name}. You can print it and attach it to their collar.',
      'qr.share': 'Share',
      'qr.downloadPDF': 'Download PDF',
      'scanNose.title': 'Scan Nose',
      'scanNose.description': "Point the camera at the dog's nose to identify it. Make sure the nose is well lit and in focus.",
      'scanNose.step1': "Bring the phone close to the dog's nose",
      'scanNose.step2': 'Keep the camera steady',
      'scanNose.step3': 'Wait for the verification result',
      'scanNose.startScan': 'Start Scan',
      'scanNose.scanQRInstead': 'Scan QR instead',
      'scanNose.errorVerification': 'Verification failed',
      'scanQR.title': 'Scan QR Code',
      'scanQR.description': "Scan the QR code on the dog's collar to see its information.",
      'scanQR.openCamera': 'Open QR Camera',
      'scanQR.manualEntry': 'or enter the code manually',
      'scanQR.qrPlaceholder': 'QR Code (e.g.: IDC-DOG-00001)',
      'scanQR.enterCode': 'Enter a QR code',
      'scanQR.errorSearch': 'Could not search the QR code',
      'result.matchFound': 'Match Found',
      'result.noMatch': 'No Match',
      'result.dogData': 'Dog Information',
      'result.name': 'Name',
      'result.id': 'ID',
      'result.confidence': 'Confidence',
      'result.dailyUsage': 'Daily usage',
      'result.remainingVerifications': '{count} verifications remaining today',
      'result.unlimitedVerifications': 'Unlimited verifications',
      'result.newVerification': 'New Verification',
      'result.dogFoundByQR': 'Dog found by QR',
      'result.dogNotFoundByQR': 'No dog found with that QR code',
      'limit.title': 'Daily Limit Reached',
      'limit.description': 'You have reached the maximum free verifications for today.',
      'limit.usageCount': '{used} / {limit} verifications used',
      'limit.upgradeText': 'Upgrade to Premium for unlimited verifications and more benefits.',
      'limit.viewPremium': 'View Premium',
      'limit.dailyLimitReached': 'Daily limit reached',
      'vaccineCard.vet': 'Vet',
      'vaccineCard.clinic': 'Clinic',
      'vaccineCard.nextDose': 'Next dose',
      'common.cancel': 'Cancel',
      'common.save': 'Save',
      'common.delete': 'Delete',
      'common.search': 'Search',
      'common.back': 'Back',
      'common.close': 'Close',
      'common.error': 'Error',
    },
    pt: {
      'auth.subtitle': 'Identificação biométrica canina',
      'auth.email': 'Email',
      'auth.password': 'Senha',
      'auth.confirmPassword': 'Confirmar senha',
      'auth.fullName': 'Nome completo',
      'auth.phone': 'Telefone (opcional)',
      'auth.login': 'Entrar',
      'auth.register': 'Criar Conta',
      'auth.noAccount': 'Não tem conta? Cadastre-se',
      'auth.hasAccount': 'Já tenho conta, entrar',
      'auth.fillAllFields': 'Preencha todos os campos',
      'auth.fillRequired': 'Preencha os campos obrigatórios',
      'auth.passwordMinLength': 'A senha deve ter pelo menos 6 caracteres',
      'auth.passwordsNoMatch': 'As senhas não coincidem',
      'nav.createAccount': 'Criar Conta',
      'nav.myCan': 'Meu Cão',
      'nav.verify': 'Verificar',
      'nav.myDogs': 'Meus Cães',
      'nav.addDog': 'Adicionar Cão',
      'nav.profile': 'Perfil',
      'nav.vaccines': 'Vacinas',
      'nav.qrCode': 'Código QR',
      'nav.scanNose': 'Escanear Nariz',
      'nav.scanQR': 'Escanear QR',
      'nav.result': 'Resultado',
      'home.greeting': 'Olá, {name}',
      'home.dogCountOne': '1 cão registrado',
      'home.dogCountOther': '{count} cães registrados',
      'home.noDogs': 'Nenhum cão registrado',
      'home.noDogsHint': 'Toque no botão + para adicionar seu primeiro cão',
      'home.errorLoading': 'Erro ao carregar cães',
      'dog.male': 'Macho',
      'dog.female': 'Fêmea',
      'dog.noBreed': 'Sem raça',
      'dog.years': 'anos',
      'dog.kg': 'kg',
      'addDog.basicInfo': 'Dados básicos',
      'addDog.additionalInfo': 'Informações adicionais',
      'addDog.dogName': 'Nome do cão',
      'addDog.breed': 'Raça',
      'addDog.sex': 'Sexo',
      'addDog.origin': 'Origem',
      'addDog.age': 'Idade (anos)',
      'addDog.weight': 'Peso (kg)',
      'addDog.color': 'Cor',
      'addDog.microchip': 'ID Microchip',
      'addDog.behavior': 'Comportamento',
      'addDog.likes': 'Gosta de...',
      'addDog.allergies': 'Alergias',
      'addDog.registerDog': 'Registrar Cão',
      'addDog.nameRequired': 'Nome é obrigatório',
      'addDog.success': 'Pronto',
      'addDog.successMessage': '{name} foi registrado com sucesso',
      'addDog.errorRegistering': 'Erro ao registrar o cão',
      'addDog.adopted': 'Adotado',
      'addDog.purchased': 'Comprado',
      'addDog.rescued': 'Resgatado',
      'addDog.other': 'Outro',
      'dogProfile.sex': 'Sexo',
      'dogProfile.age': 'Idade',
      'dogProfile.weight': 'Peso',
      'dogProfile.color': 'Cor',
      'dogProfile.origin': 'Origem',
      'dogProfile.microchip': 'Microchip',
      'dogProfile.notes': 'Notas',
      'dogProfile.behaviorLabel': 'Comportamento',
      'dogProfile.likesLabel': 'Gosta de',
      'dogProfile.allergiesLabel': 'Alergias',
      'dogProfile.vaccines': 'Vacinas',
      'dogProfile.qrCode': 'Código QR',
      'dogProfile.registeredOn': 'Registrado em {date}',
      'dogProfile.notRegistered': 'Não registrada',
      'dogProfile.yearsUnit': '{count} anos',
      'dogProfile.kgUnit': '{value} kg',
      'vaccines.title': 'Vacinas de {name}',
      'vaccines.noVaccines': 'Nenhuma vacina registrada',
      'vaccines.addVaccine': 'Adicionar Vacina',
      'vaccines.vaccineType': 'Tipo de vacina',
      'vaccines.date': 'Data (AAAA-MM-DD)',
      'vaccines.vet': 'Veterinário',
      'vaccines.clinic': 'Clínica',
      'vaccines.notes': 'Notas',
      'vaccines.deleteTitle': 'Excluir vacina',
      'vaccines.deleteConfirm': 'Tem certeza?',
      'vaccines.errorLoading': 'Não foi possível carregar as vacinas',
      'vaccines.errorSaving': 'Erro ao salvar',
      'vaccines.errorDeleting': 'Não foi possível excluir',
      'vaccines.fillRequired': 'Preencha o tipo de vacina e a data',
      'vaccines.dateFormat': 'Formato de data: AAAA-MM-DD',
      'vaccines.vaccineTypePlaceholder': 'Ex: Raiva, V8',
      'vaccines.datePlaceholder': '2024-01-15',
      'qr.scanInstruction': 'Escaneie este código QR para identificar {name}. Você pode imprimi-lo e colocá-lo na coleira.',
      'qr.share': 'Compartilhar',
      'qr.downloadPDF': 'Baixar PDF',
      'scanNose.title': 'Escanear Nariz',
      'scanNose.description': 'Aponte a câmera para o nariz do cão para identificá-lo. Certifique-se de que o nariz esteja bem iluminado e em foco.',
      'scanNose.step1': 'Aproxime o celular do nariz do cão',
      'scanNose.step2': 'Mantenha a câmera estável',
      'scanNose.step3': 'Aguarde o resultado da verificação',
      'scanNose.startScan': 'Iniciar Escaneamento',
      'scanNose.scanQRInstead': 'Escanear QR em vez disso',
      'scanNose.errorVerification': 'Não foi possível realizar a verificação',
      'scanQR.title': 'Escanear Código QR',
      'scanQR.description': 'Escaneie o código QR na coleira do cão para ver suas informações.',
      'scanQR.openCamera': 'Abrir Câmera QR',
      'scanQR.manualEntry': 'ou digite o código manualmente',
      'scanQR.qrPlaceholder': 'Código QR (ex: IDC-DOG-00001)',
      'scanQR.enterCode': 'Digite um código QR',
      'scanQR.errorSearch': 'Não foi possível buscar o código QR',
      'result.matchFound': 'Correspondência Encontrada',
      'result.noMatch': 'Sem Correspondência',
      'result.dogData': 'Dados do Cão',
      'result.name': 'Nome',
      'result.id': 'ID',
      'result.confidence': 'Confiança',
      'result.dailyUsage': 'Uso do dia',
      'result.remainingVerifications': '{count} verificações restantes hoje',
      'result.unlimitedVerifications': 'Verificações ilimitadas',
      'result.newVerification': 'Nova Verificação',
      'result.dogFoundByQR': 'Cão encontrado por QR',
      'result.dogNotFoundByQR': 'Nenhum cão encontrado com esse código QR',
      'limit.title': 'Limite Diário Atingido',
      'limit.description': 'Você atingiu o máximo de verificações gratuitas por hoje.',
      'limit.usageCount': '{used} / {limit} verificações usadas',
      'limit.upgradeText': 'Faça upgrade para Premium para verificações ilimitadas e mais benefícios.',
      'limit.viewPremium': 'Ver Premium',
      'limit.dailyLimitReached': 'Limite diário atingido',
      'vaccineCard.vet': 'Vet',
      'vaccineCard.clinic': 'Clínica',
      'vaccineCard.nextDose': 'Próxima dose',
      'common.cancel': 'Cancelar',
      'common.save': 'Salvar',
      'common.delete': 'Excluir',
      'common.search': 'Buscar',
      'common.back': 'Voltar',
      'common.close': 'Fechar',
      'common.error': 'Erro',
    },
  };

  function t(key, params) {
    const str = (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key]) || key;
    if (!params) return str;
    return str.replace(/\{(\w+)\}/g, (_, k) => (params[k] != null ? params[k] : ''));
  }

  // ── Helpers ─────────────────────────────────────────────
  function $(sel) { return document.querySelector(sel); }
  function $$(sel) { return document.querySelectorAll(sel); }

  function esc(str) {
    if (!str) return '';
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function formatDate(iso) {
    if (!iso) return '-';
    const locales = { es: 'es-AR', en: 'en-US', pt: 'pt-BR' };
    return new Date(iso).toLocaleDateString(locales[currentLang] || 'es-AR', {
      year: 'numeric', month: 'short', day: 'numeric',
    });
  }

  function showAlert(id, msg) {
    const el = $(id);
    if (!el) return;
    el.textContent = msg;
    el.classList.add('visible');
  }

  function hideAlert(id) {
    const el = $(id);
    if (el) el.classList.remove('visible');
  }

  function showSnackbar(msg, duration) {
    const el = $('#snackbar');
    el.textContent = msg;
    el.classList.add('visible');
    setTimeout(() => el.classList.remove('visible'), duration || 3000);
  }

  // ── API Client ──────────────────────────────────────────
  async function api(path, options) {
    options = options || {};
    const headers = options.headers || {};
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json';
    }
    if (token) headers['Authorization'] = 'Bearer ' + token;

    const res = await fetch(API_BASE + path, { ...options, headers });
    if (res.status === 401) {
      logout();
      throw new Error('Session expired');
    }
    if (!res.ok) {
      const body = await res.json().catch(function () { return {}; });
      const err = new Error(typeof body.detail === 'string' ? body.detail : (body.detail && body.detail.error) || 'Request failed');
      err.status = res.status;
      err.detail = body.detail;
      throw err;
    }
    if (res.status === 204) return null;
    return res.json();
  }

  // ── Auth ────────────────────────────────────────────────
  function showAuthScreen() {
    $('#auth-screen').style.display = 'block';
    $('#app-screen').style.display = 'none';
    $('#login-view').style.display = 'flex';
    $('#register-view').style.display = 'none';
  }

  function showAppScreen() {
    $('#auth-screen').style.display = 'none';
    $('#app-screen').style.display = 'block';
  }

  async function handleLogin(e) {
    e.preventDefault();
    hideAlert('#login-error');
    const email = $('#login-email').value.trim();
    const password = $('#login-password').value;

    if (!email || !password) {
      showAlert('#login-error', t('auth.fillAllFields'));
      return;
    }

    try {
      $('#login-btn').disabled = true;
      const data = await api('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email: email, password: password }),
      });
      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem('identican_token', token);
      showAppScreen();
      initApp();
    } catch (err) {
      showAlert('#login-error', err.message || t('auth.fillAllFields'));
    } finally {
      $('#login-btn').disabled = false;
    }
  }

  async function handleRegister(e) {
    e.preventDefault();
    hideAlert('#register-error');
    const name = $('#reg-name').value.trim();
    const email = $('#reg-email').value.trim();
    const phone = $('#reg-phone').value.trim();
    const password = $('#reg-password').value;
    const confirm = $('#reg-confirm-password').value;

    if (!name || !email || !password) {
      showAlert('#register-error', t('auth.fillRequired'));
      return;
    }
    if (password.length < 6) {
      showAlert('#register-error', t('auth.passwordMinLength'));
      return;
    }
    if (password !== confirm) {
      showAlert('#register-error', t('auth.passwordsNoMatch'));
      return;
    }

    try {
      $('#register-btn').disabled = true;
      const data = await api('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify({ email: email, password: password, name: name, phone: phone || null }),
      });
      token = data.access_token;
      currentUser = data.user;
      localStorage.setItem('identican_token', token);
      showAppScreen();
      initApp();
    } catch (err) {
      showAlert('#register-error', err.message || t('auth.fillRequired'));
    } finally {
      $('#register-btn').disabled = false;
    }
  }

  function logout() {
    token = null;
    currentUser = null;
    localStorage.removeItem('identican_token');
    showAuthScreen();
    $('#login-password').value = '';
  }

  // ── i18n ────────────────────────────────────────────────
  function applyTranslations() {
    $$('[data-i18n]').forEach(function (el) {
      el.textContent = t(el.dataset.i18n);
    });
  }

  function renderLangSelectors() {
    var langs = ['es', 'en', 'pt'];
    var html = langs.map(function (l) {
      return '<button class="lang-btn' + (l === currentLang ? ' active' : '') + '" data-lang="' + l + '">' + l.toUpperCase() + '</button>';
    }).join('');

    $$('.lang-selector').forEach(function (el) {
      el.innerHTML = html;
    });

    $$('.lang-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        currentLang = btn.dataset.lang;
        localStorage.setItem('identican_lang', currentLang);
        renderLangSelectors();
        applyTranslations();
        // Re-render current dynamic content
        if (currentUser && $('#app-screen').style.display !== 'none') {
          updateHomeHeader();
          updateHeaderTitle();
        }
      });
    });
  }

  // ── Navigation ──────────────────────────────────────────
  function navigateTo(screen, opts) {
    opts = opts || {};
    if (!opts.isBack) {
      screenHistory.push(currentScreen);
    }
    currentScreen = screen;

    // Hide all screens
    $$('.screen').forEach(function (s) { s.style.display = 'none'; });

    var el = $('#screen-' + screen);
    if (el) el.style.display = 'block';

    // Back button
    var backBtn = $('#back-btn');
    var showBack = screenHistory.length > 0 && screen !== 'home' && screen !== 'scan-nose';
    backBtn.style.display = showBack ? 'block' : 'none';

    // Update header title
    updateHeaderTitle();

    // Show/hide FABs
    $('#add-dog-fab').style.display = screen === 'home' ? 'flex' : 'none';
    var vaxFab = $('#add-vaccine-fab');
    if (vaxFab) vaxFab.style.display = screen === 'vaccines' ? 'flex' : 'none';

    // Load screen data
    if (screen === 'home') loadDogs();
    if (screen === 'dog-profile' && currentDog) renderDogProfile();
    if (screen === 'vaccines' && currentDog) loadVaccines();
    if (screen === 'qr' && currentDog) renderQR();
    if (screen === 'result' && currentResult) renderResult();
  }

  function goBack() {
    if (screenHistory.length > 0) {
      var prev = screenHistory.pop();
      navigateTo(prev, { isBack: true });
    }
  }

  function switchTab(tab) {
    currentTab = tab;
    screenHistory = [];

    $$('.tab-btn').forEach(function (btn) {
      btn.classList.toggle('active', btn.dataset.tab === tab);
    });

    if (tab === 'mican') {
      navigateTo('home', { isBack: true });
    } else if (tab === 'verificador') {
      navigateTo('scan-nose', { isBack: true });
    }
  }

  function updateHeaderTitle() {
    var titles = {
      'home': t('nav.myDogs'),
      'add-dog': t('nav.addDog'),
      'dog-profile': t('nav.profile'),
      'vaccines': t('nav.vaccines'),
      'qr': t('nav.qrCode'),
      'scan-nose': t('nav.scanNose'),
      'scan-qr': t('nav.scanQR'),
      'result': t('nav.result'),
    };
    $('#header-title').textContent = titles[currentScreen] || 'IdentiCan';
  }

  // ── App Init ────────────────────────────────────────────
  async function initApp() {
    if (!currentUser) {
      try {
        currentUser = await api('/api/auth/me');
      } catch (e) {
        logout();
        return;
      }
    }
    switchTab('mican');
  }

  // ── Home Screen (My Dogs) ──────────────────────────────
  function updateHomeHeader() {
    if (!currentUser) return;
    $('#home-greeting').textContent = t('home.greeting', { name: currentUser.name });
  }

  async function loadDogs() {
    updateHomeHeader();
    $('#home-loading').style.display = 'flex';
    $('#dogs-list').innerHTML = '';
    $('#dogs-empty').style.display = 'none';
    $('#home-dog-count').textContent = '';

    try {
      var dogs = await api('/api/dogs');
      $('#home-loading').style.display = 'none';

      if (!dogs.length) {
        $('#dogs-empty').style.display = 'block';
        $('#home-dog-count').textContent = t('home.dogCountOther', { count: 0 });
        return;
      }

      $('#home-dog-count').textContent = dogs.length === 1
        ? t('home.dogCountOne')
        : t('home.dogCountOther', { count: dogs.length });

      $('#dogs-list').innerHTML = dogs.map(function (dog) {
        var sexLabel = dog.sex === 'M' ? t('dog.male') : t('dog.female');
        var details = sexLabel;
        if (dog.age_years) details += ' &middot; ' + dog.age_years + ' ' + t('dog.years');
        if (dog.weight_kg) details += ' &middot; ' + dog.weight_kg + ' ' + t('dog.kg');

        return '<div class="dog-card" data-dog-id="' + dog.id + '">' +
          '<div class="dog-card-name">' + esc(dog.name) + '</div>' +
          '<div class="dog-card-breed">' + esc(dog.breed || t('dog.noBreed')) + '</div>' +
          '<div class="dog-card-qr">&#9642; ' + esc(dog.qr_code) + '</div>' +
          '<div class="dog-card-details">' + details + '</div>' +
          '</div>';
      }).join('');

      // Attach click handlers
      $$('.dog-card').forEach(function (card) {
        card.addEventListener('click', function () {
          var dogId = parseInt(card.dataset.dogId);
          var dog = dogs.find(function (d) { return d.id === dogId; });
          if (dog) {
            currentDog = dog;
            navigateTo('dog-profile');
          }
        });
      });
    } catch (err) {
      $('#home-loading').style.display = 'none';
      showSnackbar(t('home.errorLoading'));
    }
  }

  // ── Add Dog Screen ─────────────────────────────────────
  function getSegmentValue(groupId) {
    var active = $('#' + groupId + ' .segment-btn.active');
    return active ? active.dataset.value : '';
  }

  function resetAddDogForm() {
    $('#dog-name').value = '';
    $('#dog-breed').value = '';
    $('#dog-age').value = '';
    $('#dog-weight').value = '';
    $('#dog-color').value = '';
    $('#dog-microchip').value = '';
    $('#dog-behavior').value = '';
    $('#dog-likes').value = '';
    $('#dog-allergies').value = '';
    hideAlert('#add-dog-error');

    // Reset segments
    $$('#dog-sex-group .segment-btn').forEach(function (b, i) {
      b.classList.toggle('active', i === 0);
    });
    $$('#dog-origin-group .segment-btn').forEach(function (b, i) {
      b.classList.toggle('active', i === 0);
    });
  }

  async function handleAddDog() {
    hideAlert('#add-dog-error');
    var name = $('#dog-name').value.trim();
    if (!name) {
      showAlert('#add-dog-error', t('addDog.nameRequired'));
      return;
    }

    var data = {
      name: name,
      breed: $('#dog-breed').value.trim() || null,
      sex: getSegmentValue('dog-sex-group'),
      origin: getSegmentValue('dog-origin-group'),
      age_years: $('#dog-age').value ? parseInt($('#dog-age').value) : null,
      weight_kg: $('#dog-weight').value ? parseFloat($('#dog-weight').value) : null,
      color: $('#dog-color').value.trim() || null,
      microchip_id: $('#dog-microchip').value.trim() || null,
      behavior_notes: $('#dog-behavior').value.trim() || null,
      likes: $('#dog-likes').value.trim() || null,
      allergies: $('#dog-allergies').value.trim() || null,
    };

    try {
      $('#submit-dog-btn').disabled = true;
      await api('/api/dogs', { method: 'POST', body: JSON.stringify(data) });
      showSnackbar(t('addDog.successMessage', { name: name }));
      resetAddDogForm();
      goBack();
    } catch (err) {
      showAlert('#add-dog-error', err.message || t('addDog.errorRegistering'));
    } finally {
      $('#submit-dog-btn').disabled = false;
    }
  }

  // ── Dog Profile Screen ─────────────────────────────────
  async function renderDogProfile() {
    // Refresh dog data
    try {
      currentDog = await api('/api/dogs/' + currentDog.id);
    } catch (e) {
      // keep existing data
    }

    var dog = currentDog;
    var sexLabel = dog.sex === 'M' ? t('dog.male') : t('dog.female');
    var ageStr = dog.age_years ? t('dogProfile.yearsUnit', { count: dog.age_years }) : '-';
    var weightStr = dog.weight_kg ? t('dogProfile.kgUnit', { value: dog.weight_kg }) : '-';

    var notesHtml = '';
    if (dog.behavior_notes || dog.likes || dog.allergies) {
      notesHtml = '<div class="notes-card"><h3 class="section-title">' + esc(t('dogProfile.notes')) + '</h3>';
      if (dog.behavior_notes) notesHtml += '<div class="note-item"><div class="note-label">' + esc(t('dogProfile.behaviorLabel')) + '</div><div class="note-value">' + esc(dog.behavior_notes) + '</div></div>';
      if (dog.likes) notesHtml += '<div class="note-item"><div class="note-label">' + esc(t('dogProfile.likesLabel')) + '</div><div class="note-value">' + esc(dog.likes) + '</div></div>';
      if (dog.allergies) notesHtml += '<div class="note-item"><div class="note-label">' + esc(t('dogProfile.allergiesLabel')) + '</div><div class="note-value">' + esc(dog.allergies) + '</div></div>';
      notesHtml += '</div>';
    }

    $('#dog-profile-content').innerHTML =
      '<div class="profile-header-card">' +
        '<div class="profile-header-row">' +
          '<div>' +
            '<div class="profile-dog-name">' + esc(dog.name) + '</div>' +
            '<div class="profile-breed">' + esc(dog.breed || t('dog.noBreed')) + '</div>' +
          '</div>' +
          '<div class="profile-qr-chip">&#9642; ' + esc(dog.qr_code) + '</div>' +
        '</div>' +
        '<hr class="profile-divider" />' +
        '<div class="details-grid">' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.sex')) + '</div><div class="detail-cell-value">' + esc(sexLabel) + '</div></div>' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.age')) + '</div><div class="detail-cell-value">' + esc(ageStr) + '</div></div>' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.weight')) + '</div><div class="detail-cell-value">' + esc(weightStr) + '</div></div>' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.color')) + '</div><div class="detail-cell-value">' + esc(dog.color || '-') + '</div></div>' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.origin')) + '</div><div class="detail-cell-value">' + esc(dog.origin || '-') + '</div></div>' +
          '<div class="detail-cell"><div class="detail-cell-label">' + esc(t('dogProfile.microchip')) + '</div><div class="detail-cell-value">' + esc(dog.microchip_id || '-') + '</div></div>' +
        '</div>' +
      '</div>' +
      notesHtml +
      '<div class="profile-actions">' +
        '<button class="btn btn-primary" id="profile-vaccines-btn">&#128137; ' + esc(t('dogProfile.vaccines')) + '</button>' +
        '<button class="btn btn-secondary" id="profile-qr-btn">&#9642; ' + esc(t('dogProfile.qrCode')) + '</button>' +
      '</div>' +
      '<div class="profile-footer">' + esc(t('dogProfile.registeredOn', { date: formatDate(dog.created_at) })) + '</div>';

    $('#profile-vaccines-btn').addEventListener('click', function () {
      navigateTo('vaccines');
    });
    $('#profile-qr-btn').addEventListener('click', function () {
      navigateTo('qr');
    });
  }

  // ── Vaccines Screen ────────────────────────────────────
  async function loadVaccines() {
    var dog = currentDog;
    $('#vaccines-content').innerHTML = '<div class="vaccines-title">' + esc(t('vaccines.title', { name: dog.name })) + '</div><div class="loading-center"><div class="spinner"></div></div>';

    try {
      var vaccines = await api('/api/vaccines/dog/' + dog.id);
      currentDogVaccines = vaccines;
      renderVaccines(vaccines);
    } catch (err) {
      showSnackbar(t('vaccines.errorLoading'));
    }
  }

  function renderVaccines(vaccines) {
    var dog = currentDog;
    var titleHtml = '<div class="vaccines-title">' + esc(t('vaccines.title', { name: dog.name })) + '</div>';

    if (!vaccines.length) {
      $('#vaccines-content').innerHTML = titleHtml +
        '<div class="empty-state">' +
          '<div class="empty-icon">&#128137;</div>' +
          '<div class="empty-title">' + esc(t('vaccines.noVaccines')) + '</div>' +
        '</div>';
      return;
    }

    var listHtml = vaccines.map(function (v) {
      var html = '<div class="vaccine-card">' +
        '<div class="vaccine-header">' +
          '<div>' +
            '<div class="vaccine-type">' + esc(v.vaccine_type) + '</div>' +
            '<div class="vaccine-date">' + formatDate(v.vaccine_date) + '</div>' +
          '</div>' +
          '<button class="vaccine-delete-btn" data-vax-id="' + v.id + '" title="Delete">&#128465;</button>' +
        '</div>';
      if (v.veterinarian_name) html += '<div class="vaccine-detail">' + esc(t('vaccineCard.vet')) + ': ' + esc(v.veterinarian_name) + '</div>';
      if (v.clinic_name) html += '<div class="vaccine-detail">' + esc(t('vaccineCard.clinic')) + ': ' + esc(v.clinic_name) + '</div>';
      if (v.next_dose_date) html += '<div class="vaccine-next-dose">' + esc(t('vaccineCard.nextDose')) + ': ' + formatDate(v.next_dose_date) + '</div>';
      if (v.notes) html += '<div class="vaccine-notes">' + esc(v.notes) + '</div>';
      html += '</div>';
      return html;
    }).join('');

    $('#vaccines-content').innerHTML = titleHtml + '<div class="vaccines-list">' + listHtml + '</div>';

    // Delete handlers
    $$('.vaccine-delete-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        deleteVaccineId = parseInt(btn.dataset.vaxId);
        $('#delete-modal').classList.add('active');
      });
    });
  }

  async function handleAddVaccine() {
    var type = $('#vax-type').value.trim();
    var date = $('#vax-date').value.trim();

    if (!type || !date) {
      showSnackbar(t('vaccines.fillRequired'));
      return;
    }

    try {
      $('#vax-save-btn').disabled = true;
      await api('/api/vaccines', {
        method: 'POST',
        body: JSON.stringify({
          dog_id: currentDog.id,
          vaccine_type: type,
          vaccine_date: date,
          veterinarian_name: $('#vax-vet').value.trim() || null,
          clinic_name: $('#vax-clinic').value.trim() || null,
          notes: $('#vax-notes').value.trim() || null,
        }),
      });
      $('#vaccine-modal').classList.remove('active');
      resetVaccineForm();
      loadVaccines();
    } catch (err) {
      showSnackbar(err.message || t('vaccines.errorSaving'));
    } finally {
      $('#vax-save-btn').disabled = false;
    }
  }

  async function handleDeleteVaccine() {
    if (!deleteVaccineId) return;
    try {
      await api('/api/vaccines/' + deleteVaccineId, { method: 'DELETE' });
      $('#delete-modal').classList.remove('active');
      deleteVaccineId = null;
      loadVaccines();
    } catch (err) {
      showSnackbar(t('vaccines.errorDeleting'));
    }
  }

  function resetVaccineForm() {
    $('#vax-type').value = '';
    $('#vax-date').value = '';
    $('#vax-vet').value = '';
    $('#vax-clinic').value = '';
    $('#vax-notes').value = '';
  }

  // ── QR Screen ──────────────────────────────────────────
  function renderQR() {
    var dog = currentDog;
    $('#qr-content').innerHTML =
      '<div class="qr-card">' +
        '<div class="qr-dog-name">' + esc(dog.name) + '</div>' +
        '<div class="qr-code-label">' + esc(dog.qr_code) + '</div>' +
        '<div class="qr-image-wrapper" id="qr-canvas-holder"></div>' +
        '<div class="qr-instructions">' + esc(t('qr.scanInstruction', { name: dog.name })) + '</div>' +
      '</div>' +
      '<div class="qr-actions">' +
        '<a href="' + API_BASE + '/api/qr/generate/' + dog.id + '" target="_blank" class="btn btn-primary btn-full">' + esc(t('qr.share')) + '</a>' +
        '<a href="' + API_BASE + '/api/qr/pdf/' + dog.id + '" target="_blank" class="btn btn-outline btn-full">' + esc(t('qr.downloadPDF')) + '</a>' +
      '</div>';

    // Render QR code using canvas (simple implementation)
    renderQRCanvas(dog.qr_code, 'qr-canvas-holder');
  }

  function renderQRCanvas(text, containerId) {
    var container = document.getElementById(containerId);
    if (!container) return;

    // Simple QR code rendering using a pattern-based approach
    // We'll create a canvas with the QR code text rendered as a visual code
    var canvas = document.createElement('canvas');
    var size = 250;
    canvas.width = size;
    canvas.height = size;
    var ctx = canvas.getContext('2d');

    // White background
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, 0, size, size);

    // Simple visual representation - generate a deterministic pattern from the text
    var cellSize = 10;
    var modules = Math.floor(size / cellSize);
    ctx.fillStyle = '#000000';

    // Generate a hash-based pattern
    var hash = 0;
    for (var i = 0; i < text.length; i++) {
      hash = ((hash << 5) - hash + text.charCodeAt(i)) | 0;
    }

    // Draw finder patterns (3 corners)
    drawFinderPattern(ctx, 0, 0, cellSize);
    drawFinderPattern(ctx, (modules - 7) * cellSize, 0, cellSize);
    drawFinderPattern(ctx, 0, (modules - 7) * cellSize, cellSize);

    // Draw data area with deterministic pattern
    var seed = Math.abs(hash);
    for (var row = 0; row < modules; row++) {
      for (var col = 0; col < modules; col++) {
        // Skip finder pattern areas
        if ((row < 8 && col < 8) || (row < 8 && col >= modules - 8) || (row >= modules - 8 && col < 8)) continue;
        // Generate pseudo-random but deterministic pattern
        seed = (seed * 1103515245 + 12345) & 0x7fffffff;
        if (seed % 3 !== 0) {
          ctx.fillRect(col * cellSize, row * cellSize, cellSize, cellSize);
        }
      }
    }

    // Draw text label at bottom
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(0, size - 20, size, 20);
    ctx.fillStyle = '#000000';
    ctx.font = '11px monospace';
    ctx.textAlign = 'center';
    ctx.fillText(text, size / 2, size - 6);

    container.innerHTML = '';
    container.appendChild(canvas);
  }

  function drawFinderPattern(ctx, x, y, cellSize) {
    // Outer square
    ctx.fillStyle = '#000000';
    ctx.fillRect(x, y, 7 * cellSize, 7 * cellSize);
    // Inner white
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(x + cellSize, y + cellSize, 5 * cellSize, 5 * cellSize);
    // Inner black
    ctx.fillStyle = '#000000';
    ctx.fillRect(x + 2 * cellSize, y + 2 * cellSize, 3 * cellSize, 3 * cellSize);
  }

  // ── Scan Nose Screen ───────────────────────────────────
  async function handleNoseScan() {
    // Create a mock file for the API call (matching mobile behavior)
    var btn = $('#start-nose-scan-btn');
    btn.disabled = true;

    try {
      // Use file input for selecting a nose image
      var fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = 'image/*';

      var fileSelected = await new Promise(function (resolve) {
        fileInput.addEventListener('change', function () {
          resolve(fileInput.files[0] || null);
        });
        // Also handle cancel
        fileInput.addEventListener('cancel', function () { resolve(null); });
        fileInput.click();
        // Timeout fallback for cancel
        setTimeout(function () { resolve(fileInput.files[0] || null); }, 60000);
      });

      if (!fileSelected) {
        btn.disabled = false;
        return;
      }

      var formData = new FormData();
      formData.append('file', fileSelected);

      var response = await api('/api/nose/verify', {
        method: 'POST',
        body: formData,
      });

      currentResult = response;
      navigateTo('result');
    } catch (err) {
      if (err.status === 429) {
        var detail = err.detail;
        showLimitModal(detail);
      } else {
        showSnackbar(t('scanNose.errorVerification'));
      }
    } finally {
      btn.disabled = false;
    }
  }

  function showLimitModal(detail) {
    var usageBar = $('#limit-usage-bar');
    if (detail && typeof detail === 'object') {
      var used = detail.verifications_used || 3;
      var limit = detail.verifications_limit || 3;
      usageBar.innerHTML =
        '<div class="limit-usage-text">' + esc(t('limit.usageCount', { used: used, limit: limit })) + '</div>' +
        '<div class="limit-progress-bar"><div class="limit-progress-fill"></div></div>';
    } else {
      usageBar.innerHTML = '';
    }
    $('#limit-modal').classList.add('active');
  }

  // ── Scan QR Screen ─────────────────────────────────────
  async function handleQRSearch() {
    var code = $('#qr-manual-input').value.trim().toUpperCase();
    if (!code) {
      showSnackbar(t('scanQR.enterCode'));
      return;
    }

    try {
      $('#qr-search-btn').disabled = true;
      var dogs = await api('/api/dogs');
      var found = dogs.find(function (d) { return d.qr_code === code; });

      if (found) {
        currentResult = {
          match: true,
          confidence: 1.0,
          dog_id: found.id,
          dog_name: found.name,
          verification_type: 'qr_scan',
          message: t('result.dogFoundByQR'),
        };
      } else {
        currentResult = {
          match: false,
          confidence: 0,
          dog_id: null,
          dog_name: null,
          verification_type: 'qr_scan',
          message: t('result.dogNotFoundByQR'),
        };
      }
      navigateTo('result');
    } catch (err) {
      showSnackbar(t('scanQR.errorSearch'));
    } finally {
      $('#qr-search-btn').disabled = false;
      $('#qr-manual-input').value = '';
    }
  }

  // ── Result Screen ──────────────────────────────────────
  function renderResult() {
    var r = currentResult;
    var isMatch = r.match;

    var html = '<div class="result-main-card ' + (isMatch ? 'match' : 'no-match') + '">' +
      '<div class="result-icon">' + (isMatch ? '&#9989;' : '&#10060;') + '</div>' +
      '<div class="result-title">' + esc(isMatch ? t('result.matchFound') : t('result.noMatch')) + '</div>' +
      '<div class="result-message">' + esc(r.message || '') + '</div>' +
      '</div>';

    if (isMatch && r.dog_name) {
      html += '<div class="result-detail-card">' +
        '<div class="result-detail-title">' + esc(t('result.dogData')) + '</div>' +
        '<hr class="result-detail-divider" />' +
        '<div class="result-detail-row"><span class="result-detail-label">' + esc(t('result.name')) + '</span><span class="result-detail-value">' + esc(r.dog_name) + '</span></div>' +
        '<div class="result-detail-row"><span class="result-detail-label">' + esc(t('result.id')) + '</span><span class="result-detail-value">' + (r.dog_id || '-') + '</span></div>';
      if (r.confidence) {
        html += '<div class="result-detail-row"><span class="result-detail-label">' + esc(t('result.confidence')) + '</span><span class="result-detail-value">' + (r.confidence * 100).toFixed(1) + '%</span></div>';
      }
      html += '</div>';
    }

    if (r.verification_usage) {
      html += '<div class="result-usage-card">' +
        '<div class="result-usage-title">' + esc(t('result.dailyUsage')) + '</div>' +
        '<div class="result-usage-text">' +
          (r.verification_usage.remaining !== null
            ? esc(t('result.remainingVerifications', { count: r.verification_usage.remaining }))
            : esc(t('result.unlimitedVerifications'))) +
        '</div></div>';
    }

    html += '<div class="result-actions">' +
      '<button class="btn btn-primary btn-full" id="result-new-btn">' + esc(t('result.newVerification')) + '</button>' +
      '<button class="btn btn-outline btn-full" id="result-back-btn">' + esc(t('common.back')) + '</button>' +
      '</div>';

    $('#result-content').innerHTML = html;

    $('#result-new-btn').addEventListener('click', function () {
      screenHistory = [];
      navigateTo('scan-nose', { isBack: true });
    });
    $('#result-back-btn').addEventListener('click', function () {
      goBack();
    });
  }

  // ── Segment Group Setup ─────────────────────────────────
  function initSegmentGroups() {
    $$('.segment-group').forEach(function (group) {
      group.querySelectorAll('.segment-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
          group.querySelectorAll('.segment-btn').forEach(function (b) {
            b.classList.remove('active');
          });
          btn.classList.add('active');
        });
      });
    });
  }

  // ── Password Toggle ─────────────────────────────────────
  function initPasswordToggles() {
    $$('.toggle-password').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var input = document.getElementById(btn.dataset.target);
        if (input) {
          input.type = input.type === 'password' ? 'text' : 'password';
        }
      });
    });
  }

  // ── Boot ────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', function () {
    // Language
    renderLangSelectors();
    applyTranslations();

    // Auth forms
    $('#login-form').addEventListener('submit', handleLogin);
    $('#register-form').addEventListener('submit', handleRegister);
    $('#goto-register').addEventListener('click', function () {
      hideAlert('#login-error');
      $('#login-view').style.display = 'none';
      $('#register-view').style.display = 'flex';
    });
    $('#goto-login').addEventListener('click', function () {
      hideAlert('#register-error');
      $('#register-view').style.display = 'none';
      $('#login-view').style.display = 'flex';
    });

    // Password toggles
    initPasswordToggles();

    // Logout
    $('#logout-btn').addEventListener('click', logout);

    // Back button
    $('#back-btn').addEventListener('click', goBack);

    // Tabs
    $$('.tab-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        switchTab(btn.dataset.tab);
      });
    });

    // Add Dog FAB
    $('#add-dog-fab').addEventListener('click', function () {
      resetAddDogForm();
      navigateTo('add-dog');
    });

    // Submit Dog
    $('#submit-dog-btn').addEventListener('click', handleAddDog);

    // Segment groups
    initSegmentGroups();

    // Nose scan
    $('#start-nose-scan-btn').addEventListener('click', handleNoseScan);

    // Go to QR scan
    $('#goto-scan-qr-btn').addEventListener('click', function () {
      navigateTo('scan-qr');
    });

    // QR camera (placeholder)
    $('#open-qr-camera-btn').addEventListener('click', function () {
      showSnackbar('QR camera coming soon. Use manual search.');
    });

    // QR manual search
    $('#qr-search-btn').addEventListener('click', handleQRSearch);
    $('#qr-manual-input').addEventListener('keydown', function (e) {
      if (e.key === 'Enter') handleQRSearch();
    });

    // Vaccine modal
    $('#add-vaccine-fab').addEventListener('click', function () {
      resetVaccineForm();
      $('#vaccine-modal').classList.add('active');
    });
    $('#vaccine-modal-close').addEventListener('click', function () {
      $('#vaccine-modal').classList.remove('active');
    });
    $('#vax-cancel-btn').addEventListener('click', function () {
      $('#vaccine-modal').classList.remove('active');
    });
    $('#vax-save-btn').addEventListener('click', handleAddVaccine);

    // Delete modal
    $('#delete-cancel-btn').addEventListener('click', function () {
      $('#delete-modal').classList.remove('active');
      deleteVaccineId = null;
    });
    $('#delete-confirm-btn').addEventListener('click', handleDeleteVaccine);

    // Limit modal
    $('#limit-premium-btn').addEventListener('click', function () {
      $('#limit-modal').classList.remove('active');
    });
    $('#limit-close-btn').addEventListener('click', function () {
      $('#limit-modal').classList.remove('active');
    });
    $('#limit-modal').addEventListener('click', function (e) {
      if (e.target === $('#limit-modal')) $('#limit-modal').classList.remove('active');
    });

    // Modal overlay clicks
    $$('.modal-overlay').forEach(function (overlay) {
      overlay.addEventListener('click', function (e) {
        if (e.target === overlay) overlay.classList.remove('active');
      });
    });

    // Check token
    if (token) {
      showAppScreen();
      initApp();
    } else {
      showAuthScreen();
    }
  });
})();
