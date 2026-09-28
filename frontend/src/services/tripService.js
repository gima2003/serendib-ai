import { apiClient } from './apiClient';

export const tripService = {
  // TODO: Connect to actual FastAPI endpoints once they are ready
  
  async getCurrentTrip() {
    // return apiClient.get('/api/trips/current');
    return null;
  },

  async getUpcomingTrip() {
    return apiClient.get('/api/trips/upcoming');
  },

  async getAllTrips() {
    return apiClient.get('/api/trips');
  },

  async getCompletedTrips() {
    // return apiClient.get('/api/trips/completed');
    return [];
  },

  async saveTrip(tripData) {
    return apiClient.post('/api/trips', { trip_data: tripData });
  },

  // eslint-disable-next-line no-unused-vars
  async getCurrentBudget(tripId) {
    // return apiClient.get(`/api/trips/${tripId}/budget`);
    return null;
  },

  async getRecommendations() {
    const response = await apiClient.get('/api/trips/recommendations');
    return response.data;
  },

  // Planner endpoints
  // eslint-disable-next-line no-unused-vars
  async parseNaturalLanguageTrip(text) {
    return apiClient.post('/profile/extract', { text });
  },

  async requestClarificationPermission(userResponse, profile, readiness) {
  return apiClient.post('/profile/clarification/permission', {
    user_response: userResponse,
    profile,
    readiness,
  });
  },

  async submitClarificationAnswer(userAnswer, currentContext, profile) {
    return apiClient.post('/profile/clarification/answer', {
      user_answer: userAnswer,
      current_context: currentContext,
      profile,
    });
  },

  async getActivities() {
    // return apiClient.get('/api/activities');
    return [];
  },

  async generateTrip(planPayload) {
    // Determine if it's an NLP request or guided request
    let requestBody = {};
    
    if (planPayload.traveller_profile) {
      requestBody.traveller_profile = planPayload.traveller_profile;
    } else {
      // Fallback if the whole object is the profile (legacy)
      requestBody.traveller_profile = planPayload;
    }

    if (planPayload.raw_user_request) {
      requestBody.raw_user_request = planPayload.raw_user_request;
    } else if (planPayload.text) {
      requestBody.raw_user_request = planPayload.text;
    }
    
    return apiClient.post('/api/trips/generate', requestBody);
  },

  // Workspace endpoints
  async getTrip(tripId) {
    return apiClient.get(`/api/trips/${tripId}`);
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
  },

  async submitGuidedPlanner(plan) {
  return apiClient.post('/profile/guided', plan);
  },
};
