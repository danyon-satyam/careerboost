import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import interviewReducer from './slices/interviewSlice';
import jobReducer from './slices/jobSlice';
import typingReducer from './slices/typingSlice';
import uiReducer from './slices/uiSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    interview: interviewReducer,
    jobs: jobReducer,
    typing: typingReducer,
    ui: uiReducer,
  },
});

export default store;
