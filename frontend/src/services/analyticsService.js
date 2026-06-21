import api from './api.js';

export const analyticsService = {
  async getDashboard() {
    const response = await api.get('/analytics/dashboard');
    return response.data;
  },

  async getInterviewAnalytics() {
    const response = await api.get('/analytics/interviews');
    return response.data;
  },

  async getTypingAnalytics() {
    const response = await api.get('/analytics/typing');
    return response.data;
  },
};

export default analyticsService;
