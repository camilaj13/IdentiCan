import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Card, Text, IconButton } from 'react-native-paper';
import { useTranslation } from '../i18n';
import { COLORS } from '../constants/config';

export default function VaccineCard({ vaccine, onDelete }) {
  const { t, language } = useTranslation();

  const dateLocales = { es: 'es-AR', en: 'en-US', pt: 'pt-BR' };

  const formatDate = (dateStr) => {
    if (!dateStr) return '-';
    return new Date(dateStr).toLocaleDateString(dateLocales[language] || 'es-AR');
  };

  return (
    <Card style={styles.card}>
      <Card.Content>
        <View style={styles.header}>
          <View style={styles.headerInfo}>
            <Text style={styles.type}>{vaccine.vaccine_type}</Text>
            <Text style={styles.date}>{formatDate(vaccine.vaccine_date)}</Text>
          </View>
          <IconButton
            icon="delete-outline"
            iconColor={COLORS.error}
            size={20}
            onPress={onDelete}
          />
        </View>

        {vaccine.veterinarian_name && (
          <Text style={styles.detail}>{t('vaccineCard.vet')}: {vaccine.veterinarian_name}</Text>
        )}
        {vaccine.clinic_name && (
          <Text style={styles.detail}>{t('vaccineCard.clinic')}: {vaccine.clinic_name}</Text>
        )}
        {vaccine.next_dose_date && (
          <Text style={styles.nextDose}>
            {t('vaccineCard.nextDose')}: {formatDate(vaccine.next_dose_date)}
          </Text>
        )}
        {vaccine.notes && <Text style={styles.notes}>{vaccine.notes}</Text>}
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    marginBottom: 10,
    elevation: 1,
    backgroundColor: COLORS.surface,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  headerInfo: {
    flex: 1,
  },
  type: {
    fontSize: 16,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  date: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  detail: {
    fontSize: 13,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  nextDose: {
    fontSize: 13,
    color: COLORS.warning,
    fontWeight: '500',
    marginTop: 4,
  },
  notes: {
    fontSize: 12,
    color: COLORS.textSecondary,
    fontStyle: 'italic',
    marginTop: 6,
  },
});
