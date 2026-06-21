import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { staggerContainer, staggerItem, cardHover } from '../../animations/variants.js';
import { transitionDefault } from '../../animations/transitions.js';

function ActionCard(props) {
  const icon = props.icon;
  const title = props.title;
  const description = props.description;
  const to = props.to;
  const accent = props.accent;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionDefault}
      whileHover="hover"
      initial="rest"
      animate="rest"
      style={{ flex: '1 1 220px' }}
    >
      <motion.div variants={cardHover} transition={transitionDefault}>
        <Link
          to={to}
          style={{
            padding: '1.5rem',
            background: 'rgba(17, 24, 39, 0.6)',
            backdropFilter: 'blur(12px)',
            WebkitBackdropFilter: 'blur(12px)',
            border: '1px solid rgba(255, 255, 255, 0.08)',
            borderRadius: '1rem',
            textDecoration: 'none',
            display: 'block',
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
              marginBottom: '1rem',
            }}
          >
            {icon}
          </div>
          <h3
            style={{
              color: '#F9FAFB',
              fontWeight: 600,
              fontSize: '1rem',
              marginBottom: '0.375rem',
            }}
          >
            {title}
          </h3>
          <p style={{ color: '#6B7280', fontSize: '0.825rem', lineHeight: 1.6 }}>
            {description}
          </p>
        </Link>
      </motion.div>
    </motion.div>
  );
}

function QuickActions() {
  return (
    <motion.div
      variants={staggerContainer}
      initial="hidden"
      animate="visible"
      style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}
    >
      <ActionCard
        icon="🎤"
        title="Start an interview"
        description="Practice with the AI interviewer"
        to="/interview/create"
        accent="#2DD4BF"
      />
      <ActionCard
        icon="⌨️"
        title="Typing practice"
        description="Improve your WPM and accuracy"
        to="/typing"
        accent="#34D399"
      />
      <ActionCard
        icon="💼"
        title="Browse jobs"
        description="See your AI-matched opportunities"
        to="/jobs"
        accent="#06B6D4"
      />
      <ActionCard
        icon="📊"
        title="View analytics"
        description="Track your progress over time"
        to="/analytics"
        accent="#FBBF24"
      />
    </motion.div>
  );
}

export default QuickActions;
