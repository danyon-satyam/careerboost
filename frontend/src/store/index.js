import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import interviewReducer from './slices/interviewSlice';
import jobReducer from './slices/jobSlice';
import typingReducer from './slices/typingSlice';
import uiReducer from './slices/uiSlice';
import candidateReducer from './slices/candidateSlice.js';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    interview: interviewReducer,
    jobs: jobReducer,
    typing: typingReducer,
    ui: uiReducer,
    candidate: candidateReducer,
  },
});

export default store;
