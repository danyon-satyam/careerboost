function StepProgressDots(props) {
  const total = props.total || 3;
  const current = props.current || 0;

  return (
    <div
      style={{
        display: 'flex',
        gap: '0.5rem',
        justifyContent: 'center',
        alignItems: 'center',
      }}
    >
      {Array.from({ length: total }).map(function (_, i) {
        const done = i < current;
        const active = i === current;
        return (
          <div
            key={i}
            style={{
              width: active ? 24 : done ? 8 : 8,
              height: 8,
              borderRadius: '999px',
              background: active
                ? 'linear-gradient(135deg, #2DD4BF, #06B6D4)'
                : done
                ? '#2DD4BF'
                : 'rgba(255,255,255,0.15)',
              transition: 'all 300ms ease',
            }}
          />
        );
      })}
    </div>
  );
}

export default StepProgressDots;
