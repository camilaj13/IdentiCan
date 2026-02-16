import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../context/AuthContext';
import { useTranslation } from '../i18n';
import { COLORS } from '../constants/config';
import { LanguageSelectorHeader } from '../components/LanguageSelector';

import AuthNavigator from './AuthNavigator';
import HomeScreen from '../screens/MiCan/HomeScreen';
import AddDogScreen from '../screens/MiCan/AddDogScreen';
import DogProfileScreen from '../screens/MiCan/DogProfileScreen';
import VaccinesScreen from '../screens/MiCan/VaccinesScreen';
import GenerateQRScreen from '../screens/MiCan/GenerateQRScreen';
import ScanNoseScreen from '../screens/Verificador/ScanNoseScreen';
import ScanQRScreen from '../screens/Verificador/ScanQRScreen';
import ResultScreen from '../screens/Verificador/ResultScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function MiCanStack() {
  const { t } = useTranslation();
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: COLORS.primary },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
        headerRight: () => <LanguageSelectorHeader />,
      }}
    >
      <Stack.Screen name="Home" component={HomeScreen} options={{ title: t('nav.myDogs') }} />
      <Stack.Screen name="AddDog" component={AddDogScreen} options={{ title: t('nav.addDog') }} />
      <Stack.Screen name="DogProfile" component={DogProfileScreen} options={{ title: t('nav.profile') }} />
      <Stack.Screen name="Vaccines" component={VaccinesScreen} options={{ title: t('nav.vaccines') }} />
      <Stack.Screen name="GenerateQR" component={GenerateQRScreen} options={{ title: t('nav.qrCode') }} />
    </Stack.Navigator>
  );
}

function VerificadorStack() {
  const { t } = useTranslation();
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: COLORS.primary },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
        headerRight: () => <LanguageSelectorHeader />,
      }}
    >
      <Stack.Screen name="ScanNose" component={ScanNoseScreen} options={{ title: t('nav.scanNose') }} />
      <Stack.Screen name="ScanQR" component={ScanQRScreen} options={{ title: t('nav.scanQR') }} />
      <Stack.Screen name="Result" component={ResultScreen} options={{ title: t('nav.result') }} />
    </Stack.Navigator>
  );
}

function MainTabs() {
  const { t } = useTranslation();
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textSecondary,
        tabBarStyle: { paddingBottom: 5, height: 60 },
        tabBarLabelStyle: { fontSize: 12, fontWeight: '600' },
      }}
    >
      <Tab.Screen
        name="MiCan"
        component={MiCanStack}
        options={{
          tabBarLabel: t('nav.myCan'),
          tabBarIcon: ({ color, size }) => null,
        }}
      />
      <Tab.Screen
        name="Verificador"
        component={VerificadorStack}
        options={{
          tabBarLabel: t('nav.verify'),
          tabBarIcon: ({ color, size }) => null,
        }}
      />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  const { token, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <NavigationContainer>
      {token ? <MainTabs /> : <AuthNavigator />}
    </NavigationContainer>
  );
}
