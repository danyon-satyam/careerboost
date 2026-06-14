import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  sidebarOpen: false,
  activeModal: null,
  activePanels: [],
  toast: null,
  isPageLoading: false,
  theme: 'dark',
};

const uiSlice = createSlice({
  name: 'ui',
  initialState,
  reducers: {
    toggleSidebar: (state) => {
      state.sidebarOpen = !state.sidebarOpen;
    },
    setSidebarOpen: (state, action) => {
      state.sidebarOpen = action.payload;
    },
    openModal: (state, action) => {
      state.activeModal = action.payload;
    },
    closeModal: (state) => {
      state.activeModal = null;
    },
    openPanel: (state, action) => {
      if (!state.activePanels.includes(action.payload)) {
        state.activePanels.push(action.payload);
      }
    },
    closePanel: (state, action) => {
      state.activePanels = state.activePanels.filter(
        (p) => p !== action.payload
      );
    },
    showToast: (state, action) => {
      state.toast = action.payload;
    },
    clearToast: (state) => {
      state.toast = null;
    },
    setPageLoading: (state, action) => {
      state.isPageLoading = action.payload;
    },
  },
});

export const {
  toggleSidebar,
  setSidebarOpen,
  openModal,
  closeModal,
  openPanel,
  closePanel,
  showToast,
  clearToast,
  setPageLoading,
} = uiSlice.actions;

export default uiSlice.reducer;
