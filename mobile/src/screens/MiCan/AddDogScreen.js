import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, Alert } from 'react-native';
import { TextInput, Button, SegmentedButtons, Text, HelperText } from 'react-native-paper';
import { useTranslation } from '../../i18n';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function AddDogScreen({ navigation }) {
  const { t } = useTranslation();
  const [name, setName] = useState('');
  const [breed, setBreed] = useState('');
  const [sex, setSex] = useState('M');
  const [origin, setOrigin] = useState('adopted');
  const [ageYears, setAgeYears] = useState('');
  const [weightKg, setWeightKg] = useState('');
  const [color, setColor] = useState('');
  const [microchipId, setMicrochipId] = useState('');
  const [behaviorNotes, setBehaviorNotes] = useState('');
  const [likes, setLikes] = useState('');
  const [allergies, setAllergies] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const originOptions = [
    { value: 'adopted', label: t('addDog.adopted') },
    { value: 'purchased', label: t('addDog.purchased') },
    { value: 'rescued', label: t('addDog.rescued') },
    { value: 'other', label: t('addDog.other') },
  ];

  const handleSubmit = async () => {
    if (!name.trim()) {
      setError(t('addDog.nameRequired'));
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const data = {
        name: name.trim(),
        breed: breed.trim() || null,
        sex,
        origin,
        age_years: ageYears ? parseInt(ageYears, 10) : null,
        weight_kg: weightKg ? parseFloat(weightKg) : null,
        color: color.trim() || null,
        microchip_id: microchipId.trim() || null,
        behavior_notes: behaviorNotes.trim() || null,
        likes: likes.trim() || null,
        allergies: allergies.trim() || null,
      };

      await client.post('/api/dogs', data);
      Alert.alert(t('addDog.success'), t('addDog.successMessage', { name }), [
        { text: t('common.ok'), onPress: () => navigation.goBack() },
      ]);
    } catch (err) {
      setError(err.response?.data?.detail || t('addDog.errorRegistering'));
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.sectionTitle}>{t('addDog.basicInfo')}</Text>

      <TextInput
        label={`${t('addDog.dogName')} *`}
        value={name}
        onChangeText={setName}
        mode="outlined"
        style={styles.input}
      />

      <TextInput
        label={t('addDog.breed')}
        value={breed}
        onChangeText={setBreed}
        mode="outlined"
        style={styles.input}
      />

      <Text style={styles.label}>{t('addDog.sex')}</Text>
      <SegmentedButtons
        value={sex}
        onValueChange={setSex}
        buttons={[
          { value: 'M', label: t('dog.male') },
          { value: 'F', label: t('dog.female') },
        ]}
        style={styles.segmented}
      />

      <Text style={styles.label}>{t('addDog.origin')}</Text>
      <SegmentedButtons
        value={origin}
        onValueChange={setOrigin}
        buttons={originOptions}
        style={styles.segmented}
      />

      <View style={styles.row}>
        <TextInput
          label={t('addDog.age')}
          value={ageYears}
          onChangeText={setAgeYears}
          mode="outlined"
          keyboardType="numeric"
          style={[styles.input, styles.halfInput]}
        />
        <TextInput
          label={t('addDog.weight')}
          value={weightKg}
          onChangeText={setWeightKg}
          mode="outlined"
          keyboardType="decimal-pad"
          style={[styles.input, styles.halfInput]}
        />
      </View>

      <TextInput
        label={t('addDog.color')}
        value={color}
        onChangeText={setColor}
        mode="outlined"
        style={styles.input}
      />

      <TextInput
        label={t('addDog.microchip')}
        value={microchipId}
        onChangeText={setMicrochipId}
        mode="outlined"
        style={styles.input}
      />

      <Text style={styles.sectionTitle}>{t('addDog.additionalInfo')}</Text>

      <TextInput
        label={t('addDog.behavior')}
        value={behaviorNotes}
        onChangeText={setBehaviorNotes}
        mode="outlined"
        multiline
        numberOfLines={3}
        style={styles.input}
      />

      <TextInput
        label={t('addDog.likes')}
        value={likes}
        onChangeText={setLikes}
        mode="outlined"
        multiline
        numberOfLines={2}
        style={styles.input}
      />

      <TextInput
        label={t('addDog.allergies')}
        value={allergies}
        onChangeText={setAllergies}
        mode="outlined"
        multiline
        numberOfLines={2}
        style={styles.input}
      />

      {error && (
        <HelperText type="error" visible={!!error}>
          {error}
        </HelperText>
      )}

      <Button
        mode="contained"
        onPress={handleSubmit}
        loading={loading}
        disabled={loading}
        style={styles.button}
        labelStyle={styles.buttonLabel}
      >
        {t('addDog.registerDog')}
      </Button>
    </ScrollView>
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.primary,
    marginTop: 16,
    marginBottom: 12,
  },
  label: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 8,
    marginTop: 4,
  },
  input: {
    marginBottom: 12,
    backgroundColor: COLORS.surface,
  },
  segmented: {
    marginBottom: 12,
  },
  row: {
    flexDirection: 'row',
    gap: 12,
  },
  halfInput: {
    flex: 1,
  },
  button: {
    marginTop: 24,
    paddingVertical: 6,
    backgroundColor: COLORS.primary,
  },
  buttonLabel: {
    fontSize: 16,
    fontWeight: 'bold',
  },
});
