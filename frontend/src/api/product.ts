import { apiClient } from './client';
import { Product } from '../types';

export const createProduct = async (product: Omit<Product, 'id' | 'created_at'>): Promise<{ id: number; message: string }> => {
  const response = await apiClient.post('/api/product/create', {
    name: product.name,
    category: product.category || 'Consumer Brand',
    description: product.description,
    features: Array.isArray(product.features) ? product.features.join(', ') : product.features || '',
    problem: product.problem_solved || '',
    audience: product.target_audience,
    price_range: product.price || '',
    competitors: '',
    platform: product.platform,
    tone: product.tone,
    requirements: product.requirements || '',
  });
  return {
    id: response.data.product_id,
    message: response.data.message,
  };
};

export const getProduct = async (id: number): Promise<Product> => {
  const response = await apiClient.get(`/api/product/${id}`);
  return {
    id: response.data.id,
    name: response.data.name,
    category: response.data.category,
    description: response.data.description,
    features: response.data.features ? String(response.data.features).split(',').map((item) => item.trim()).filter(Boolean) : [],
    problem_solved: response.data.problem,
    target_audience: response.data.audience,
    price: response.data.price_range,
    platform: response.data.platform,
    tone: response.data.tone,
    requirements: response.data.requirements,
    created_at: response.data.created_at,
  };
};
