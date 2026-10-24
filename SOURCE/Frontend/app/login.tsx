import React, { useState } from 'react';
import { View, Text, TouchableOpacity, TextInput, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { BASE_URL } from '../constants/api';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import Animated, { FadeInDown, FadeInUp } from 'react-native-reanimated';
import styles from '../styles/login.styles';

export default function LoginScreen() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const updateEmail = (val: string) => {
    setEmail(val);
    setStatusMessage(null);
  };
  const updatePassword = (val: string) => {
    setPassword(val);
    setStatusMessage(null);
  };
  const updateName = (val: string) => {
    setName(val);
    setStatusMessage(null);
  };

  const handleAuth = async () => {
    if (!email || !password || (!isLogin && !name)) {
      setStatusMessage({ type: 'error', text: 'Please fill in all required fields.' });
      return;
    }

    if (!email.includes('@')) {
      setStatusMessage({ type: 'error', text: 'Please enter a valid email address containing "@".' });
      return;
    }

    if (password.length < 8) {
      setStatusMessage({ type: 'error', text: 'Password must be at least 8 characters long.' });
      return;
    }

    setLoading(true);
    setStatusMessage(null);

    try {
      if (isLogin) {
        // OAuth2 Password form requires x-www-form-urlencoded
        const details = {
          'username': email,
          'password': password,
        };
        const formBody = Object.keys(details)
          .map(key => encodeURIComponent(key) + '=' + encodeURIComponent(details[key as keyof typeof details]))
          .join('&');

        const response = await fetch(`${BASE_URL}/account/login`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
          },
          body: formBody,
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || 'Failed to login. Please check your credentials.');
        }

        const data = await response.json();
        if (data.access_token) {
          await AsyncStorage.setItem('user_token', data.access_token);
          
          // Fetch profile details
          const profileResponse = await fetch(`${BASE_URL}/account/me`, {
            headers: {
              'Authorization': `Bearer ${data.access_token}`,
            },
          });
          if (profileResponse.ok) {
            const profileData = await profileResponse.json();
            await AsyncStorage.setItem('user_profile', JSON.stringify(profileData));
          }
          
          router.replace('/(tabs)');
        } else {
          throw new Error('Access token not received.');
        }
      } else {
        // Register handles standard JSON
        const response = await fetch(`${BASE_URL}/account/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            password: password,
            name: name,
          }),
        });

        if (!response.ok) {
          const errData = await response.json();
          throw new Error(errData.detail || 'Registration failed. Email might already be registered.');
        }

        setStatusMessage({
          type: 'success',
          text: 'Signup complete! Please login now.'
        });
        setPassword('');
        setIsLogin(true);
      }
    } catch (error: any) {
      setStatusMessage({ type: 'error', text: error.message || 'Something went wrong. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <LinearGradient colors={['#F0FDF4', '#DCFCE7', '#BBF7D0']} style={styles.container}>
      <Animated.ScrollView contentContainerStyle={styles.scrollContainer} showsVerticalScrollIndicator={false}>
        
        {/* Back Button */}
        <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
          <MaterialCommunityIcons name="arrow-left" size={24} color="#166534" />
        </TouchableOpacity>

        {/* Header Logo & Title */}
        <Animated.View entering={FadeInUp.duration(600)} style={styles.header}>
          <LinearGradient colors={['#166534', '#15803D']} style={styles.logoBackground}>
            <MaterialCommunityIcons name="shield-lock-outline" size={48} color="#fff" />
          </LinearGradient>
          <Text style={styles.title}>{isLogin ? 'Welcome Back' : 'Create Account'}</Text>
          <Text style={styles.subtitle}>
            {isLogin ? 'Log in to save your AI food predictions and pricing history' : 'Sign up to keep track of food freshness and nutrition data'}
          </Text>
        </Animated.View>

        {/* Input Form */}
        <Animated.View entering={FadeInDown.delay(100).duration(600)} style={styles.card}>
          
          {/* Status Banner */}
          {statusMessage && (
            <Animated.View 
              entering={FadeInDown.duration(300)} 
              style={[
                styles.statusBanner, 
                statusMessage.type === 'success' ? styles.statusBannerSuccess : styles.statusBannerError
              ]}
            >
              <MaterialCommunityIcons 
                name={statusMessage.type === 'success' ? 'check-circle-outline' : 'alert-circle-outline'} 
                size={20} 
                color={statusMessage.type === 'success' ? '#15803D' : '#B91C1C'} 
              />
              <Text style={[
                styles.statusBannerText, 
                { color: statusMessage.type === 'success' ? '#15803D' : '#B91C1C' }
              ]}>
                {statusMessage.text}
              </Text>
            </Animated.View>
          )}

          {!isLogin && (
            <View style={styles.inputContainer}>
              <Text style={styles.label}>Full Name</Text>
              <View style={styles.inputWrapper}>
                <MaterialCommunityIcons name="account-outline" size={20} color="#15803D" style={styles.inputIcon} />
                <TextInput
                  style={styles.input}
                  placeholder="Enter your name"
                  placeholderTextColor="#94A3B8"
                  value={name}
                  onChangeText={updateName}
                />
              </View>
            </View>
          )}

          <View style={styles.inputContainer}>
            <Text style={styles.label}>Email Address</Text>
            <View style={styles.inputWrapper}>
              <MaterialCommunityIcons name="email-outline" size={20} color="#15803D" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Enter your email"
                placeholderTextColor="#94A3B8"
                keyboardType="email-address"
                autoCapitalize="none"
                value={email}
                onChangeText={updateEmail}
              />
            </View>
          </View>

          <View style={styles.inputContainer}>
            <Text style={styles.label}>Password</Text>
            <View style={styles.inputWrapper}>
              <MaterialCommunityIcons name="lock-outline" size={20} color="#15803D" style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Enter your password"
                placeholderTextColor="#94A3B8"
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                value={password}
                onChangeText={updatePassword}
              />
              <TouchableOpacity onPress={() => setShowPassword(!showPassword)} style={styles.eyeIcon}>
                <MaterialCommunityIcons name={showPassword ? "eye-off-outline" : "eye-outline"} size={20} color="#64748B" />
              </TouchableOpacity>
            </View>
          </View>

          {/* Submit Button */}
          <TouchableOpacity 
            style={styles.submitBtn} 
            activeOpacity={0.8}
            onPress={handleAuth}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color="#fff" size="small" />
            ) : (
              <>
                <Text style={styles.submitBtnText}>{isLogin ? 'LOG IN' : 'SIGN UP'}</Text>
                <MaterialCommunityIcons name="arrow-right" size={20} color="#fff" style={{ marginLeft: 8 }} />
              </>
            )}
          </TouchableOpacity>

          {/* Toggle Login/Signup */}
          <TouchableOpacity 
            style={styles.toggleBtn} 
            onPress={() => {
              setIsLogin(!isLogin);
              setEmail('');
              setPassword('');
              setName('');
              setStatusMessage(null);
            }}
          >
            <Text style={styles.toggleText}>
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <Text style={styles.toggleTextLink}>{isLogin ? 'Sign Up' : 'Log In'}</Text>
            </Text>
          </TouchableOpacity>
        </Animated.View>
        
      </Animated.ScrollView>
    </LinearGradient>
  );
}
