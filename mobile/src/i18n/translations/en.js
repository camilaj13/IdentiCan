export default {
  // Common
  common: {
    appName: 'IdentiCan',
    loading: 'Loading...',
    error: 'Error',
    cancel: 'Cancel',
    save: 'Save',
    delete: 'Delete',
    search: 'Search',
    back: 'Back',
    ok: 'OK',
    close: 'Close',
    share: 'Share',
    or: 'or',
    yes: 'Yes',
    no: 'No',
  },

  // Language names
  languages: {
    es: 'Español',
    en: 'English',
    pt: 'Português',
    selectLanguage: 'Language',
  },

  // Auth
  auth: {
    login: 'Log In',
    register: 'Create Account',
    logout: 'Log Out',
    email: 'Email',
    password: 'Password',
    confirmPassword: 'Confirm password',
    fullName: 'Full name',
    phone: 'Phone (optional)',
    subtitle: 'Canine biometric identification',
    noAccount: "Don't have an account? Sign up",
    hasAccount: 'I already have an account, log in',
    fillAllFields: 'Please fill in all fields',
    fillRequired: 'Please fill in the required fields',
    passwordMinLength: 'Password must be at least 6 characters',
    passwordsNoMatch: 'Passwords do not match',
    loginError: 'Login failed',
    registerError: 'Registration failed',
  },

  // Navigation & Tabs
  nav: {
    myDogs: 'My Dogs',
    verify: 'Verify',
    myCan: 'My Dog',
    addDog: 'Add Dog',
    profile: 'Profile',
    vaccines: 'Vaccines',
    qrCode: 'QR Code',
    scanNose: 'Scan Nose',
    scanQR: 'Scan QR',
    result: 'Result',
    createAccount: 'Create Account',
    settings: 'Settings',
  },

  // Home Screen
  home: {
    greeting: 'Hello, {{name}}',
    dogCount: '{{count}} registered dog(s)',
    dogCountOne: '1 registered dog',
    dogCountOther: '{{count}} registered dogs',
    noDogs: 'No registered dogs',
    noDogsHint: 'Tap the + button to add your first dog',
    errorLoading: 'Error loading dogs',
  },

  // Dog Card
  dog: {
    male: 'Male',
    female: 'Female',
    noBreed: 'No breed',
    years: 'years',
    kg: 'kg',
  },

  // Add Dog
  addDog: {
    basicInfo: 'Basic information',
    additionalInfo: 'Additional information',
    dogName: 'Dog name',
    breed: 'Breed',
    sex: 'Sex',
    origin: 'Origin',
    age: 'Age (years)',
    weight: 'Weight (kg)',
    color: 'Color',
    microchip: 'Microchip ID',
    behavior: 'Behavior',
    likes: 'Likes...',
    allergies: 'Allergies',
    registerDog: 'Register Dog',
    nameRequired: 'Name is required',
    success: 'Done',
    successMessage: '{{name}} was registered successfully',
    errorRegistering: 'Error registering dog',
    adopted: 'Adopted',
    purchased: 'Purchased',
    rescued: 'Rescued',
    other: 'Other',
  },

  // Dog Profile
  dogProfile: {
    sex: 'Sex',
    age: 'Age',
    weight: 'Weight',
    color: 'Color',
    origin: 'Origin',
    microchip: 'Microchip',
    notes: 'Notes',
    behaviorLabel: 'Behavior',
    likesLabel: 'Likes',
    allergiesLabel: 'Allergies',
    vaccines: 'Vaccines',
    qrCode: 'QR Code',
    registeredOn: 'Registered on {{date}}',
    notRegistered: 'Not registered',
    yearsUnit: '{{count}} years',
    kgUnit: '{{value}} kg',
  },

  // Vaccines
  vaccines: {
    title: "{{name}}'s Vaccines",
    noVaccines: 'No vaccines recorded',
    addVaccine: 'Add Vaccine',
    vaccineType: 'Vaccine type',
    date: 'Date (YYYY-MM-DD)',
    vet: 'Veterinarian',
    clinic: 'Clinic',
    notes: 'Notes',
    deleteTitle: 'Delete vaccine',
    deleteConfirm: 'Are you sure?',
    errorLoading: 'Could not load vaccines',
    errorSaving: 'Error saving',
    errorDeleting: 'Could not delete',
    fillRequired: 'Fill in the vaccine type and date',
    dateFormat: 'Date format: YYYY-MM-DD',
    nextDose: 'Next dose: {{date}}',
    vaccineTypePlaceholder: 'E.g.: Rabies, DHPP',
    datePlaceholder: '2024-01-15',
  },

  // QR Screen
  qr: {
    title: 'QR Code',
    scanInstruction: 'Scan this QR code to identify {{name}}. You can print it and attach it to their collar.',
    share: 'Share',
    downloadPDF: 'Download PDF',
    shareTitle: 'Share QR',
    shareMessage: 'Share feature will be available soon.',
    pdfTitle: 'Download PDF',
    pdfMessage: 'PDF download will be available soon.',
  },

  // Scan Nose
  scanNose: {
    title: 'Scan Nose',
    description: "Point the camera at the dog's nose to identify it. Make sure the nose is well lit and in focus.",
    step1: "Bring the phone close to the dog's nose",
    step2: 'Keep the camera steady',
    step3: 'Wait for the verification result',
    startScan: 'Start Scan',
    scanQRInstead: 'Scan QR instead',
    errorVerification: 'Verification failed',
  },

  // Scan QR
  scanQR: {
    title: 'Scan QR Code',
    description: "Scan the QR code on the dog's collar to see its information.",
    openCamera: 'Open QR Camera',
    cameraTitle: 'QR Camera',
    cameraMessage: 'QR camera will be available soon. Use manual search instead.',
    manualEntry: 'or enter the code manually',
    qrPlaceholder: 'QR Code (e.g.: IDC-DOG-00001)',
    enterCode: 'Enter a QR code',
    errorSearch: 'Could not search the QR code',
  },

  // Result Screen
  result: {
    matchFound: 'Match Found',
    noMatch: 'No Match',
    dogData: 'Dog Information',
    name: 'Name',
    id: 'ID',
    confidence: 'Confidence',
    dailyUsage: 'Daily usage',
    remainingVerifications: '{{count}} verifications remaining today',
    unlimitedVerifications: 'Unlimited verifications',
    newVerification: 'New Verification',
    dogFoundByQR: 'Dog found by QR',
    dogNotFoundByQR: 'No dog found with that QR code',
  },

  // Limit Modal
  limit: {
    title: 'Daily Limit Reached',
    description: 'You have reached the maximum free verifications for today.',
    usageCount: '{{used}} / {{limit}} verifications used',
    upgradeText: 'Upgrade to Premium for unlimited verifications and more benefits.',
    viewPremium: 'View Premium',
    dailyLimitReached: 'Daily limit reached',
  },

  // Vaccine Card
  vaccineCard: {
    vet: 'Vet',
    clinic: 'Clinic',
    nextDose: 'Next dose',
  },
};
