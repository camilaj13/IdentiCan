import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { ActivityIndicator, View } from 'react-native';
import { useAuth } from '../context/AuthContext';
import { COLORS } from '../constants/config';

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
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: COLORS.primary },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Mis Perros' }} />
      <Stack.Screen name="AddDog" component={AddDogScreen} options={{ title: 'Agregar Perro' }} />
      <Stack.Screen name="DogProfile" component={DogProfileScreen} options={{ title: 'Perfil' }} />
      <Stack.Screen name="Vaccines" component={VaccinesScreen} options={{ title: 'Vacunas' }} />
      <Stack.Screen name="GenerateQR" component={GenerateQRScreen} options={{ title: 'Código QR' }} />
    </Stack.Navigator>
  );
}

function VerificadorStack() {
  return (
    <Stack.Navigator
      screenOptions={{
        headerStyle: { backgroundColor: COLORS.primary },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      <Stack.Screen name="ScanNose" component={ScanNoseScreen} options={{ title: 'Escanear Nariz' }} />
      <Stack.Screen name="ScanQR" component={ScanQRScreen} options={{ title: 'Escanear QR' }} />
      <Stack.Screen name="Result" component={ResultScreen} options={{ title: 'Resultado' }} />
    </Stack.Navigator>
  );
}

function MainTabs() {
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
          tabBarLabel: 'Mi Can',
          tabBarIcon: ({ color, size }) => null, // Icons handled by react-native-vector-icons
        }}
      />
      <Tab.Screen
        name="Verificador"
        component={VerificadorStack}
        options={{
          tabBarLabel: 'Verificar',
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
