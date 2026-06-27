function InstructionCard(props) {
  const icon = props.icon;
  const title = props.title;
  const description = props.description;
  const accent = props.accent || '#2DD4BF';

  return (
    <div
      style={{
        display: 'flex',
        gap: '1rem',
        padding: '1.25rem',
        background: 'rgba(17, 24, 39, 0.5)',
        border: '1px solid rgba(255,255,255,0.07)',
        borderRadius: '0.875rem',
        alignItems: 'flex-start',
      }}
    >
      <div
        style={{
          width: 42,
          height: 42,
          borderRadius: '0.625rem',
          background: accent + '1A',
          border: '1px solid ' + accent + '33',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.1rem',
          flexShrink: 0,
        }}
      >
        {icon}
      </div>
      <div>
        <h3
          style={{
            color: '#F9FAFB',
            fontWeight: 600,
            fontSize: '0.95rem',
            marginBottom: '0.375rem',
          }}
        >
          {title}
        </h3>
        <p style={{ color: '#6B7280', fontSize: '0.85rem', lineHeight: 1.65 }}>
          {description}
        </p>
      </div>
    </div>
  );
}

export default InstructionCard;
