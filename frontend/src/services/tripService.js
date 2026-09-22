export const tripService = {
  // TODO: Connect to actual FastAPI endpoints once they are ready
  
  async getCurrentTrip() {
    // return apiClient.get('/api/trips/current');
    return null;
  },

  async getUpcomingTrips() {
    // return apiClient.get('/api/trips/upcoming');
    return [];
  },

  async getSavedTrips() {
    // return apiClient.get('/api/trips/saved');
    return [];
  },

  async getCompletedTrips() {
    // return apiClient.get('/api/trips/completed');
    return [];
  },

  // eslint-disable-next-line no-unused-vars
  async getCurrentBudget(tripId) {
    // return apiClient.get(`/api/trips/${tripId}/budget`);
    return null;
  },

  async getRecommendations() {
    // return apiClient.get('/api/recommendations');
    return [];
  },

  // Planner endpoints
  // eslint-disable-next-line no-unused-vars
  async parseNaturalLanguageTrip(text) {
    // return apiClient.post('/api/planner/parse-nlp', { text });
    return null;
  },

  async getActivities() {
    // return apiClient.get('/api/activities');
    return [];
  },

  // eslint-disable-next-line no-unused-vars
  async generateTrip(planPayload) {
    // return apiClient.post('/api/trips/generate', planPayload);
    return { id: 'new-trip-id' };
  },

  // Workspace endpoints
  // eslint-disable-next-line no-unused-vars
  async getTrip(tripId) {
    // return apiClient.get(`/api/trips/${tripId}`);
    return null;
  },

  // eslint-disable-next-line no-unused-vars
  async updateTrip(tripId, updates) {
    // return apiClient.patch(`/api/trips/${tripId}`, updates);
    return null;
  },

  // eslint-disable-next-line no-unused-vars
  async getTripBudget(tripId) {
    // return apiClient.get(`/api/trips/${tripId}/budget`);
    return null;
  },

  // eslint-disable-next-line no-unused-vars
  async getTripRoute(tripId) {
    // return apiClient.get(`/api/trips/${tripId}/route`);
    return null;
  }
};
