import axios from 'axios';

// Note: Next.js uses process.env.NEXT_PUBLIC_* for client-side env vars.
// We also check VITE_API_URL if it happens to be set.
const API_URL = 
  process.env.NEXT_PUBLIC_API_URL || 
  process.env.VITE_API_URL || 
  'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
