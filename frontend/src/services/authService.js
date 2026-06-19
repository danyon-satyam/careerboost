import api from './api.js';

export const authService = {
  async signup({ email, password, full_name }) {
    const response = await api.post('/auth/signup', {
      email,
      password,
      full_name,
    });
    return response.data;
  },

  async login({ email, password }) {
    const response = await api.post('/auth/login', {
      email,
      password,
    });
    return response.data;
  },

  async getProfile() {
    const response = await api.get('/users/profile');
    return response.data;
  },
};

export default authService;
