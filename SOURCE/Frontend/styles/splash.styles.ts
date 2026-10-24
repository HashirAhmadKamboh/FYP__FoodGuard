import { StyleSheet, Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

export default StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },
  iconContainer: {
    marginBottom: 30,
    shadowColor: '#166534',
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.3,
    shadowRadius: 20,
    elevation: 10,
  },
  iconBackground: {
    width: 140,
    height: 140,
    borderRadius: 70,
    justifyContent: 'center',
    alignItems: 'center',
  },
  textContainer: {
    alignItems: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: '900',
    color: '#14532D',
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 16,
    color: '#15803D',
    marginTop: 8,
    fontWeight: '500',
    textAlign: 'center',
    paddingHorizontal: 40,
  },
  bottomContainer: {
    position: 'absolute',
    bottom: 50,
    width: width,
    paddingHorizontal: 24,
    alignItems: 'center',
  },
  button: {
    backgroundColor: '#166534',
    flexDirection: 'row',
    width: '100%',
    paddingVertical: 18,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#166534',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.4,
    shadowRadius: 12,
    elevation: 8,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700',
    marginRight: 10,
  },
  hint: {
    marginTop: 16,
    color: '#15803D',
    fontSize: 13,
    fontWeight: '500',
  }
});
