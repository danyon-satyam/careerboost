import { motion } from 'framer-motion';
import { fadeIn } from '../../animations/variants.js';
import { transitionSlow } from '../../animations/transitions.js';

function ProgressChart(props) {
  const trend = props.trend;
  const label = props.label;
  const color = props.color || '#2DD4BF';

  if (!trend || trend.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#6B7280', fontSize: '0.875rem' }}>
        No data yet — complete a few sessions to see your trend.
      </div>
    );
  }

  const values = trend.map(function (t) {
    return t.score != null ? t.score : (t.wpm != null ? t.wpm : 0);
  });
  const max = Math.max.apply(null, values.concat([1]));
  const min = Math.min.apply(null, values.concat([0]));
  const range = max - min || 1;

  const width = 100;
  const height = 100;
  const padding = 8;

  const points = values.map(function (v, i) {
    const x =
      values.length === 1
        ? width / 2
        : padding + (i / (values.length - 1)) * (width - padding * 2);
    const y = height - padding - ((v - min) / range) * (height - padding * 2);
    return x + ',' + y;
  });

  const polylinePoints = points.join(' ');

  return (
    <motion.div initial="hidden" animate="visible" variants={fadeIn} transition={transitionSlow}>
      <p style={{ color: '#6B7280', fontSize: '0.8rem', marginBottom: '1rem' }}>{label}</p>
      <svg viewBox={'0 0 ' + width + ' ' + height} style={{ width: '100%', height: 140 }} preserveAspectRatio="none">
        <polyline
          points={polylinePoints}
          fill="none"
          stroke={color}
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {points.map(function (p, i) {
          const parts = p.split(',');
          const x = parts[0];
          const y = parts[1];
          return <circle key={i} cx={x} cy={y} r="1.8" fill={color} />;
        })}
      </svg>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          color: '#4B5563',
          fontSize: '0.75rem',
          marginTop: '0.5rem',
        }}
      >
        <span>{values.length} sessions</span>
        <span>Latest: {values[values.length - 1]}</span>
      </div>
    </motion.div>
  );
}

export default ProgressChart;
