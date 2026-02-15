import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Card, Button, Divider } from 'react-native-paper';
import { COLORS } from '../../constants/config';

export default function ResultScreen({ route, navigation }) {
  const { result } = route.params;
  const isMatch = result.match;

  return (
    <View style={styles.container}>
      <Card style={[styles.card, isMatch ? styles.successCard : styles.failCard]}>
        <Card.Content style={styles.cardContent}>
          <Text style={styles.icon}>{isMatch ? '✅' : '❌'}</Text>
          <Text style={styles.title}>
            {isMatch ? 'Coincidencia Encontrada' : 'Sin Coincidencia'}
          </Text>
          <Text style={styles.message}>{result.message}</Text>
        </Card.Content>
      </Card>

      {isMatch && result.dog_name && (
        <Card style={styles.detailCard}>
          <Card.Content>
            <Text style={styles.sectionTitle}>Datos del Perro</Text>
            <Divider style={styles.divider} />

            <DetailRow label="Nombre" value={result.dog_name} />
            <DetailRow label="ID" value={result.dog_id?.toString()} />
            {result.confidence && (
              <DetailRow
                label="Confianza"
                value={`${(result.confidence * 100).toFixed(1)}%`}
              />
            )}
          </Card.Content>
        </Card>
      )}

      {result.verification_usage && (
        <Card style={styles.usageCard}>
          <Card.Content>
            <Text style={styles.usageTitle}>Uso del día</Text>
            <Text style={styles.usageText}>
              {result.verification_usage.remaining !== null
                ? `Te quedan ${result.verification_usage.remaining} verificaciones hoy`
                : 'Verificaciones ilimitadas'}
            </Text>
          </Card.Content>
        </Card>
      )}

      <View style={styles.actions}>
        <Button
          mode="contained"
          onPress={() => navigation.navigate('ScanNose')}
          style={styles.button}
        >
          Nueva Verificación
        </Button>
        <Button
          mode="outlined"
          onPress={() => navigation.goBack()}
          style={styles.button}
        >
          Volver
        </Button>
      </View>
    </View>
  );
}

function DetailRow({ label, value }) {
  return (
    <View style={styles.detailRow}>
      <Text style={styles.detailLabel}>{label}</Text>
      <Text style={styles.detailValue}>{value || '-'}</Text>
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
    marginBottom: 16,
    elevation: 3,
  },
  successCard: {
    borderLeftWidth: 4,
    borderLeftColor: COLORS.success,
  },
  failCard: {
    borderLeftWidth: 4,
    borderLeftColor: COLORS.error,
  },
  cardContent: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  icon: {
    fontSize: 64,
    marginBottom: 12,
  },
  title: {
    fontSize: 22,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  message: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  detailCard: {
    marginBottom: 16,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginBottom: 8,
  },
  divider: {
    marginBottom: 12,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
  },
  detailLabel: {
    fontSize: 14,
    color: COLORS.textSecondary,
  },
  detailValue: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.text,
  },
  usageCard: {
    marginBottom: 24,
    backgroundColor: '#FFF3E0',
  },
  usageTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: COLORS.secondary,
  },
  usageText: {
    fontSize: 13,
    color: COLORS.text,
    marginTop: 4,
  },
  actions: {
    gap: 12,
  },
  button: {
    paddingVertical: 4,
  },
});
