import { useRef, useState, useEffect } from 'react';

function AnimatedBackground({ children }) {
  const [videoError, setVideoError] = useState(false);
  const videoRef = useRef(null);

  useEffect(() => {
    const video = videoRef.current;
    if (!video) return;
    video.play().catch(() => setVideoError(true));
  }, []);

  return (
    <div
      style={{ backgroundColor: '#0A0E14', minHeight: '100vh' }}
    >
      {/* Fixed background */}
      <div
        style={{
          position: 'fixed',
          inset: 0,
          zIndex: -1,
          overflow: 'hidden',
        }}
      >
        {!videoError ? (
          <video
            ref={videoRef}
            style={{
              position: 'absolute',
              inset: 0,
              width: '100%',
              height: '100%',
              objectFit: 'cover',
            }}
            autoPlay
            loop
            muted
            playsInline
            onError={() => setVideoError(true)}
          >
            <source
              src="/src/assets/videos/bg-animation.mp4"
              type="video/mp4"
            />
          </video>
        ) : (
          /* Gradient fallback */
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background:
                'radial-gradient(ellipse at 20% 20%, rgba(45,212,191,0.15) 0%, transparent 55%),' +
                'radial-gradient(ellipse at 80% 80%, rgba(6,182,212,0.1) 0%, transparent 55%),' +
                '#0A0E14',
            }}
          />
        )}

        {/* Overlay for text legibility */}
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundColor: 'rgba(10, 14, 20, 0.55)',
          }}
        />
      </div>

      {/* Content */}
      <div style={{ position: 'relative', zIndex: 10 }}>
        {children}
      </div>
    </div>
  );
}

export default AnimatedBackground;
