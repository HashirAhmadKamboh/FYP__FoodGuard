import React, { useState, useMemo } from 'react';
import { View, Text, TouchableOpacity, TextInput, FlatList } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { DISTRICTS } from '../constants/api';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import Animated, { FadeInUp, FadeInDown } from 'react-native-reanimated';
import styles from '../styles/district.styles';

export default function DistrictScreen() {
  const router = useRouter();
  const [search, setSearch] = useState('');

  const filteredDistricts = useMemo(() => {
    return DISTRICTS.filter(d => d.toLowerCase().includes(search.toLowerCase())).sort();
  }, [search]);

  const handleSelect = async (district: string) => {
    await AsyncStorage.setItem('user_district', district);
    router.replace('/(tabs)');
  };

  const renderItem = ({ item, index }: { item: string, index: number }) => (
    <Animated.View entering={FadeInDown.delay(Math.min(index * 30, 600)).duration(400)}>
      <TouchableOpacity 
        style={styles.card} 
        activeOpacity={0.7}
        onPress={() => handleSelect(item)}
      >
        <Text style={styles.cardText}>{item.toUpperCase()}</Text>
        <MaterialCommunityIcons name="chevron-right" size={24} color="#166534" />
      </TouchableOpacity>
    </Animated.View>
  );

  return (
    <View style={styles.container}>
      <Animated.View entering={FadeInUp.duration(600)} style={styles.header}>
        <View style={styles.headerTop}>
          <Text style={styles.title}>Select City</Text>
          <TouchableOpacity onPress={() => router.back()} style={styles.closeBtn}>
            <MaterialCommunityIcons name="close-circle" size={28} color="#166534" />
          </TouchableOpacity>
        </View>
        <Text style={styles.subtitle}>Choose your location to see accurate local prices</Text>
        
        <View style={styles.searchContainer}>
          <MaterialCommunityIcons name="magnify" size={24} color="#15803D" style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Search for your city..."
            placeholderTextColor="#888"
            value={search}
            onChangeText={setSearch}
          />
          {search.length > 0 && (
            <TouchableOpacity onPress={() => setSearch('')}>
              <MaterialCommunityIcons name="close" size={20} color="#666" style={styles.clearIcon} />
            </TouchableOpacity>
          )}
        </View>
      </Animated.View>

      <FlatList
        data={filteredDistricts}
        keyExtractor={(item) => item}
        renderItem={renderItem}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <MaterialCommunityIcons name="city-variant-outline" size={60} color="#ccc" />
            <Text style={styles.emptyText}>No cities found matching "{search}"</Text>
          </View>
        }
      />
    </View>
  );
}