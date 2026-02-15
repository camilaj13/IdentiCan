import React, { useState } from 'react';
import { View, StyleSheet, Alert, Image } from 'react-native';
import { Text, Button, Card } from 'react-native-paper';
import client from '../../api/client';
import { COLORS, FREE_VERIFICATION_LIMIT } from '../../constants/config';
import LimitModal from '../../components/LimitModal';

export default function ScanNoseScreen({ navigation }) {
  const [loading, setLoading] = useState(false);
  const [limitModalVisible, setLimitModalVisible] = useState(false);
  const [limitInfo, setLimitInfo] = useState(null);

  const handleScanNose = async () => {
    // In a real implementation, this would:
    // 1. Open the camera
    // 2. Capture a nose image
    // 3. Send it to the API for verification

    setLoading(true);
    try {
      // Create a mock image file for the API call
      const formData = new FormData();
      formData.append('file', {
        uri: 'mock://nose-image.jpg',
        type: 'image/jpeg',
        name: 'nose_scan.jpg',
      });

      const response = await client.post('/api/nose/verify', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      navigation.navigate('Result', { result: response.data });
    } catch (err) {
      if (err.response?.status === 429) {
        const detail = err.response.data?.detail;
        setLimitInfo({
          used: detail?.verifications_used || FREE_VERIFICATION_LIMIT,
          limit: detail?.verifications_limit || FREE_VERIFICATION_LIMIT,
          message: detail?.message || 'Límite diario alcanzado',
        });
        setLimitModalVisible(true);
      } else {
        Alert.alert('Error', 'No se pudo realizar la verificación');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.cardContent}>
          <Text style={styles.icon}>👃</Text>
          <Text style={styles.title}>Escanear Nariz</Text>
          <Text style={styles.description}>
            Apuntá la cámara a la nariz del perro para identificarlo.
            Asegurate de que la nariz esté bien iluminada y enfocada.
          </Text>

          <View style={styles.steps}>
            <StepItem number="1" text="Acercá el celular a la nariz del perro" />
            <StepItem number="2" text="Mantené la cámara estable" />
            <StepItem number="3" text="Esperá el resultado de la verificación" />
          </View>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        icon="camera"
        onPress={handleScanNose}
        loading={loading}
        disabled={loading}
        style={styles.scanButton}
        labelStyle={styles.scanButtonLabel}
      >
        Iniciar Escaneo
      </Button>

      <Button
        mode="outlined"
        icon="qrcode-scan"
        onPress={() => navigation.navigate('ScanQR')}
        style={styles.altButton}
      >
        Escanear QR en su lugar
      </Button>

      <LimitModal
        visible={limitModalVisible}
        onDismiss={() => setLimitModalVisible(false)}
        limitInfo={limitInfo}
      />
    </View>
  );
}

function StepItem({ number, text }) {
  return (
    <View style={styles.stepItem}>
      <View style={styles.stepNumber}>
        <Text style={styles.stepNumberText}>{number}</Text>
      </View>
      <Text style={styles.stepText}>{text}</Text>
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
    marginBottom: 24,
    paddingHorizontal: 16,
  },
  steps: {
    width: '100%',
    paddingHorizontal: 16,
  },
  stepItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  stepNumber: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: COLORS.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  stepNumberText: {
    color: '#fff',
    fontWeight: 'bold',
    fontSize: 14,
  },
  stepText: {
    fontSize: 14,
    color: COLORS.text,
    flex: 1,
  },
  scanButton: {
    paddingVertical: 8,
    backgroundColor: COLORS.primary,
    marginBottom: 12,
  },
  scanButtonLabel: {
    fontSize: 18,
    fontWeight: 'bold',
  },
  altButton: {
    paddingVertical: 4,
  },
});
