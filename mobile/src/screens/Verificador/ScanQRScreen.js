import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text, Button, Card, TextInput } from 'react-native-paper';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function ScanQRScreen({ navigation }) {
  const [qrCode, setQrCode] = useState('');
  const [loading, setLoading] = useState(false);

  // In a real implementation, this would use expo-barcode-scanner
  // For now, we provide manual QR code entry as fallback

  const handleManualSearch = async () => {
    if (!qrCode.trim()) {
      Alert.alert('Error', 'Ingresá un código QR');
      return;
    }

    setLoading(true);
    try {
      // Search for the dog by QR code
      const response = await client.get('/api/dogs');
      const dogs = response.data;
      const found = dogs.find((d) => d.qr_code === qrCode.trim().toUpperCase());

      if (found) {
        navigation.navigate('Result', {
          result: {
            match: true,
            confidence: 1.0,
            dog_id: found.id,
            dog_name: found.name,
            verification_type: 'qr_scan',
            message: 'Perro encontrado por QR',
          },
        });
      } else {
        navigation.navigate('Result', {
          result: {
            match: false,
            confidence: 0,
            dog_id: null,
            dog_name: null,
            verification_type: 'qr_scan',
            message: 'No se encontró un perro con ese código QR',
          },
        });
      }
    } catch {
      Alert.alert('Error', 'No se pudo buscar el código QR');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.cardContent}>
          <Text style={styles.icon}>📱</Text>
          <Text style={styles.title}>Escanear Código QR</Text>
          <Text style={styles.description}>
            Escaneá el código QR del collar del perro para ver su información.
          </Text>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        icon="camera"
        onPress={() =>
          Alert.alert(
            'Cámara QR',
            'La cámara QR estará disponible próximamente. Usá la búsqueda manual.',
          )
        }
        style={styles.cameraButton}
        labelStyle={styles.cameraButtonLabel}
      >
        Abrir Cámara QR
      </Button>

      <Text style={styles.orText}>o ingresá el código manualmente</Text>

      <TextInput
        label="Código QR (ej: IDC-DOG-00001)"
        value={qrCode}
        onChangeText={setQrCode}
        mode="outlined"
        autoCapitalize="characters"
        style={styles.input}
      />

      <Button
        mode="outlined"
        onPress={handleManualSearch}
        loading={loading}
        disabled={loading}
        style={styles.searchButton}
      >
        Buscar
      </Button>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    padding: 16,
  },
  card: {
    marginBottom: 24,
    elevation: 2,
  },
  cardContent: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  icon: {
    fontSize: 64,
    marginBottom: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
  },
  cameraButton: {
    paddingVertical: 8,
    backgroundColor: COLORS.primary,
    marginBottom: 16,
  },
  cameraButtonLabel: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  orText: {
    textAlign: 'center',
    color: COLORS.textSecondary,
    marginBottom: 16,
  },
  input: {
    marginBottom: 12,
    backgroundColor: COLORS.surface,
  },
  searchButton: {
    paddingVertical: 4,
  },
});
