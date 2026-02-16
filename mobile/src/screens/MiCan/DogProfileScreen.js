import React, { useState, useCallback } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Text, Card, Button, Chip, Divider, ActivityIndicator } from 'react-native-paper';
import { useFocusEffect } from '@react-navigation/native';
import { useTranslation } from '../../i18n';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function DogProfileScreen({ route, navigation }) {
  const { dog: initialDog } = route.params;
  const { t, language } = useTranslation();
  const [dog, setDog] = useState(initialDog);
  const [loading, setLoading] = useState(false);

  useFocusEffect(
    useCallback(() => {
      const refresh = async () => {
        try {
          const response = await client.get(`/api/dogs/${initialDog.id}`);
          setDog(response.data);
        } catch {
          // Keep the initial data on error
        }
      };
      refresh();
    }, [initialDog.id])
  );

  const dateLocales = { es: 'es-AR', en: 'en-US', pt: 'pt-BR' };

  const formatDate = (dateStr) => {
    if (!dateStr) return t('dogProfile.notRegistered');
    return new Date(dateStr).toLocaleDateString(dateLocales[language] || 'es-AR');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Header */}
      <Card style={styles.headerCard}>
        <Card.Content>
          <View style={styles.headerRow}>
            <View style={styles.headerInfo}>
              <Text style={styles.dogName}>{dog.name}</Text>
              <Text style={styles.breed}>{dog.breed || t('dog.noBreed')}</Text>
            </View>
            <Chip icon="qrcode" style={styles.qrChip}>
              {dog.qr_code}
            </Chip>
          </View>

          <Divider style={styles.divider} />

          <View style={styles.detailsGrid}>
            <DetailItem label={t('dogProfile.sex')} value={dog.sex === 'M' ? t('dog.male') : t('dog.female')} />
            <DetailItem label={t('dogProfile.age')} value={dog.age_years ? t('dogProfile.yearsUnit', { count: dog.age_years }) : '-'} />
            <DetailItem label={t('dogProfile.weight')} value={dog.weight_kg ? t('dogProfile.kgUnit', { value: dog.weight_kg }) : '-'} />
            <DetailItem label={t('dogProfile.color')} value={dog.color || '-'} />
            <DetailItem label={t('dogProfile.origin')} value={dog.origin} />
            <DetailItem label={t('dogProfile.microchip')} value={dog.microchip_id || '-'} />
          </View>
        </Card.Content>
      </Card>

      {/* Notes Section */}
      {(dog.behavior_notes || dog.likes || dog.allergies) && (
        <Card style={styles.card}>
          <Card.Content>
            <Text style={styles.sectionTitle}>{t('dogProfile.notes')}</Text>
            {dog.behavior_notes && (
              <NoteItem label={t('dogProfile.behaviorLabel')} value={dog.behavior_notes} />
            )}
            {dog.likes && <NoteItem label={t('dogProfile.likesLabel')} value={dog.likes} />}
            {dog.allergies && (
              <NoteItem label={t('dogProfile.allergiesLabel')} value={dog.allergies} icon="alert" />
            )}
          </Card.Content>
        </Card>
      )}

      {/* Actions */}
      <View style={styles.actions}>
        <Button
          mode="contained"
          icon="needle"
          onPress={() => navigation.navigate('Vaccines', { dogId: dog.id, dogName: dog.name })}
          style={styles.actionButton}
        >
          {t('dogProfile.vaccines')}
        </Button>

        <Button
          mode="contained"
          icon="qrcode"
          onPress={() => navigation.navigate('GenerateQR', { dog })}
          style={[styles.actionButton, { backgroundColor: COLORS.secondary }]}
        >
          {t('dogProfile.qrCode')}
        </Button>
      </View>

      <Text style={styles.footer}>
        {t('dogProfile.registeredOn', { date: formatDate(dog.created_at) })}
      </Text>
    </ScrollView>
  );
}

function DetailItem({ label, value }) {
  return (
    <View style={styles.detailItem}>
      <Text style={styles.detailLabel}>{label}</Text>
      <Text style={styles.detailValue}>{value}</Text>
    </View>
  );
}

function NoteItem({ label, value, icon }) {
  return (
    <View style={styles.noteItem}>
      <Text style={styles.noteLabel}>{label}</Text>
      <Text style={styles.noteValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  content: {
    padding: 16,
    paddingBottom: 40,
  },
  headerCard: {
    marginBottom: 16,
    elevation: 2,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  headerInfo: {
    flex: 1,
  },
  dogName: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  breed: {
    fontSize: 16,
    color: COLORS.textSecondary,
    marginTop: 2,
  },
  qrChip: {
    backgroundColor: COLORS.background,
  },
  divider: {
    marginVertical: 16,
  },
  detailsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
  },
  detailItem: {
    width: '50%',
    marginBottom: 12,
  },
  detailLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
  },
  detailValue: {
    fontSize: 16,
    color: COLORS.text,
    fontWeight: '500',
    marginTop: 2,
  },
  card: {
    marginBottom: 16,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginBottom: 12,
  },
  noteItem: {
    marginBottom: 12,
  },
  noteLabel: {
    fontSize: 12,
    color: COLORS.textSecondary,
    textTransform: 'uppercase',
  },
  noteValue: {
    fontSize: 14,
    color: COLORS.text,
    marginTop: 4,
  },
  actions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 16,
  },
  actionButton: {
    flex: 1,
    backgroundColor: COLORS.primary,
  },
  footer: {
    textAlign: 'center',
    color: COLORS.textSecondary,
    fontSize: 12,
  },
});
