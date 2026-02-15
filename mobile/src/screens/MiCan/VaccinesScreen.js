import React, { useState, useCallback } from 'react';
import {
  View,
  FlatList,
  StyleSheet,
  Alert,
  RefreshControl,
} from 'react-native';
import {
  FAB,
  Text,
  ActivityIndicator,
  Portal,
  Modal,
  TextInput,
  Button,
} from 'react-native-paper';
import { useFocusEffect } from '@react-navigation/native';
import VaccineCard from '../../components/VaccineCard';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function VaccinesScreen({ route }) {
  const { dogId, dogName } = route.params;
  const [vaccines, setVaccines] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [saving, setSaving] = useState(false);

  // Form state
  const [vaccineType, setVaccineType] = useState('');
  const [vaccineDate, setVaccineDate] = useState('');
  const [vetName, setVetName] = useState('');
  const [clinicName, setClinicName] = useState('');
  const [notes, setNotes] = useState('');

  const fetchVaccines = async () => {
    try {
      const response = await client.get(`/api/vaccines/dog/${dogId}`);
      setVaccines(response.data);
    } catch {
      Alert.alert('Error', 'No se pudieron cargar las vacunas');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchVaccines();
    }, [dogId])
  );

  const handleAddVaccine = async () => {
    if (!vaccineType.trim() || !vaccineDate.trim()) {
      Alert.alert('Error', 'Completá el tipo de vacuna y la fecha');
      return;
    }

    // Simple date validation (YYYY-MM-DD)
    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(vaccineDate)) {
      Alert.alert('Error', 'Formato de fecha: AAAA-MM-DD');
      return;
    }

    setSaving(true);
    try {
      await client.post('/api/vaccines', {
        dog_id: dogId,
        vaccine_type: vaccineType.trim(),
        vaccine_date: vaccineDate.trim(),
        veterinarian_name: vetName.trim() || null,
        clinic_name: clinicName.trim() || null,
        notes: notes.trim() || null,
      });
      setModalVisible(false);
      resetForm();
      fetchVaccines();
    } catch (err) {
      Alert.alert('Error', err.response?.data?.detail || 'Error al guardar');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (vaccineId) => {
    Alert.alert('Eliminar vacuna', '¿Estás seguro?', [
      { text: 'Cancelar', style: 'cancel' },
      {
        text: 'Eliminar',
        style: 'destructive',
        onPress: async () => {
          try {
            await client.delete(`/api/vaccines/${vaccineId}`);
            fetchVaccines();
          } catch {
            Alert.alert('Error', 'No se pudo eliminar');
          }
        },
      },
    ]);
  };

  const resetForm = () => {
    setVaccineType('');
    setVaccineDate('');
    setVetName('');
    setClinicName('');
    setNotes('');
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={COLORS.primary} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Vacunas de {dogName}</Text>

      {vaccines.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>💉</Text>
          <Text style={styles.emptyText}>No hay vacunas registradas</Text>
        </View>
      ) : (
        <FlatList
          data={vaccines}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <VaccineCard vaccine={item} onDelete={() => handleDelete(item.id)} />
          )}
          contentContainerStyle={styles.list}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={() => {
                setRefreshing(true);
                fetchVaccines();
              }}
            />
          }
        />
      )}

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={() => setModalVisible(true)}
        color="#fff"
      />

      {/* Add Vaccine Modal */}
      <Portal>
        <Modal
          visible={modalVisible}
          onDismiss={() => setModalVisible(false)}
          contentContainerStyle={styles.modal}
        >
          <Text style={styles.modalTitle}>Agregar Vacuna</Text>

          <TextInput
            label="Tipo de vacuna *"
            value={vaccineType}
            onChangeText={setVaccineType}
            mode="outlined"
            style={styles.input}
            placeholder="Ej: Antirrábica, Séxtuple"
          />

          <TextInput
            label="Fecha (AAAA-MM-DD) *"
            value={vaccineDate}
            onChangeText={setVaccineDate}
            mode="outlined"
            style={styles.input}
            placeholder="2024-01-15"
          />

          <TextInput
            label="Veterinario"
            value={vetName}
            onChangeText={setVetName}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Clínica"
            value={clinicName}
            onChangeText={setClinicName}
            mode="outlined"
            style={styles.input}
          />

          <TextInput
            label="Notas"
            value={notes}
            onChangeText={setNotes}
            mode="outlined"
            multiline
            style={styles.input}
          />

          <View style={styles.modalActions}>
            <Button mode="text" onPress={() => setModalVisible(false)}>
              Cancelar
            </Button>
            <Button mode="contained" onPress={handleAddVaccine} loading={saving}>
              Guardar
            </Button>
          </View>
        </Modal>
      </Portal>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    padding: 16,
    color: COLORS.text,
  },
  list: {
    paddingHorizontal: 16,
    paddingBottom: 80,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  emptyIcon: {
    fontSize: 48,
    marginBottom: 12,
  },
  emptyText: {
    fontSize: 16,
    color: COLORS.textSecondary,
  },
  fab: {
    position: 'absolute',
    right: 16,
    bottom: 16,
    backgroundColor: COLORS.primary,
  },
  modal: {
    backgroundColor: COLORS.surface,
    margin: 20,
    padding: 20,
    borderRadius: 12,
  },
  modalTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 16,
    color: COLORS.primary,
  },
  input: {
    marginBottom: 12,
    backgroundColor: COLORS.surface,
  },
  modalActions: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    gap: 12,
    marginTop: 8,
  },
});
