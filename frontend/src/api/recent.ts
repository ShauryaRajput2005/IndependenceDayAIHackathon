import { apiClient } from './client';
import { RecentGenerationsResponse } from '../types';

export const getRecent = async (): Promise<RecentGenerationsResponse> => {
  const response = await apiClient.get('/api/recent');
  const items = (response.data || []).map((item: any) => ({
    id: item.generation_id,
    product_id: item.product_id,
    hook: item.response?.hook || 'Untitled angle',
    tone: item.tone,
    platform: item.response?.trend?.platform || item.response?.trend?.name || 'Generated',
    created_at: item.created_at,
  }));
  return {
    items,
    total: items.length,
  };
};

export const getTrends = async (): Promise<any> => {
  const response = await apiClient.post('/api/trends/analyze', {
    brand: 'KAIROS',
    industry: 'Consumer Brand',
    audience: 'Social media audience',
    limit: 10,
  });
  return response.data;
};
