import React, { useState, useCallback } from 'react';
import { View, FlatList, StyleSheet, RefreshControl } from 'react-native';
import { FAB, Text, ActivityIndicator, Snackbar } from 'react-native-paper';
import { useFocusEffect } from '@react-navigation/native';
import DogCard from '../../components/DogCard';
import { useAuth } from '../../context/AuthContext';
import { useTranslation } from '../../i18n';
import client from '../../api/client';
import { COLORS } from '../../constants/config';

export default function HomeScreen({ navigation }) {
  const { user, logout } = useAuth();
  const { t } = useTranslation();
  const [dogs, setDogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchDogs = async () => {
    try {
      const response = await client.get('/api/dogs');
      setDogs(response.data);
      setError(null);
    } catch (err) {
      setError(t('home.errorLoading'));
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useFocusEffect(
    useCallback(() => {
      fetchDogs();
    }, [])
  );

  const onRefresh = () => {
    setRefreshing(true);
    fetchDogs();
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
      <View style={styles.header}>
        <Text style={styles.greeting}>
          {t('home.greeting', { name: user?.name || 'User' })}
        </Text>
        <Text style={styles.dogCount}>
          {dogs.length === 1
            ? t('home.dogCountOne')
            : t('home.dogCountOther', { count: dogs.length })}
        </Text>
      </View>

      {dogs.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyIcon}>🐾</Text>
          <Text style={styles.emptyTitle}>{t('home.noDogs')}</Text>
          <Text style={styles.emptySubtitle}>{t('home.noDogsHint')}</Text>
        </View>
      ) : (
        <FlatList
          data={dogs}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <DogCard
              dog={item}
              onPress={() => navigation.navigate('DogProfile', { dog: item })}
            />
          )}
          contentContainerStyle={styles.list}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
          }
        />
      )}

      <FAB
        icon="plus"
        style={styles.fab}
        onPress={() => navigation.navigate('AddDog')}
        color="#fff"
      />

      <Snackbar
        visible={!!error}
        onDismiss={() => setError(null)}
        duration={3000}
      >
        {error}
      </Snackbar>
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
  header: {
    padding: 16,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  greeting: {
    fontSize: 20,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  dogCount: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginTop: 4,
  },
  list: {
    padding: 16,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 8,
  },
  emptySubtitle: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
  },
  fab: {
    position: 'absolute',
    right: 16,
    bottom: 16,
    backgroundColor: COLORS.primary,
  },
});
