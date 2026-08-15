import { apiClient } from './client';

export const getHealth = async (): Promise<{ status: string; service: string }> => {
  const response = await apiClient.get('/api/health');
  return response.data;
};
