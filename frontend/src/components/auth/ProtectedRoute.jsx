import { Navigate, useLocation } from 'react-router-dom';

/**
 * ProtectedRoute — redirects unauthenticated users to /login.
 * Checks for access_token in localStorage.
 */
function ProtectedRoute({ children }) {
  const location = useLocation();
  const token = localStorage.getItem('access_token');

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}

export default ProtectedRoute;
