// filepath: my-fullstack-app/frontend/src/utils/extractor.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL; // Use environment variable for the backend API URL

export const postBlogUrl = async (url: string) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/extract`, { url });
        return response.data;
    } catch (error: unknown) {
        if ((error as any).isAxiosError) {
            throw new Error('Axios error: ' + (error as any).message);
        }
        throw new Error('Unknown error occurred');
    }
};

export const checkStatus = async (jobId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/status/${jobId}`);
        return response.data;
    } catch (error: unknown) {
        if ((error as any).isAxiosError) {
            throw new Error('Axios error: ' + (error as any).message);
        }
        throw new Error('Unknown error occurred');
    }
};

export const fetchResults = async (jobId: string) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/results/${jobId}`);
        return response.data;
    } catch (error: unknown) {
        if ((error as any).isAxiosError) {
            throw new Error('Axios error: ' + (error as any).message);
        }
        throw new Error('Unknown error occurred');
    }
};