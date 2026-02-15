import React from 'react';
import { View, StyleSheet, Alert } from 'react-native';
import { Text, Button, Card } from 'react-native-paper';
import QRCode from 'react-native-qrcode-svg';
import { COLORS } from '../../constants/config';

export default function GenerateQRScreen({ route }) {
  const { dog } = route.params;

  const handleShare = () => {
    Alert.alert(
      'Compartir QR',
      'La funcionalidad de compartir estará disponible próximamente.',
    );
  };

  const handleDownloadPDF = () => {
    Alert.alert(
      'Descargar PDF',
      'La descarga de PDF estará disponible próximamente.',
    );
  };

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content style={styles.cardContent}>
          <Text style={styles.dogName}>{dog.name}</Text>
          <Text style={styles.qrCodeText}>{dog.qr_code}</Text>

          <View style={styles.qrContainer}>
            <QRCode
              value={dog.qr_code}
              size={250}
              backgroundColor="white"
              color="black"
            />
          </View>

          <Text style={styles.instructions}>
            Escaneá este código QR para identificar a {dog.name}.
            Podés imprimirlo y colocarlo en su collar.
          </Text>
        </Card.Content>
      </Card>

      <View style={styles.actions}>
        <Button
          mode="contained"
          icon="share-variant"
          onPress={handleShare}
          style={styles.button}
        >
          Compartir
        </Button>

        <Button
          mode="outlined"
          icon="file-pdf-box"
          onPress={handleDownloadPDF}
          style={styles.button}
        >
          Descargar PDF
        </Button>
      </View>
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
    elevation: 3,
    marginBottom: 24,
  },
  cardContent: {
    alignItems: 'center',
    paddingVertical: 24,
  },
  dogName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 4,
  },
  qrCodeText: {
    fontSize: 14,
    color: COLORS.textSecondary,
    marginBottom: 24,
    fontFamily: 'monospace',
  },
  qrContainer: {
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 12,
    marginBottom: 24,
    elevation: 1,
  },
  instructions: {
    fontSize: 14,
    color: COLORS.textSecondary,
    textAlign: 'center',
    lineHeight: 20,
    paddingHorizontal: 16,
  },
  actions: {
    gap: 12,
  },
  button: {
    paddingVertical: 4,
  },
});
