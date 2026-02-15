import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Portal, Modal, Text, Button } from 'react-native-paper';
import { COLORS } from '../constants/config';

export default function LimitModal({ visible, onDismiss, limitInfo }) {
  return (
    <Portal>
      <Modal
        visible={visible}
        onDismiss={onDismiss}
        contentContainerStyle={styles.container}
      >
        <Text style={styles.icon}>⚠️</Text>
        <Text style={styles.title}>Límite Diario Alcanzado</Text>

        <Text style={styles.description}>
          {limitInfo?.message ||
            'Alcanzaste el máximo de verificaciones gratuitas por hoy.'}
        </Text>

        {limitInfo && (
          <View style={styles.usageBar}>
            <Text style={styles.usageText}>
              {limitInfo.used} / {limitInfo.limit} verificaciones usadas
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

        <Text style={styles.upgradeText}>
          Upgrade a Premium para verificaciones ilimitadas y más beneficios.
        </Text>

        <View style={styles.actions}>
          <Button mode="contained" onPress={onDismiss} style={styles.premiumButton}>
            Ver Premium
          </Button>
          <Button mode="text" onPress={onDismiss}>
            Cerrar
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
