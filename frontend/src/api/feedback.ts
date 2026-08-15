import { apiClient } from './client';
import { Feedback, FeedbackResponse } from '../types';

export const submitFeedback = async (feedback: Feedback): Promise<FeedbackResponse> => {
  const response = await apiClient.post('/api/feedback', feedback);
  return response.data;
};
