import React, { useState } from 'react';
import { View, StyleSheet, Alert, Image } from 'react-native';
import { Text, Button, Card } from 'react-native-paper';
import { useTranslation } from '../../i18n';
import client from '../../api/client';
import { COLORS, FREE_VERIFICATION_LIMIT } from '../../constants/config';
import LimitModal from '../../components/LimitModal';

export default function ScanNoseScreen({ navigation }) {
  const { t } = useTranslation();
  const [loading, setLoading] = useState(false);
  const [limitModalVisible, setLimitModalVisible] = useState(false);
  const [limitInfo, setLimitInfo] = useState(null);

  const handleScanNose = async () => {
    setLoading(true);
    try {
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
          message: detail?.message || t('limit.dailyLimitReached'),
        });
        setLimitModalVisible(true);
      } else {
        Alert.alert(t('common.error'), t('scanNose.errorVerification'));
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
          <Text style={styles.title}>{t('scanNose.title')}</Text>
          <Text style={styles.description}>{t('scanNose.description')}</Text>

          <View style={styles.steps}>
            <StepItem number="1" text={t('scanNose.step1')} />
            <StepItem number="2" text={t('scanNose.step2')} />
            <StepItem number="3" text={t('scanNose.step3')} />
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
        {t('scanNose.startScan')}
      </Button>

      <Button
        mode="outlined"
        icon="qrcode-scan"
        onPress={() => navigation.navigate('ScanQR')}
        style={styles.altButton}
      >
        {t('scanNose.scanQRInstead')}
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
