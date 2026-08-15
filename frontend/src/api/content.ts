import { apiClient } from './client';
import { Generation } from '../types';

export const generateContent = async (productId: number): Promise<Generation> => {
  const response = await apiClient.post('/api/content/generate', { product_id: productId });
  return response.data;
};
