import axios from 'axios';

// CHANGE THIS to your computer's current IPv4 address
export const BASE_URL = 'http://192.168.213.227:8000';

export const api = axios.create({
  baseURL: BASE_URL,
});

export const DISTRICTS = [
  "attock", "jhelum", "pakpattan", "bahawalnagar", "kasur", "rahimyarkhan",
  "rajanpur", "bahawalpur", "khanewal", "rawalpindi", "bhakkar",
  "sahiwal", "khushab", "chakwal", "sargodha", "lahore", "dgkhan",
  "sheikhupura", "faisalabad", "layyah", "mianwali", "sialkot",
  "gujranwala", "multan", "ttsingh", "lodhran", "gujrat",
  "vehari", "muzaffargarh", "nankana", "jhang", "narowal",
  "mandibahaudin", "hafizabad", "okara", "chiniot",
  "wazirabad", "murree", "talagang", "taunsasharif", "kotadu"
];