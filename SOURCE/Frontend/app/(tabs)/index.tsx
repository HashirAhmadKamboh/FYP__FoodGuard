import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, ScrollView, ActivityIndicator, Alert, Platform, BackHandler } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { api, BASE_URL } from '../../constants/api';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as FileSystem from 'expo-file-system';
import Animated, { FadeIn, FadeInDown } from 'react-native-reanimated';
import { useRouter } from 'expo-router';
import { useIsFocused } from '@react-navigation/native';
import styles from '../../styles/home.styles';

let welcomeShown = false;

export default function HomeScreen() {
  const router = useRouter();
  const isFocused = useIsFocused();
  const [image, setImage] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [district, setDistrict] = useState<string>('lahore');
  const [userProfile, setUserProfile] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  useEffect(() => {
    if (!welcomeShown) {
      welcomeShown = true;
      const welcomeTitle = "Welcome to FoodGuard";
      const welcomeText = "FoodGuard helps users check food freshness, nutrition information, and market prices.\n\n" +
        "The AI model is trained on selected food categories such as fruits, vegetables, chicken, fish, and meat, and achieved approximately 81% accuracy during testing. For better results, please upload clear images of supported food items only.\n\n" +
        "Market prices are collected from official Government of Punjab sources:\n\n" +
        "AMIS.pk â€” Agriculture Marketing Information Service, used for agriculture and market price information.\n\n" +
        "PCCMD Punjab â€” Price Control and Commodities Management Department.\n\n" +
        "PSBA Punjab â€” Punjab Sahulat Bazaars Authority.\n\n" +
        "Nutrition information is also based on valid food nutrition sources.\n\n" +
        "Please use the AI prediction feature within its trained categories.";
        
      if (Platform.OS === 'web') {
        alert(`${welcomeTitle}\n\n${welcomeText}`);
      } else {
        Alert.alert(
          welcomeTitle,
          welcomeText,
          [{ text: "OK" }]
        );
      }
    }
  }, []);

  useEffect(() => {
    const backAction = () => {
      if (isFocused) {
        Alert.alert("Exit App", "Are you sure you want to exit the app?", [
          {
            text: "No",
            onPress: () => null,
            style: "cancel"
          },
          { text: "Yes", onPress: () => BackHandler.exitApp() }
        ]);
        return true;
      }
      return false;
    };

    const backHandler = BackHandler.addEventListener(
      "hardwareBackPress",
      backAction
    );

    return () => backHandler.remove();
  }, [isFocused]);

  useEffect(() => {
    const loadDistrictAndAuth = async () => {
      const dist = await AsyncStorage.getItem('user_district');
      if (dist) setDistrict(dist);
      
      const token = await AsyncStorage.getItem('user_token');
      const profileStr = await AsyncStorage.getItem('user_profile');
      if (token && profileStr) {
        try {
          setUserProfile(JSON.parse(profileStr));
        } catch {
          setUserProfile(null);
        }
      } else {
        setUserProfile(null);
      }
    };
    if (isFocused) {
      loadDistrictAndAuth();
    }
  }, [isFocused]);

  const handleShowSupportedItems = () => {
    const title = "Supported AI Prediction Categories";
    const message = "Fruits:\nApple, Banana, Grape, Guava, Jujube, Mango, Orange, Pomegranate, Strawberry\n\n" +
      "Vegetables:\nBell Pepper, Bitter Gourd, Capsicum, Carrot, Cucumber, Okra, Potato, Tomato\n\n" +
      "Meat & Protein Items:\nChicken, Fish, Meat\n\n" +
      "Other:\nNon-Food";

    if (Platform.OS === 'web') {
      alert(`${title}\n\n${message}`);
    } else {
      Alert.alert(title, message, [{ text: "OK" }]);
    }
  };

  const pickImage = async (useCamera: boolean) => {
    let permissionResult;
    if (useCamera) {
      permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    } else {
      permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    }

    if (permissionResult.granted === false) {
      setErrorMessage(`Camera/Gallery permission needed! Please grant permission to select food images.`);
      return;
    }

    let pickerResult = useCamera
      ? await ImagePicker.launchCameraAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        })
      : await ImagePicker.launchImageLibraryAsync({
          mediaTypes: ImagePicker.MediaTypeOptions.Images,
          allowsEditing: true,
          aspect: [4, 3],
          quality: 0.8,
        });

    if (!pickerResult.canceled) {
      setImage(pickerResult.assets[0].uri);
      setResult(null); // Clear previous results
      setErrorMessage(null); // Clear previous errors
    }
  };

  const handleLogout = async () => {
    const performLogout = async () => {
      await AsyncStorage.removeItem('user_token');
      await AsyncStorage.removeItem('user_profile');
      setUserProfile(null);
      setErrorMessage(null);
      if (Platform.OS === 'web') {
        alert('Logged out successfully');
      } else {
        Alert.alert('Success', 'Logged out successfully');
      }
    };

    if (Platform.OS === 'web') {
      const confirmed = window.confirm('Are you sure you want to log out?');
      if (confirmed) {
        await performLogout();
      }
    } else {
      Alert.alert(
        'Logout',
        'Are you sure you want to log out?',
        [
          { text: 'Cancel', style: 'cancel' },
          { 
            text: 'Logout', 
            style: 'destructive',
            onPress: performLogout
          }
        ]
      );
    }
  };

  const handlePredict = async () => {
    if (!image) {
      setErrorMessage("Please select an image first.");
      return;
    }
    
    setLoading(true);
    setResult(null);
    setErrorMessage(null);
    try {
      // Read image as base64 to completely bypass React Native's Android FormData file bugs
      let base64String: string;
      if (Platform.OS === 'web') {
        const response = await fetch(image);
        const blob = await response.blob();
        base64String = await new Promise<string>((resolve, reject) => {
          const reader = new FileReader();
          reader.onloadend = () => resolve(reader.result as string);
          reader.onerror = reject;
          reader.readAsDataURL(blob);
        });
      } else {
        base64String = await FileSystem.readAsStringAsync(image, { encoding: FileSystem.EncodingType.Base64 });
      }
      
      const token = await AsyncStorage.getItem('user_token');
      const headers: any = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${BASE_URL}/predict/base64`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          file_base64: base64String,
          city: district || 'lahore'
        })
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`HTTP error! status: ${response.status} body: ${errorText}`);
      }

      const data = await response.json();
      
      if (!data || !data.ai_prediction) {
        throw new Error("Invalid response: " + JSON.stringify(data));
      }
      
      setResult(data);

    } catch (error: any) {
      console.error("Predict Error: ", error);
      setErrorMessage(`Error: ${error.message}\n\nPlease check if your FastAPI backend is running and the URL in api.ts is correct.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container} showsVerticalScrollIndicator={false}>
      
      {/* Dynamic Header with District and Auth Actions */}
      <Animated.View entering={FadeInDown.duration(600)} style={styles.headerArea}>
        <View style={styles.headerTop}>
          <Text style={styles.title}>AI Analysis</Text>
          
          {userProfile ? (
            <View style={styles.userActionGroup}>
              <TouchableOpacity 
                style={styles.historyIconBtn}
                onPress={() => router.push('/history')}
              >
                <MaterialCommunityIcons name="history" size={22} color="#166534" />
              </TouchableOpacity>
              <TouchableOpacity 
                style={styles.logoutIconBtn}
                onPress={handleLogout}
              >
                <MaterialCommunityIcons name="logout" size={20} color="#991B1B" />
              </TouchableOpacity>
            </View>
          ) : (
            <TouchableOpacity 
              style={styles.loginBtn}
              onPress={() => router.push('/login')}
            >
              <Text style={styles.loginBtnText}>Login</Text>
            </TouchableOpacity>
          )}
        </View>

        <View style={styles.headerSecondaryRow}>
          <TouchableOpacity 
            style={styles.supportedItemsBtn} 
            onPress={handleShowSupportedItems}
          >
            <MaterialCommunityIcons name="food-apple-outline" size={14} color="#166534" />
            <Text style={styles.supportedItemsText}>Supported Items</Text>
          </TouchableOpacity>

          <TouchableOpacity 
            style={styles.changeDistBtn} 
            onPress={() => router.push('/district')}
          >
            <MaterialCommunityIcons name="map-marker" size={14} color="#166534" />
            <Text style={styles.changeDistText}>{district.toUpperCase()}</Text>
          </TouchableOpacity>
        </View>
        <Text style={styles.subtitle}>Upload food to verify freshness and view local prices</Text>
      </Animated.View>

      {/* Image Picker Card */}
      <Animated.View entering={FadeInDown.delay(100).duration(600)} style={styles.card}>
        <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.primaryButton} onPress={() => pickImage(true)}>
            <MaterialCommunityIcons name="camera-iris" size={24} color="#fff" />
            <Text style={styles.buttonText}>Camera</Text>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.secondaryButton} onPress={() => pickImage(false)}>
            <MaterialCommunityIcons name="image-multiple-outline" size={24} color="#1B5E20" />
            <Text style={styles.secondaryButtonText}>Gallery</Text>
          </TouchableOpacity>
        </View>

        {image ? (
          <Animated.View entering={FadeIn} style={styles.imageWrapper}>
            <Image source={{ uri: image }} style={styles.image} />
          </Animated.View>
        ) : (
          <View style={styles.placeholderBox}>
            <MaterialCommunityIcons name="cloud-upload-outline" size={60} color="#CBD5E1" />
            <Text style={styles.placeholderText}>Tap buttons above to upload</Text>
          </View>
        )}

        {/* The Predict Action Button */}
        {image && !loading && !result && (
          <Animated.View entering={FadeInDown}>
            <TouchableOpacity style={styles.predictActionButton} onPress={handlePredict}>
              <MaterialCommunityIcons name="brain" size={24} color="#fff" />
              <Text style={styles.predictActionText}>PREDICT NOW</Text>
            </TouchableOpacity>
          </Animated.View>
        )}
      </Animated.View>

      {/* Error Message Banner */}
      {errorMessage && (
        <Animated.View entering={FadeInDown.duration(400)} style={styles.errorBanner}>
          <MaterialCommunityIcons name="alert-circle-outline" size={24} color="#B91C1C" />
          <View style={styles.errorTextWrapper}>
            <Text style={styles.errorBannerTitle}>Prediction Failed</Text>
            <Text style={styles.errorBannerText}>{errorMessage}</Text>
          </View>
        </Animated.View>
      )}

      {/* Loading State */}
      {loading && (
        <Animated.View entering={FadeIn} exiting={FadeIn} style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#166534" />
          <Text style={styles.loadingText}>Running AI Models...</Text>
        </Animated.View>
      )}

      {/* Localized Prediction Result Render */}
      {result && (
        <Animated.View entering={FadeInDown.duration(600)} style={styles.resultsWrapper}>
          
          {/* Detection Result */}
          {result.ai_prediction && (
            <View style={[styles.resultCard, result.ai_prediction.is_food === false ? styles.irrelevantCard : styles.predictionCard]}>
              <View style={styles.cardHeader}>
                <MaterialCommunityIcons 
                  name={result.ai_prediction.is_food === false ? "image-filter-center-focus-weak" : "brain"} 
                  size={24} 
                  color={result.ai_prediction.is_food === false ? "#64748B" : "#166534"} 
                />
                <Text style={[styles.cardTitle, result.ai_prediction.is_food === false && { color: '#64748B' }]}>
                  {result.ai_prediction.is_food === false ? "Irrelevant Image" : "Detection"}
                </Text>
              </View>
              {result.ai_prediction.is_food === false ? (
                <View style={styles.irrelevantContent}>
                  <Text style={styles.irrelevantText}>Non-Food Item / Irrelevant</Text>
                  <Text style={styles.irrelevantSubtext}>Please upload a clear picture of food (fruits, vegetables, chicken, fish, or meat).</Text>
                </View>
              ) : (
                <>
                  <View style={styles.predRow}>
                    <Text style={styles.predLabel}>Item:</Text>
                    <Text style={styles.predValue}>{result.ai_prediction.item}</Text>
                  </View>
                  <View style={styles.predRow}>
                    <Text style={styles.predLabel}>Confidence:</Text>
                    <Text style={styles.predValue}>{(result.ai_prediction.item_confidence * 100).toFixed(1)}%</Text>
                  </View>
                  <View style={styles.predRow}>
                    <Text style={styles.predLabel}>Freshness:</Text>
                    <View style={[styles.badge, String(result.ai_prediction.freshness).toLowerCase() === 'fresh' ? styles.badgeGreen : styles.badgeRed]}>
                      <Text style={[styles.badgeText, String(result.ai_prediction.freshness).toLowerCase() === 'fresh' ? styles.badgeTextGreen : styles.badgeTextRed]}>
                        {result.ai_prediction.freshness ? String(result.ai_prediction.freshness).toUpperCase() : ''}
                      </Text>
                    </View>
                  </View>
                </>
              )}
            </View>
          )}

          {/* Pricing Result */}
          {result.ai_prediction && result.ai_prediction.is_food !== false && (
            <View style={[styles.resultCard, styles.pricingCard]}>
              <View style={styles.cardHeader}>
                <MaterialCommunityIcons name="cash-multiple" size={24} color="#0369A1" />
                <Text style={[styles.cardTitle, {color: '#0369A1'}]}>Local Rates</Text>
              </View>
              {Array.isArray(result.district_pricing) && result.district_pricing.length > 0 ? (
                <View>
                  <Text style={styles.cityText}>in {result.district_pricing[0]?.city ? String(result.district_pricing[0].city).toUpperCase() : ''}</Text>
                  {result.district_pricing.map((priceItem: any, index: number) => (
                    <View key={index} style={styles.varietyContainer}>
                      <View style={styles.varietyHeaderRow}>
                        <Text style={styles.varietyName}>{priceItem.item_name}</Text>
                        <View style={styles.sourceBadge}>
                          <Text style={styles.sourceText}>
                            {priceItem.source === 'amisprizescrape' ? 'AMIS' : 
                             priceItem.source === 'psbaprizescrape' ? 'PSBA' : 
                             priceItem.source === 'pccmdprizescrape' ? 'PCCMD' : 'General'}
                          </Text>
                        </View>
                      </View>
                      <View style={styles.priceGrid}>
                        {priceItem.min_price !== null && (
                          <View style={[styles.priceBox, { backgroundColoTÃH¢ÿvIMÒÒüÃd|bâ‚äî]-¶á–à@~[êÛÔ&s7š~m?©Mê¸ùCÔD5a4†/Ã.ÓñA¤ÙoH®×Gæ^ñı7øÛ ¤Ksël«DùêQ¸İ}÷ÄÛbŸnób6˜•¦¹ÜzÃl“ó«-ì_zT®çûæËáÉr-¨?EÜBÛVÏQíÿ¨¡î„j(Ú³iDĞ‡È¼«Šïƒ±|„TN×nªµ4Û¥´{Ûåù„¼iäª+²¸hZx¡Û(´Á«¿x$ƒnX<“#$Ğşu(Ùù_9vç*ªş©ddOÛÓ6ôo¤š"İ`ØíÈŞŞ
BÙ•fTƒÉ`?ÃëêíW9ß8W!šJ“¹‹ZŒyUí]Ä&M‘´ÿÒâ£ÙVüŞë¢È™Z%WÏ8µæË Q»ÒÕ4TEç®RÚ¥e7dœìJ¬.i3/²oÏÃïVø0Áì¥½}¼tÆªõŸO¥7Y2/WÏ[ı0ıæÑÉ³¥Â_ôeãNU™æ—°’.4p<¬{¡ä2¥*gªŸ0",m‡£kßX¦D/Ko-4Çz»Ë æ¡@÷â„=âxq1á÷g2ëQ„Ğˆxïr.?:6ÕMã÷<…<MX+@
Ñ"¯Şº ;¥à6÷(oVr•
f·Mİ_62}+ ”9î5÷¨wp§çÎ
û@Ùv%X¶|9Ë~?Bg^šU®†ñ&ë1@“äü»ŸñŒçÀo:J½” ¿]-ƒmP‡qßRMÄø¡}‹­>3ª•»Ši)t!Qúét:HSl­—f”Dßƒ{%Ö~¾9[eS¾9½éŸË!´=Œ¥J!
šÄbÖD!ÇUdé)!8®@ÌRWvR`ÌœÖ@|«ì5®ºô¬_ÊNRë4ùÃÏĞÂôxszÉ"\IÚ_×6=–AìZ„GŠÍĞÕ¨€ùÙ,(âÜcµ³Ìú¤`Ì'ÎM÷Öıš‹9n'•Mú:²Ly»ã_¥G
ªÿ¦5„.œ™©1#VJÿo²§÷²–1Ó«áŞ Ã0ª`på÷¸,;OâñtC íÑÎ/ØùéÖm6Ù£MÖ?(ºÓ™]+¥ğ%Èrğc"ñ„ëôl¿ı x({	³`µ”ÂG6®L;Ş‹?ğRÄáK;íS‰Ò:Zi0g,Ç>Š&É†İ©^¹ãy0ˆ&ä0çá—¶ÚA‚Ğ,¹ï*kZü`–òĞÿ´ŸjÕ‹s7ï÷ ƒ‘Ê–®Ùíi%&ôklg©õ'n‚¬¦ÄÑ¾7àHÀi"=~½¦*‹¥Ø©_‚ü@¹%Èíèz;§†ƒ;s8´¯Ä¹èW"õ”’FÂ¢Ş€Ô	#İ.Îq9<W˜A lna¥¨0™Fk)%I¤ÑÄcÌ""u–Gâ+yÇ§äˆ[®ê]ìQ©~ÿ	‹Kd>~#ù˜64õñT1<âT¦£È7îm€tV¶Ÿó|^(Åtäqs7ãÂ2Ñaÿogğ‡z/jø 0ô+p½ì–ğP6ödJ'ÙQıˆ³q/Èíî)ŠÌqõ}%•)ÀÄ°a‘‹üêÄ\Çr@Ât^H|eÛÉğu7|è1EÀ@R‡ÃP'¸Ÿ­ŸÖÖz‡æ<m½a“N„ùÁY×šóB {[Å/ß¬2aù!s÷ñ¿êµLOj€´Ri~h˜Zªòé §ÉN%‰J÷&HINr…açDã9•ñw€ÁÚ®‚_yv`™ër—B"ñÑj[`=:n\*/ƒ>UÓUÃè!L(÷Aúú½Xi“hQ`Ê”ü_¿\™"”¡‚wñ2{×j6C¿X”àÅÿyKeeÄ0·ÿÔê1p—$[v8ˆ2ûJ çï	(”õ5è¤ m©å/…´<aD9*
³óœ–›+ïk_PQ1Y’‘¬‹´ö‡Õîk†Üõæ3¶ràÛA|åÖÏn"—ä™”÷=[à®åOEºÛ¯|F<¥şÕ!„•€.ó³Â¥ ÇoÔ€,’ö‹¹Í„¦Ø¦ X1VÌ©!'„swRwK¹ì¸÷_Ä‰<.š¶;ÔÖ;'"ƒ®9Âm·ŠHEşw‚û9ÙfÚ}êø1Õw§R¯‡m 0Ø®%vYg1 ğDÑŠÖ»ıN›ßìÑzâz·êç™™,ÃZ¢4/g¦Š¥µä¶P|:9õŒ-0{aVGéÆVõ…Ô× |%Á¨‹Iı“Â%@ï»"Ş`ô$¿P Æ³È°Ùá«–”­Ô2pğ!  nÆm™&ş<Üµ"^¤Eüé#¤«~½TE;èûEX””:*ÿù4Òé‘C®` W½f—ÿÙºo|÷˜ï4Ü-ë·—ç{¸÷¨<¤½!ñ´S3¶¨aœó=Q^ËggËAWxşªÅ_ óİ[t”Š–(¨§hˆ>‘ÿ5™%öè@·#ï¶y‹ˆ{ŸzL'·Et1­Gû¶oxõ«wİ*ê!n&8ËŞB(Ê†»–ƒ½ÈÛ¤‰}ÔÖ“¯~‹Q:¢#fCöˆkÉ“ˆoQasO³„æ°eÉ5,GˆÿxAƒªC xâ~@b.^H¿,Ñ#r@Ò‚jö÷jL¦™R[<mİsçïIE®&ù<jäZ ¬PdGHô=W›B ëìúFSºı ”à¼»”[¤¯3¥ôì¥R“èŠ´qö]¾äNO<¬1»
7&†£,kîÃ›Ed?£«U9qqNÈƒÛÌõX›6 €3»Æ³`vÈïòÀbiÒñHÄ¨²hƒ“ä°Gp¸JšAÍ¿dºŞ­'­Ü§|*]ÜíéÉ¤xãêoOœbó/Ä¿<[I’ıİ|ªZ^ã’g,¦]ú)~XèÙ>ÇÊ¨B½$Š\*É5óÓ‡•œœ$SvıÓ(®Öø[QÈ÷Ò’’<1ÙnÓÅ€tœ#àĞç1¶M_¯`Wğ0C+cbx¶‹YßÃyµÙ@†<Ë…¯¤Z–8ë0f"Â>l£~ìf„ºŞzÎÉo1U¼®s
ğs,ÁÓâŞW‰uï€/_û&	ì¶³£bÛÂ‚—„9¢:±àz§Ğ|Ì­¤;ü‹ı<«RÊs¦‡¸ÔÒj/ˆ÷>úß¼ØÅœqÂøCßÊ(towÿêLá¹H÷é‡j1šFZ›L°WĞ|J?f™|K*ü–­ãÁ(÷ñí4`P}Õœ.§Ö?O0•~“I£”k ûW&ä:ó÷kuöX©É®ÇÂ!£a=Ú´j¹ù‘6[_ÎÁã9¿D\â´Sk]­´ñcc=;ë¹ÅnØ›8T“ÑÂöã9=‹•Ï4s©™œJ™%è.”P¶nH½vc;ş¢}¥±m:gtÆ‰"`¬ÁÕ/å.æc%Õˆ)ÁI“w< v«/!`Ç\#¤Í‹‰°|]ZØ™ÃXf_Ÿ·:E•1ÉÏ¯útÀÏpƒ®‹µY@ÇıÉ‹F3œ[¾>)µÔï;5ğ—ú–©ÈÅÁ,çp)ÕÙ.&=á~¨YKÑAbEz$V"s|P‚gÉ-ãêÍénÊ’æA¥63	qíŸ&]f ]¯
]†'íU	ÓHıÉ¹‰ò“šı‹ Â<vq÷ÎÀÄ¾jİ®œeöôŞy›J‡õXğ‘ûLqîa¡ŸŞí•ÓcNQ­oL@.¦r£†ì\L2¡¹”}ÔsX«˜j¡í¨ù {
î¹óû3aõX²ò‡\T¸,x÷&Ó·€åÊèÒÙ7U¬u·òÜª Úz¨ó´ÔqtõŞÀF®XÅRy
ï© TíB˜œšiƒÖ¹¾„	=’Eñ¼€ÊìV†…Pe¼VJê&eª°­:ƒºúnx]ıñc&aMKMƒ~dË‘T!U*[%c«—ŸQQ
üv¯úŒÉŸÙ*ß‚sò±úu{ìâi<9%Øêú¾÷ubä5'CšŠZIHútq41)“™îõeŸ@e	úã”¦Ù]¡¯âNHÂ¬öß~¦»GÇTwnd„u=áÃÉNgŒ‹û/1|ä÷kSÊ^«>ì|Ğçbí³a}µğàâc„SĞ…¤uAÃ]Rš3ô•å°DR-´à ôÏù>ËğÚÿ½Ú,ÛR0Püâ—?Œî¡Ëé„ióâdÇÿkù»/j²_ûä/Åææãú……–Ğ%yóÉñ|fÎÑWSĞHÃpºq†ÄŒªÎ‚ñYCï ù©ê¦ÛªÓ¹$#§ÀİMG-D÷b«÷ØWò¯û+=lä~ÀŞ38ö?§?à˜
"Öor_úF,ÓG¼Z~Ê «F°ÊOp">}ksïQHOi®P¾§¾í«ˆAª²¢u¬|u’fÈ©‡“Wcx³ÖãÜƒÉ¦Ac95:&@`êp\ƒ~1ÚiñÜFçÖSLí@‘¹åš çßÜ‰ØRtVÂñ‰òØ.Ù”c¾ñÖFuuŒFCÒèÏèå¯ËÀ‰>¨
õ:¡Õ·n¥‘7*RÈßÌÒz"ß»ÊÈòü/~ * –üm®Ş[Va`„@(0ªú§ÜöÑQi±°¨lA.—áš;úã[a‹4CTª22cõ0OuÔµ0ˆrQ.t#êÖˆ™Ã‚²>Âu£ˆ¨‚Šyµós!m£á»ÚiŸ”ÇÖ”Ç|aÍÆø®@$Ãf…fDËbÃ r2I3ILY{ıñ uE·;lpG<*¬û›Ù`dlâ¼õ¯÷Ä÷°ñ<k¼À…MŠ Ä&C(¤’üWFa¯×Zî²9ÆÂ 2Š¦İGhƒ‚%²šöX^ïz<HÈ¿×¶º·?"nÇâ¼³„E¥Òé[‘¸."ÎdşèrŞ­ÅÙ¾:İåL?h