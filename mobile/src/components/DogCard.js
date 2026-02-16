import React from 'react';
import { StyleSheet } from 'react-native';
import { Card, Text, Chip } from 'react-native-paper';
import { useTranslation } from '../i18n';
import { COLORS } from '../constants/config';

export default function DogCard({ dog, onPress }) {
  const { t } = useTranslation();

  return (
    <Card style={styles.card} onPress={onPress}>
      <Card.Content style={styles.content}>
        <Text style={styles.name}>{dog.name}</Text>
        <Text style={styles.breed}>{dog.breed || t('dog.noBreed')}</Text>

        <Chip icon="qrcode" style={styles.chip} textStyle={styles.chipText}>
          {dog.qr_code}
        </Chip>

        <Text style={styles.details}>
          {dog.sex === 'M' ? t('dog.male') : t('dog.female')}
          {dog.age_years ? ` · ${dog.age_years} ${t('dog.years')}` : ''}
          {dog.weight_kg ? ` · ${dog.weight_kg} ${t('dog.kg')}` : ''}
        </Text>
      </Card.Content>
    </Card>
  );
}

const styles = StyleSheet.create({
  card: {
    marginBottom: 12,
    elevation: 2,
    backgroundColor: COLORS.surface,
  },
  content: {
    paddingVertical: 12,
  },
  name: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  breed: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 2,
    marginBottom: 8,
  },
  chip: {
    alignSelf: 'flex-start',
    marginBottom: 8,
    backgroundColor: COLORS.background,
  },
  chipText: {
    fontSize: 12,
  },
  details: {
    fontSize: 13,
    color: COLORS.textSecondary,
  },
});
