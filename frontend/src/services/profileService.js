import { apiClient } from './apiClient';

export const profileService = {
  async getProfile() {
    return apiClient.get('/api/auth/me');
  },

  async updateProfile(profileData) {
    return apiClient.patch('/api/auth/me', profileData);
  }
};
