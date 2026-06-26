import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { fadeInUp, staggerContainer, staggerItem } from '../animations/variants.js';
import { transitionDefault, transitionSlow } from '../animations/transitions.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';

const SECTION_ICONS = {
  technical: '⚙️',
  behavioral: '🧠',
  general: '💬',
  situational: '🎯',
  default: '📋',
};

const SUGGESTED_EDITS = [
  'Focus more on system design',
  'Add leadership questions',
  'Include coding exercises',
  'More behavioural questions',
  'Focus on culture fit',
  'Add salary negotiation prep',
];

function SectionCard(props) {
  const section = props.section;
  const questions = props.questions;
  const [open, setOpen] = useState(false);

  const sectionQuestions = questions.filter(
    (q) => q.category === section
  );

  const icon = SECTION_ICONS[section] || SECTION_ICONS.default;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionDefault}
      style={{
        background: 'rgba(17, 24, 39, 0.6)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        border: '1px solid rgba(255,255,255,0.08)',
        borderRadius: '1rem',
        overflow: 'hidden',
        transition: 'border-color 200ms ease',
      }}
    >
      <button
        onClick={() => setOpen(!open)}
        style={{
          width: '100%',
          padding: '1.25rem 1.5rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          fontFamily: 'inherit',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem' }}>
          <div
            style={{
              width: 38,
              height: 38,
              borderRadius: '0.625rem',
              background: 'rgba(45,212,191,0.1)',
              border: '1px solid rgba(45,212,191,0.2)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1rem',
            }}
          >
            {icon}
          </div>
          <div style={{ textAlign: 'left' }}>
            <p
              style={{
                color: '#F9FAFB',
                fontWeight: 600,
                fontSize: '0.95rem',
                textTransform: 'capitalize',
              }}
            >
              {section} questions
            </p>
            <p style={{ color: '#6B7280', fontSize: '0.775rem' }}>
              {sectionQuestions.length} question
              {sectionQuestions.length !== 1 ? 's' : ''}
            </p>
          </div>
        </div>
        <span
          style={{
            color: '#6B7280',
            fontSize: '0.8rem',
            transition: 'transform 200ms ease',
            transform: open ? 'rotate(180deg)' : 'rotate(0deg)',
            display: 'inline-block',
          }}
        >
          ▼
        </span>
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: 'easeInOut' }}
            style={{ overflow: 'hidden' }}
          >
            <div
              style={{
                padding: '0 1.5rem 1.25rem',
                borderTop: '1px solid rgba(255,255,255,0.05)',
              }}
            >
              {sectionQuestions.length === 0 ? (
                <p
                  style={{
                    color: '#6B7280',
                    fontSize: '0.875rem',
                    padding: '1rem 0',
                  }}
                >
                  No questions in this category.
                </p>
              ) : (
                <ol style={{ paddingLeft: '1.25rem', margin: '1rem 0 0' }}>
                  {sectionQuestions.map((q, i) => (
                    <li
                      key={q.id || i}
                      style={{
                        color: '#D1D5DB',
                        fontSize: '0.875rem',
                        lineHeight: 1.65,
                        marginBottom: '0.625rem',
                      }}
                    >
                      {q.question_text}
                    </li>
                  ))}
                </ol>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

function InterviewPlanPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const plan = location.state && location.state.plan ? location.state.plan : null;

  if (!plan) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#6B7280',
          gap: '1rem',
        }}
      >
        <p style={{ fontSize: '1.1rem' }}>No interview plan found.</p>
        <button
          onClick={() => navigate('/interview/create')}
          style={{
            padding: '0.75rem 1.5rem',
            background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
            color: '#0A0E14',
            border: 'none',
            borderRadius: '0.625rem',
            fontWeight: 600,
            fontSize: '0.9rem',
            cursor: 'pointer',
            fontFamily: 'inherit',
          }}
        >
          Create an interview
        </button>
      </div>
    );
  }

  const sections = plan.sections && plan.sections.length > 0
    ? plan.sections
    : ['general'];

  return (
    <div
      style={{
        minHeight: '100vh',
        padding: '5rem 1.5rem 4rem',
        position: 'relative',
      }}
    >
      <CrossGridBackground opacity={0.06} />

      <div style={{ maxWidth: 800, margin: '0 auto', position: 'relative', zIndex: 10 }}>
        {/* Header */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeInUp}
          transition={transitionSlow}
          style={{ marginBottom: '2.5rem' }}
        >
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem',
              marginBottom: '1.5rem',
            }}
          >
            <button
              onClick={() => navigate('/interview/create')}
              style={{
                background: 'rgba(255,255,255,0.05)',
                border: '1px solid rgba(255,255,255,0.08)',
                borderRadius: '0.5rem',
                padding: '0.4rem 0.875rem',
                color: '#9CA3AF',
                fontSize: '0.8rem',
                cursor: 'pointer',
                fontFamily: 'inherit',
                transition: 'all 200ms ease',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = '#F9FAFB')}
              onMouseLeave={(e) => (e.currentTarget.style.color = '#9CA3AF')}
            >
              ← Back
            </button>
            <span style={{ color: '#4B5563', fontSize: '0.8rem' }}>
              Interview plan
            </span>
          </div>

          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(45, 212, 191, 0.08)',
              border: '1px solid rgba(45, 212, 191, 0.2)',
              borderRadius: '9999px',
              padding: '0.35rem 1rem',
              fontSize: '0.78rem',
              color: '#2DD4BF',
              marginBottom: '1rem',
              fontWeight: 500,
            }}
          >
            <span
              style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: '#2DD4BF',
                display: 'inline-block',
                animation: 'pulse 2s ease-in-out infinite',
              }}
            />
            Plan ready
          </div>

          <h1
            style={{
              fontSize: 'clamp(1.5rem, 3.5vw, 2.25rem)',
              fontWeight: 800,
              color: '#F9FAFB',
              marginBottom: '0.5rem',
              lineHeight: 1.2,
            }}
          >
            {plan.title}
          </h1>
          {plan.company && plan.company !== 'Tech Company' && (
            <p style={{ color: '#9CA3AF', fontSize: '1rem', marginBottom: '1.25rem' }}>
              {plan.company}
            </p>
          )}

          {/* Meta row */}
          <div style={{ display: 'flex', gap: '1.25rem', flexWrap: 'wrap' }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.375rem',
                fontSize: '0.825rem',
                color: '#6B7280',
              }}
            >
              <span>📋</span>
              <span>{plan.total_questions} questions</span>
            </div>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.375rem',
                fontSize: '0.825rem',
                color: '#6B7280',
              }}
            >
              <span>⏱</span>
              <span>
                ~{Math.ceil((plan.total_questions * 3) / 5) * 5} min
              </span>
            </div>
            {plan.required_experience > 0 && (
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.375rem',
                  fontSize: '0.825rem',
                  color: '#6B7280',
                }}
              >
                <span>📅</span>
                <span>{plan.required_experience}+ yrs experience</span>
              </div>
            )}
          </div>
        </motion.div>

        {/* Extracted skills */}
        {plan.extracted_skills && plan.extracted_skills.length > 0 && (
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeInUp}
            transition={{ ...transitionDefault, delay: 0.1 }}
            style={{
              marginBottom: '2rem',
              padding: '1.25rem 1.5rem',
              background: 'rgba(17, 24, 39, 0.6)',
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '1rem',
            }}
          >
            <p
              style={{
                color: '#9CA3AF',
                fontSize: '0.8rem',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                marginBottom: '0.875rem',
              }}
            >
              Extracted skills
            </p>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
              {plan.extracted_skills.map((skill) => (
                <span
                  key={skill}
                  style={{
                    padding: '0.3rem 0.75rem',
                    background: 'rgba(45,212,191,0.08)',
                    border: '1px solid rgba(45,212,191,0.18)',
                    borderRadius: '9999px',
                    color: '#2DD4BF',
                    fontSize: '0.8rem',
                    fontWeight: 500,
                  }}
                >
                  {skill}
                </span>
              ))}
            </div>
          </motion.div>
        )}

        {/* Section cards */}
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          style={{ display: 'flex', flexDirection: 'column', gap: '0.875rem', marginBottom: '2rem' }}
        >
          {sections.map((section) => (
            <SectionCard
              key={section}
              section={section}
              questions={plan.questions || []}
            />
          ))}
        </motion.div>

        {/* Suggested edit chips */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeInUp}
          transition={{ ...transitionDefault, delay: 0.3 }}
          style={{ marginBottom: '2rem' }}
        >
          <p
            style={{
              color: '#9CA3AF',
              fontSize: '0.8rem',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.08em',
              marginBottom: '0.875rem',
            }}
          >
            Suggested adjustments
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {SUGGESTED_EDITS.map((edit) => (
              <button
                key={edit}
                style={{
                  padding: '0.4rem 0.875rem',
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '9999px',
                  color: '#9CA3AF',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  fontFamily: 'inherit',
                  transition: 'all 200ms ease',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'rgba(45,212,191,0.3)';
                  e.currentTarget.style.color = '#2DD4BF';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)';
                  e.currentTarget.style.color = '#9CA3AF';
                }}
              >
                + {edit}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Start interview CTA */}
        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeInUp}
          transition={{ ...transitionDefault, delay: 0.4 }}
          style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}
        >
          <button
            onClick={() =>
              navigate('/candidate/' + plan.interview_id)
            }
            style={{
              flex: 1,
              padding: '1rem',
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              color: '#0A0E14',
              border: 'none',
              borderRadius: '0.75rem',
              fontWeight: 700,
              fontSize: '1rem',
              cursor: 'pointer',
              fontFamily: 'inherit',
              boxShadow: '0 0 24px rgba(45,212,191,0.28)',
              transition: 'all 200ms ease',
              minWidth: 200,
            }}
            onMouseEnter={(e) => (e.currentTarget.style.opacity = '0.88')}
            onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
          >
            Start interview →
          </button>
          <button
            onClick={() => navigate('/interview/create')}
            style={{
              padding: '1rem 1.5rem',
              background: 'rgba(255,255,255,0.04)',
              color: '#9CA3AF',
              border: '1px solid rgba(255,255,255,0.08)',
              borderRadius: '0.75rem',
              fontWeight: 500,
              fontSize: '0.95rem',
              cursor: 'pointer',
              fontFamily: 'inherit',
              transition: 'all 200ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#F9FAFB';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#9CA3AF';
              e.currentTarget.style.borderColor = 'rgba(255,255,255,0.08)';
            }}
          >
            Start over
          </button>
        </motion.div>
      </div>

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.4; }
        }
      `}</style>
    </div>
  );
}

export default InterviewPlanPage;
