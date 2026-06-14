import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  currentInterview: null,
  interviews: [],
  currentQuestion: null,
  questions: [],
  answers: [],
  isLoading: false,
  error: null,
};

const interviewSlice = createSlice({
  name: 'interview',
  initialState,
  reducers: {
    setCurrentInterview: (state, action) => {
      state.currentInterview = action.payload;
    },
    setInterviews: (state, action) => {
      state.interviews = action.payload;
    },
    setCurrentQuestion: (state, action) => {
      state.currentQuestion = action.payload;
    },
    setQuestions: (state, action) => {
      state.questions = action.payload;
    },
    addAnswer: (state, action) => {
      state.answers.push(action.payload);
    },
    setLoading: (state, action) => {
      state.isLoading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.isLoading = false;
    },
    resetInterview: (state) => {
      state.currentInterview = null;
      state.currentQuestion = null;
      state.questions = [];
      state.answers = [];
      state.error = null;
    },
  },
});

export const {
  setCurrentInterview,
  setInterviews,
  setCurrentQuestion,
  setQuestions,
  addAnswer,
  setLoading,
  setError,
  resetInterview,
} = interviewSlice.actions;

export default interviewSlice.reducer;
