import { useEffect } from 'react';
import { View, Text, TouchableOpacity } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown, FadeIn } from 'react-native-reanimated';
import styles from '../styles/splash.styles';

export default function SplashScreen() {
  const router = useRouter();

  useEffect(() => {
    const checkSetup = async () => {
      const savedDistrict = await AsyncStorage.getItem('user_district');
      if (savedDistrict) {
        // Delay slightly for effect before bypassing
        setTimeout(() => router.replace('/(tabs)'), 800);
      }
    };
    checkSetup();
  }, []);

  return (
    <LinearGradient colors={['#F0FDF4', '#DCFCE7', '#BBF7D0']} style={styles.container}>
      <Animated.View entering={FadeInDown.duration(1000).springify()} style={styles.iconContainer}>
        <LinearGradient colors={['#166534', '#15803D']} style={styles.iconBackground}>
          <MaterialCommunityIcons name="shield-check-outline" size={80} color="#fff" />
        </LinearGradient>
      </Animated.View>

      <Animated.View entering={FadeInDown.delay(200).duration(1000).springify()} style={styles.textContainer}>
        <Text style={styles.title}>FoodGuard</Text>
        <Text style={styles.subtitle}>Smart Food Safety & Pricing Analytics</Text>
      </Animated.View>

      <Animated.View entering={FadeIn.delay(600).duration(1000)} style={styles.bottomContainer}>
        <TouchableOpacity 
          style={styles.button}
          activeOpacity={0.8}
          onPress={() => router.push('/district')}
        >
          <Text style={styles.buttonText}>Select Your City</Text>
          <MaterialCommunityIcons name="map-marker-radius" size={24} color="#fff" />
        </TouchableOpacity>
        <Text style={styles.hint}>Set your location to see accurate local prices</Text>
      </Animated.View>
    </LinearGradient>
  );
}