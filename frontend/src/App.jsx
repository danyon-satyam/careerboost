import { Routes, Route } from "react-router-dom";
import AnimatedBackground from "./components/layout/AnimatedBackground";
import ProtectedRoute from "./components/auth/ProtectedRoute";
import LandingPage from "./pages/LandingPage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import InterviewCreatePage from "./pages/InterviewCreatePage";
import InterviewPlanPage from "./pages/InterviewPlanPage";
import CandidateLandingPage from './pages/CandidateLandingPage';
import CandidateFormPage from './pages/CandidateFormPage';
import CandidateInstructionsPage from './pages/CandidateInstructionsPage';
import CandidatePermissionsPage from './pages/CandidatePermissionsPage';
import NotFoundPage from "./pages/NotFoundPage";

// We will add remaining routes as we build each page

function App() {
  return (
    <AnimatedBackground>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/interview/create"
          element={
            <ProtectedRoute>
              <InterviewCreatePage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/interview/plan"
          element={
            <ProtectedRoute>
              <InterviewPlanPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/candidate/:interviewId"
          element={<CandidateLandingPage />}
        />
        <Route
          path="/candidate/:interviewId/form"
          element={<CandidateFormPage />}
        />
        <Route
          path="/candidate/:interviewId/instructions"
          element={<CandidateInstructionsPage />}
        />
        <Route
          path="/candidate/:interviewId/permissions"
          element={<CandidatePermissionsPage />}
        />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </AnimatedBackground>
  );
}

export default App;
