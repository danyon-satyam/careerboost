import { useState, useEffect, useRef } from 'react';

/**
 * useAnimatedBackground — manages video playback state,
 * pausing the background video when the tab is hidden
 * to save resources.
 */
export function useAnimatedBackground() {
  const videoRef = useRef(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    function handleVisibilityChange() {
      const video = videoRef.current;
      if (!video) return;

      if (document.hidden) {
        video.pause();
      } else if (!hasError) {
        video.play().catch(() => setHasError(true));
      }
    }

    document.addEventListener('visibilitychange', handleVisibilityChange);
    return () =>
      document.removeEventListener(
        'visibilitychange',
        handleVisibilityChange
      );
  }, [hasError]);

  const handleLoadedData = () => {
    setIsPlaying(true);
  };

  const handleError = () => {
    setHasError(true);
    setIsPlaying(false);
  };

  return {
    videoRef,
    isPlaying,
    hasError,
    handleLoadedData,
    handleError,
  };
}

export default useAnimatedBackground;
