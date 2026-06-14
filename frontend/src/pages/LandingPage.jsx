import CrossGridBackground from '../components/layout/CrossGridBackground';

function LandingPage() {
  return (
    <div style={{ position: 'relative', minHeight: '100vh' }}>
      <CrossGridBackground />
      <div
        style={{
          position: 'relative',
          zIndex: 10,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          flexDirection: 'column',
          gap: '1rem',
        }}
      >
        <h1
          style={{
            fontSize: '3rem',
            fontWeight: 700,
            color: '#F9FAFB',
          }}
        >
          Career
          <span className="gradient-text">Boost</span>
        </h1>
        <p style={{ color: '#9CA3AF', fontSize: '1.125rem' }}>
          AI-powered interview prep platform
        </p>
        <div className="section-divider" style={{ width: '200px' }} />
        <p style={{ color: '#6B7280', fontSize: '0.875rem' }}>
          Frontend Day 19 — Foundation complete
        </p>
      </div>
    </div>
  );
}

export default LandingPage;
