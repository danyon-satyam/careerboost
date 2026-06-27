import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  interviewId: null,
  jobTitle: null,
  company: null,
  totalQuestions: 0,
  candidate: {
    full_name: '',
    email: '',
    experience_years: '',
    gender: '',
  },
  currentStep: 0,
  permissionsGranted: {
    camera: false,
    microphone: false,
    screen: false,
    fullscreen: false,
  },
  isReady: false,
};

const candidateSlice = createSlice({
  name: 'candidate',
  initialState,
  reducers: {
    setInterviewContext: function (state, action) {
      state.interviewId = action.payload.interviewId;
      state.jobTitle = action.payload.jobTitle;
      state.company = action.payload.company;
      state.totalQuestions = action.payload.totalQuestions;
    },
    setCandidateDetails: function (state, action) {
      state.candidate = Object.assign(
        {},
        state.candidate,
        action.payload
      );
    },
    setCurrentStep: function (state, action) {
      state.currentStep = action.payload;
    },
    setPermission: function (state, action) {
      state.permissionsGranted[action.payload.key] =
        action.payload.value;
    },
    setReady: function (state, action) {
      state.isReady = action.payload;
    },
    resetCandidate: function () {
      return initialState;
    },
  },
});

export const {
  setInterviewContext,
  setCandidateDetails,
  setCurrentStep,
  setPermission,
  setReady,
  resetCandidate,
} = candidateSlice.actions;

export default candidateSlice.reducer;
