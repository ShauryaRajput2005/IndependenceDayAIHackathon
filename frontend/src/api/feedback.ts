import { apiClient } from './client';
import { Feedback, FeedbackResponse } from '../types';

export const submitFeedback = async (feedback: Feedback): Promise<FeedbackResponse> => {
  const response = await apiClient.post('/api/feedback/create', {
    generation_id: feedback.generation_id,
    feedback: [feedback.feedback_type, feedback.comment].filter(Boolean).join(': '),
    sentiment: 'Positive',
  });
  return {
    id: response.data.feedback_id,
    generation_id: feedback.generation_id,
    feedback_type: feedback.feedback_type,
    comment: response.data.preference,
    created_at: new Date().toISOString(),
    preference_saved: true,
  };
};
