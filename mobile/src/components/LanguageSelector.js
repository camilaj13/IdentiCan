import React, { useState } from 'react';
import { View, StyleSheet } from 'react-native';
import { Menu, IconButton, Chip } from 'react-native-paper';
import { useTranslation } from '../i18n';
import { COLORS } from '../constants/config';

export default function LanguageSelector({ style }) {
  const { language, setLanguage, supportedLanguages } = useTranslation();
  const [visible, setVisible] = useState(false);

  const current = supportedLanguages.find((l) => l.code === language);

  return (
    <View style={[styles.container, style]}>
      <Menu
        visible={visible}
        onDismiss={() => setVisible(false)}
        anchor={
          <Chip
            icon="translate"
            onPress={() => setVisible(true)}
            style={styles.chip}
            textStyle={styles.chipText}
          >
            {current?.flag} {current?.code.toUpperCase()}
          </Chip>
        }
      >
        {supportedLanguages.map((lang) => (
          <Menu.Item
            key={lang.code}
            onPress={() => {
              setLanguage(lang.code);
              setVisible(false);
            }}
            title={`${lang.flag} ${lang.name}`}
            leadingIcon={language === lang.code ? 'check' : undefined}
          />
        ))}
      </Menu>
    </View>
  );
}

export function LanguageSelectorHeader() {
  const { language, setLanguage, supportedLanguages } = useTranslation();
  const [visible, setVisible] = useState(false);

  const current = supportedLanguages.find((l) => l.code === language);

  return (
    <Menu
      visible={visible}
      onDismiss={() => setVisible(false)}
      anchor={
        <IconButton
          icon="translate"
          iconColor="#fff"
          size={22}
          onPress={() => setVisible(true)}
        />
      }
    >
      {supportedLanguages.map((lang) => (
        <Menu.Item
          key={lang.code}
          onPress={() => {
            setLanguage(lang.code);
            setVisible(false);
          }}
          title={`${lang.flag} ${lang.name}`}
          leadingIcon={language === lang.code ? 'check' : undefined}
        />
      ))}
    </Menu>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
  },
  chip: {
    backgroundColor: '#E3F2FD',
  },
  chipText: {
    fontSize: 13,
    fontWeight: '600',
  },
});
