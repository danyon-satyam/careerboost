import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentTest: null,
  testText: '',
  typedText: '',
  startTime: null,
  isActive: false,
  isFinished: false,
  results: null,
  history: [],
  progress: null,
  isLoading: false,
  error: null,
};

const typingSlice = createSlice({
  name: 'typing',
  initialState,
  reducers: {
    setTestText: (state, action) => {
      state.testText = action.payload;
      state.typedText = '';
      state.isFinished = false;
      state.results = null;
    },
    setTypedText: (state, action) => {
      state.typedText = action.payload;
    },
    startTest: (state) => {
      state.isActive = true;
      state.startTime = Date.now();
      state.isFinished = false;
    },
    finishTest: (state, action) => {
      state.isActive = false;
      state.isFinished = true;
      state.results = action.payload;
    },
    setHistory: (state, action) => {
      state.history = action.payload;
    },
    setProgress: (state, action) => {
      state.progress = action.payload;
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    resetTest: (state) => {
      state.typedText = '';
      state.startTime = null;
      state.isActive = false;
      state.isFinished = false;
      state.results = null;
    },
  },
});

export const {
  setTestText,
  setTypedText,
  startTest,
  finishTest,
  setHistory,
  setProgress,
  setLoading,
  setError,
  resetTest,
} = typingSlice.actions;

export default typingSlice.reducer;
