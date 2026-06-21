import { motion } from 'framer-motion';
import { staggerContainer, staggerItem } from '../../animations/variants.js';
import { transitionDefault } from '../../animations/transitions.js';

function StatBox(props) {
  const icon = props.icon;
  const label = props.label;
  const value = props.value;
  const accent = props.accent;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionDefault}
      style={{
        flex: '1 1 200px',
        padding: '1.5rem',
        background: 'rgba(17, 24, 39, 0.6)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '1rem',
      }}
    >
      <div
        style={{
          width: 40,
          height: 40,
          borderRadius: '0.625rem',
          background: accent + '1A',
          border: '1px solid ' + accent + '33',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.1rem',
          marginBottom: '0.875rem',
        }}
      >
        {icon}
      </div>
      <div
        style={{
          fontSize: '1.75rem',
          fontWeight: 800,
          color: '#F9FAFB',
          lineHeight: 1,
          marginBottom: '0.375rem',
        }}
      >
        {value}
      </div>
      <div style={{ color: '#6B7280', fontSize: '0.825rem' }}>{label}</div>
    </motion.div>
  );
}

function StatsGrid(props) {
  const data = props.data || {};
  const interviews = data.interviews || {};
  const typing = data.typing || {};
  const readiness = data.overall_readiness_score != null ? data.overall_readiness_score : 0;

  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}
    >
      <StatBox icon="🎯" label="Readiness score" value={readiness + '%'} accent="#2DD4BF" />
      <StatBox
        icon="🎤"
        label="Interviews completed"
        value={interviews.completed != null ? interviews.completed : 0}
        accent="#06B6D4"
      />
      <StatBox
        icon="⌨️"
        label="Avg WPM"
        value={typing.average_wpm != null ? typing.average_wpm : 0}
        accent="#34D399"
      />
      <StatBox
        icon="📈"
        label="Avg interview score"
        value={(interviews.average_score != null ? interviews.average_score : 0) + '%'}
        accent="#FBBF24"
      />
    </motion.div>
  );
}

export default StatsGrid;
