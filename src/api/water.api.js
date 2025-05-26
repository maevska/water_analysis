import axiosInstance from './axios.config';

export const waterApi = {
    predict: async (data) => {
        try {
            const response = await axiosInstance.post('/predict', data);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Ошибка при получении предсказаний');
        }
    },

    generateReport: async (data) => {
        try {
            const response = await axiosInstance.post('/generate-report', data, {
                responseType: 'blob'
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Ошибка при генерации отчета');
        }
    },

    getUserStats: async (userId) => {
        try {
            const response = await axiosInstance.get(`/users/${userId}/stats`);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Ошибка при получении статистики');
        }
    },

    getUserPredictions: async (userId, skip = 0, limit = 10) => {
        try {
            const response = await axiosInstance.get(`/users/${userId}/predictions`, {
                params: { skip, limit }
            });
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data?.detail || 'Ошибка при получении истории прогнозов');
        }
    }
}; 