import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  jobs: [],
  currentJob: null,
  recommendations: [],
  filters: {
    location: '',
    job_type: '',
    search: '',
  },
  pagination: {
    page: 1,
    page_size: 20,
    total: 0,
  },
  isLoading: false,
  error: null,
};

const jobSlice = createSlice({
  name: 'jobs',
  initialState,
  reducers: {
    setJobs: (state, action) => {
      state.jobs = action.payload.jobs;
      state.pagination.total = action.payload.total;
    },
    setCurrentJob: (state, action) => {
      state.currentJob = action.payload;
    },
    setRecommendations: (state, action) => {
      state.recommendations = action.payload;
    },
    setFilters: (state, action) => {
      state.filters = { ...state.filters, ...action.payload };
    },
    setPage: (state, action) => {
      state.pagination.page = action.payload;
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    clearFilters: (state) => {
      state.filters = { location: '', job_type: '', search: '' };
      state.pagination.page = 1;
    },
  },
});

export const {
  setJobs,
  setCurrentJob,
  setRecommendations,
  setFilters,
  setPage,
  setLoading,
  setError,
  clearFilters,
} = jobSlice.actions;

export default jobSlice.reducer;
