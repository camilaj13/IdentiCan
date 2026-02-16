import React, { useState } from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text, Button, Card, TextInput } from 'react-native-paper';
import { useTranslation } from '../../i18n';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function ScanQRScreen({ navigation }) {
  const { t } = useTranslation();
  const [qrCode, setQrCode] = useState('');
  const [loading, setLoading] = useState(false);

  const handleManualSearch = async () => {
    if (!qrCode.trim()) {
      Alert.alert(t('common.error'), t('scanQR.enterCode'));
      return;
    }

    setLoading(true);
    try {
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
            message: t('result.dogFoundByQR'),
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
            message: t('result.dogNotFoundByQR'),
          },
        });
      }
    } catch {
      Alert.alert(t('common.error'), t('scanQR.errorSearch'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.cardContent}>
          <Text style={styles.icon}>📱</Text>
          <Text style={styles.title}>{t('scanQR.title')}</Text>
          <Text style={styles.description}>{t('scanQR.description')}</Text>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        icon="camera"
        onPress={() => Alert.alert(t('scanQR.cameraTitle'), t('scanQR.cameraMessage'))}
        style={styles.cameraButton}
        labelStyle={styles.cameraButtonLabel}
      >
        {t('scanQR.openCamera')}
      </Button>

      <Text style={styles.orText}>{t('scanQR.manualEntry')}</Text>

      <TextInput
        label={t('scanQR.qrPlaceholder')}
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
        {t('common.search')}
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
