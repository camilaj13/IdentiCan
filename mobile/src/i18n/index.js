import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import es from './translations/es';
import en from './translations/en';
import pt from './translations/pt';

const STORAGE_KEY = '@identican_language';

const translations = { es, en, pt };

const SUPPORTED_LANGUAGES = [
  { code: 'es', name: 'Español', flag: '🇦🇷' },
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'pt', name: 'Português', flag: '🇧🇷' },
];

const LanguageContext = createContext();

/**
 * Get a nested value from an object using a dot-separated path.
 * e.g. getNestedValue(obj, 'auth.login') => obj.auth.login
 */
function getNestedValue(obj, path) {
  return path.split('.').reduce((current, key) => current?.[key], obj);
}

/**
 * Replace {{variable}} placeholders in a string with provided values.
 */
function interpolate(str, params) {
  if (!params || typeof str !== 'string') return str;
  return Object.entries(params).reduce(
    (result, [key, value]) => result.replace(new RegExp(`\\{\\{${key}\\}\\}`, 'g'), value),
    str,
  );
}

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState('es');
  const [ready, setReady] = useState(false);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY).then((saved) => {
      if (saved && translations[saved]) {
        setLanguageState(saved);
      }
      setReady(true);
    });
  }, []);

  const setLanguage = useCallback(async (code) => {
    if (translations[code]) {
      setLanguageState(code);
      await AsyncStorage.setItem(STORAGE_KEY, code);
    }
  }, []);

  /**
   * Translation function. Usage:
   *   t('auth.login') => 'Log In'
   *   t('home.greeting', { name: 'Maria' }) => 'Hello, Maria'
   */
  const t = useCallback(
    (key, params) => {
      const value = getNestedValue(translations[language], key);
      if (value === undefined) {
        // Fallback to Spanish, then return the key itself
        const fallback = getNestedValue(translations.es, key);
        return interpolate(fallback ?? key, params);
      }
      return interpolate(value, params);
    },
    [language],
  );

  return (
    <LanguageContext.Provider
      value={{
        language,
        setLanguage,
        t,
        ready,
        supportedLanguages: SUPPORTED_LANGUAGES,
      }}
    >
      {children}
    </LanguageContext.Provider>
  );
}

export function useTranslation() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useTranslation must be used within a LanguageProvider');
  }
  return context;
}

export { SUPPORTED_LANGUAGES };
export default LanguageContext;
