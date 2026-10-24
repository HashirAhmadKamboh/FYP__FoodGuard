import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, FlatList, ActivityIndicator, Alert, Platform } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { BASE_URL } from '../constants/api';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import Animated, { FadeInDown, FadeInUp, Layout } from 'react-native-reanimated';
import styles from '../styles/history.styles';

const showAlert = (title: string, message: string) => {
  if (Platform.OS === 'web') {
    alert(`${title}\n\n${message}`);
  } else {
    Alert.alert(title, message);
  }
};

interface PredictionRecord {
  id: number;
  item: string;
  confidence: number;
  freshness: string;
  is_food: boolean;
  city: string;
  created_at: string;
  image_url: string | null;
  nutritional_info: any;
  district_pricing: any[];
}

export default function HistoryScreen() {
  const router = useRouter();
  const [history, setHistory] = useState<PredictionRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('user_token');
      if (!token) {
        showAlert('Unauthorized', 'Please log in to see your history.');
        router.replace('/login');
        return;
      }

      const response = await fetch(`${BASE_URL}/predict/history`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to fetch history');
      }

      const data = await response.json();
      setHistory(data);
    } catch (error: any) {
      console.error(error);
      showAlert('Error', 'Could not load your history. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const formatDate = (dateStr: string) => {
    try {
      const d = new Date(dateStr);
      return d.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch {
      return dateStr;
    }
  };

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const renderItem = ({ item, index }: { item: PredictionRecord; index: number }) => {
    const isExpanded = expandedId === item.id;
    const imageUrl = item.image_url ? `${BASE_URL}${item.image_url}` : null;
    const isFresh = String(item.freshness).toLowerCase() === 'fresh';

    return (
      <Animated.View 
        entering={FadeInDown.delay(Math.min(index * 50, 500)).duration(400)} 
        layout={Layout.springify()} 
        style={styles.card}
      >
        <TouchableOpacity 
          style={styles.cardHeader} 
          activeOpacity={0.8}
          onPress={() => toggleExpand(item.id)}
        >
          {imageUrl ? (
            <Image source={{ uri: imageUrl }} style={styles.recordImage} />
          ) : (
            <View style={styles.placeholderImage}>
              <MaterialCommunityIcons name="image-off-outline" size={20} color="#94A3B8" />
            </View>
          )}

          <View style={styles.headerInfo}>
            <View style={styles.titleRow}>
              <Text style={styles.itemTitle}>{item.item}</Text>
              <View style={[styles.badge, isFresh ? styles.badgeGreen : styles.badgeRed]}>
                <Text style={[styles.badgeText, isFresh ? styles.badgeTextGreen : styles.badgeTextRed]}>
                  {String(item.freshness).toUpperCase()}
                </Text>
              </View>
            </View>
            <Text style={styles.dateText}>{formatDate(item.created_at)}</Text>
            <View style={styles.metaRow}>
              <MaterialCommunityIcons name="map-marker-outline" size={14} color="#64748B" />
              <Text style={styles.metaText}>{item.city.toUpperCase()}</Text>
              <View style={styles.dot} />
              <Text style={styles.metaText}>{(item.confidence * 100).toFixed(1)}% Confidence</Text>
            </View>
          </View>
          
          <MaterialCommunityIcons 
            name={isExpanded ? "chevron-up" : "chevron-down"} 
            size={24} 
            color="#166534" 
            style={styles.expandChevron} 
          />
        </TouchableOpacity>

        {isExpanded && (
          <Animated.View entering={FadeInUp.duration(300)} style={styles.expandedContent}>
            
            {/* Nutrition metrics */}
            <Text style={styles.sectionTitle}>Nutritional Profile (Serving Size: {item.nutritional_info?.serving_size || 'N/A'})</Text>
            {item.nutritional_info ? (
              <View style={styles.nutriGrid}>
                <View style={styles.nutriBox}>
                  <Text style={styles.nutriVal}>{item.nutritional_info.energy_kcal || 0}</Text>
                  <Text style={styles.nutriLbl}>kCal</Text>
                </View>
                <View style={styles.nutriBox}>
                  <Text style={styles.nutriVal}>{item.nutritional_info.protein_g || 0}g</Text>
                  <Text style={styles.nutriLbl}>Protein</Text>
                </View>
                <View style={styles.nutriBox}>
                  <Text style={styles.nutriVal}>{item.nutritional_info.fat_g || 0}g</Text>
                  <Text style={styles.nutriLbl}>Fat</Text>
                </View>
                <View style={styles.nutriBox}>
                  <Text style={styles.nutriVal}>{item.nutritional_info.carbs_g || 0}g</Text>
                  <Text style={styles.nutriLbl}>Carbs</Text>
                </View>
              </View>
            ) : (
              <Text style={styles.noDataText}>Nutrition data pending or not found.</Text>
            )}

            {/* Price statistics */}
            <Text style={styles.sectionTitle}>Saved Local Pricing (City: {item.city.toUpperCase()})</Text>
            {Array.isArray(item.district_pricing) && item.district_pricing.length > 0 ? (
              item.district_pricing.map((priceItem, pIdx) => (
                <View key={pIdx} style={styles.priceItem}>
                  <View style={styles.priceRowHeader}>
                    <Text style={styles.priceItemName}>{priceItem.item_name}</Text>
                    <View style={styles.sourceLabel}>
                      <Text style={styles.sourceLabelText}>
                        {priceItem.source === 'amisprizescrape' ? 'AMIS' : 
                         priceItem.source === 'psbaprizescrape' ? 'PSBA' : 
                         priceItem.source === 'pccmdprizescrape' ? 'PCCMD' : 'General'}
                      </Text>
                    </View>
                  </View>
                  <View style={styles.priceRowValues}>
                    {priceItem.min_price && (
                      <View style={styles.priceBlock}>
                        <Text style={styles.priceBlockLabel}>Min</Text>
                        <Text style={styles.priceBlockVal}>Rs {priceItem.min_price}</Text>
                      </View>
                    )}
                    {priceItem.dc_price && (
                      <View style={styles.priceBlock}>
                        <Text style={styles.priceBlockLabel}>DC</Text>
                        <Text style={styles.priceBlockVal}>Rs {priceItem.dc_price}</Text>
                      </View>
                    )}
                    {priceItem.psba_price && (
                      <View style={styles.priceBlock}>
                        <Text style={styles.priceBlockLabel}>PSBA</Text>
                        <Text style={styles.priceBlockVal}>Rs {priceItem.psba_price}</Text>
                      </View>
                    )}
                    {priceItem.max_price && (
                      <View style={styles.priceBlock}>
                        <Text style={styles.priceBlockLabel}>Max</Text>
                        <Text style={styles.priceBlockVal}>Rs {priceItem.max_price}</Text>
                      </View>
                    )}
                  </View>
                </View>
              ))
            ) : (
              <Text style={styles.noDataText}>No pricing data stored for this scan.</Text>
            )}
          </Animated.View>
        )}
      </Animated.View>
    );
  };

  return (
    <View style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
          <MaterialCommunityIcons name="arrow-left" size={24} color="#166534" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Scan History</Text>
        <TouchableOpacity style={styles.refreshBtn} onPress={fetchHistory}>
          <MaterialCommunityIcons name="refresh" size={24} color="#166534" />
        </TouchableOpacity>
      </View>

      {/* Main List */}
      {loading ? (
        <View style={styles.loaderContainer}>
          <ActivityIndicator size="large" color="#166534" />
          <Text style={styles.loadingText}>Fetching history log...</Text>
        </View>
      ) : (
        <FlatList
          data={history}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
          contentContainerStyle={styles.listContent}
          showsVerticalScrollIndicator={false}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <MaterialCommunityIcons name="archive-outline" size={70} color="#CBD5E1" />
              <Text style={styles.emptyText}>No predictions saved yet</Text>
              <Text style={styles.emptySubtext}>
                Scan your food fresh or raw, make sure you are logged in, and we will keep track of your scans here!
              </Text>
              <TouchableOpacity style={styles.emptyActionBtn} onPress={() => router.replace('/(tabs)')}>
                <Text style={styles.emptyActionBtnText}>Scan Now</Text>
              </TouchableOpacity>
            </View>
          }
        />
      )}
    </View>
  );
}
