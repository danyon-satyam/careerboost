import { motion } from 'framer-motion';
import { staggerContainer, staggerItem } from '../../animations/variants.js';
import { transitionFast } from '../../animations/transitions.js';

function ActivityRow(props) {
  const icon = props.icon;
  const title = props.title;
  const subtitle = props.subtitle;
  const value = props.value;
  const accent = props.accent;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionFast}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.875rem 0',
        borderBottom: '1px solid rgba(255,255,255,0.05)',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
        <div
          style={{
            width: 32,
            height: 32,
            borderRadius: '0.5rem',
            background: accent + '1A',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '0.95rem',
            flexShrink: 0,
          }}
        >
          {icon}
        </div>
        <div>
          <p style={{ color: '#F9FAFB', fontSize: '0.875rem', fontWeight: 500 }}>{title}</p>
          <p style={{ color: '#6B7280', fontSize: '0.75rem' }}>{subtitle}</p>
        </div>
      </div>
      <div style={{ color: accent, fontWeight: 600, fontSize: '0.875rem' }}>{value}</div>
    </motion.div>
  );
}

function RecentActivity(props) {
  const interviewTrend = props.interviewTrend || [];
  const typingTrend = props.typingTrend || [];

  const interviewItems = interviewTrend
    .slice(-3)
    .reverse()
    .map(function (item) {
      return {
        icon: '🎤',
        title: 'Interview completed',
        subtitle: new Date(item.date).toLocaleDateString(),
        value: item.score + '%',
        accent: '#2DD4BF',
      };
    });

  const typingItems = typingTrend
    .slice(-3)
    .reverse()
    .map(function (item) {
      return {
        icon: '⌨️',
        title: 'Typing session',
        subtitle: new Date(item.date).toLocaleDateString(),
        value: item.wpm + ' WPM',
        accent: '#34D399',
      };
    });

  const combined = interviewItems.concat(typingItems).slice(0, 6);

  if (combined.length === 0) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center', color: '#6B7280', fontSize: '0.875rem' }}>
        No activity yet. Start an interview or typing test to see it here.
      </div>
    );
  }

  return (
    <motion.div variants={staggerContainer} initial="hidden" animate="visible">
      {combined.map(function (item, i) {
        return (
          <ActivityRow
            key={i}
            icon={item.icon}
            title={item.title}
            subtitle={item.subtitle}
            value={item.value}
            accent={item.accent}
          />
        );
      })}
    </motion.div>
  );
}

export default RecentActivity;
