import axios from 'axios';

// Ensure user_id exists in localStorage before any API call
if (!localStorage.getItem("user_id")) {
  localStorage.setItem("user_id", crypto.randomUUID());
}

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API,
      timeout: 120000,
    });

    // ✅ Request interceptor to add user_id and content-type
    this.client.interceptors.request.use(
      (config) => {
        const userId = localStorage.getItem("user_id");
        if (userId) {
          config.headers["user_id"] = userId;
        }
        config.headers["Content-Type"] = "application/json";
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('API Request Error:', error);
        return Promise.reject(error);
      }
    );

    // ✅ Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Response Error:', error);
        if (error.response?.status === 429) {
          throw new Error('Rate limit exceeded. Please try again in a few minutes.');
        } else if (error.response?.status === 503) {
          throw new Error('AI model is loading. Please wait and try again.');
        } else if (error.response?.data?.detail) {
          throw new Error(error.response.data.detail);
        }
        throw new Error(error.message || 'Something went wrong');
      }
    );
  }

  async generateTextContent(prompt, contentType) {
    const response = await this.client.post('/generate/text', {
      prompt,
      content_type: contentType
    });
    return response.data;
  }

  async generateImageContent(prompt) {
    const response = await this.client.post('/generate/image', {
      prompt,
      content_type: 'image'
    });
    return response.data;
  }

  async getHistory(limit = 50, offset = 0) {
    const response = await this.client.get('/history', {
      params: { limit, offset }
    });
    return response.data;
  }

  async toggleFavorite(itemId) {
    const response = await this.client.put(`/history/${itemId}/favorite`);
    return response.data;
  }

  async deleteHistoryItem(itemId) {
    const response = await this.client.delete(`/history/${itemId}`);
    return response.data;
  }

  async clearHistory() {
    const response = await this.client.delete('/history');
    return response.data;
  }

  async healthCheck() {
    const response = await this.client.get('/health');
    return response.data;
  }
}

export default new ApiService();
