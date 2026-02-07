import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const STATUS_OPTIONS = ['New', 'Contacted', 'Sample Sent', 'Negotiation', 'Closed', 'Lost'];
export const BUYER_TYPES = ['Importer', 'Wholesaler', 'Processor'];
export const SOURCE_OPTIONS = ['Google Maps', 'B2B', 'LinkedIn', 'Manual'];
export const PRODUCT_OPTIONS = ['Turmeric', 'Dal', 'Multiple'];
