import { apiClient } from './client';
import { Product } from '../types';

export const createProduct = async (product: Omit<Product, 'id' | 'created_at'>): Promise<{ id: number; message: string }> => {
  const response = await apiClient.post('/api/product/create', product);
  return response.data;
};

export const getProduct = async (id: number): Promise<Product> => {
  const response = await apiClient.get(`/api/product/${id}`);
  return response.data;
};
