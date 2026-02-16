import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import { AuthProvider } from './src/context/AuthContext';
import { LanguageProvider } from './src/i18n';
import AppNavigator from './src/navigation/AppNavigator';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#1565C0',
    secondary: '#FF8F00',
    accent: '#FF8F00',
    background: '#F5F5F5',
    surface: '#FFFFFF',
    error: '#D32F2F',
  },
  roundness: 8,
};

export default function App() {
  return (
    <PaperProvider theme={theme}>
      <LanguageProvider>
        <AuthProvider>
          <StatusBar style="light" />
          <AppNavigator />
        </AuthProvider>
      </LanguageProvider>
    </PaperProvider>
  );
}
