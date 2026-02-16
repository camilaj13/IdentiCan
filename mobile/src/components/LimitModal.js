import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Portal, Modal, Text, Button } from 'react-native-paper';
import { useTranslation } from '../i18n';
import { COLORS } from '../constants/config';

export default function LimitModal({ visible, onDismiss, limitInfo }) {
  const { t } = useTranslation();

  return (
    <Portal>
      <Modal
        visible={visible}
        onDismiss={onDismiss}
        contentContainerStyle={styles.container}
      >
        <Text style={styles.icon}>⚠️</Text>
        <Text style={styles.title}>{t('limit.title')}</Text>

        <Text style={styles.description}>
          {limitInfo?.message || t('limit.description')}
        </Text>

        {limitInfo && (
          <View style={styles.usageBar}>
            <Text style={styles.usageText}>
              {t('limit.usageCount', { used: limitInfo.used, limit: limitInfo.limit })}
            </Text>
            <View style={styles.progressBar}>
              <View
                style={[
                  styles.progressFill,
                  { width: '100%' },
                ]}
              />
            </View>
          </View>
        )}

        <Text style={styles.upgradeText}>{t('limit.upgradeText')}</Text>

        <View style={styles.actions}>
          <Button mode="contained" onPress={onDismiss} style={styles.premiumButton}>
            {t('limit.viewPremium')}
          </Button>
          <Button mode="text" onPress={onDismiss}>
            {t('common.close')}
          </Button>
        </View>
      </Modal>
    </Portal>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: COLORS.surface,
    margin: 20,
    padding: 24,
    borderRadius: 16,
    alignItems: 'center',
  },
  icon: {
    fontSize: 48,
    marginBottom: 12,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 12,
    textAlign: 'center',
  },
  description: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 16,
    lineHeight: 20,
  },
  usageBar: {
    width: '100%',
    marginBottom: 16,
  },
  usageText: {
    fontSize: 13,
    color: COLORS.text,
    fontWeight: '500',
    marginBottom: 6,
    textAlign: 'center',
  },
  progressBar: {
    height: 8,
    backgroundColor: COLORS.border,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: COLORS.error,
    borderRadius: 4,
  },
  upgradeText: {
    fontSize: 13,
    color: COLORS.secondary,
    textAlign: 'center',
    marginBottom: 20,
    fontWeight: '500',
  },
  actions: {
    width: '100%',
    gap: 8,
  },
  premiumButton: {
    backgroundColor: COLORS.secondary,
  },
});
