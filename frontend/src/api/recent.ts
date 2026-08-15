import { apiClient } from './client';
import { RecentGenerationsResponse, Trend } from '../types';

export const getRecent = async (): Promise<RecentGenerationsResponse> => {
  const response = await apiClient.get('/api/recent');
  return response.data;
};

// Assuming there's a trends endpoint as requested in step 14, although it wasn't built in the backend previously.
// Wait, we didn't build GET /api/trends in the backend. 
// Let me double check if I should fetch from the raw json or if I need to add that endpoint to the backend.
// The prompt says "Call GET /api/trends". 
export const getTrends = async (): Promise<any> => {
  const response = await apiClient.get('/api/trends');
  return response.data;
};
