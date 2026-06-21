import { useSelector } from 'react-redux';

export function useAuth() {
  const auth = useSelector(function (state) {
    return state.auth;
  });

  return {
    user: auth.user,
    token: auth.token,
    isAuthenticated: auth.isAuthenticated,
    isLoading: auth.isLoading,
    error: auth.error,
  };
}

export default useAuth;
