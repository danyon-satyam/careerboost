import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { fadeInUp, staggerContainer, staggerItem } from '../animations/variants.js';
import { transitionDefault, transitionSlow } from '../animations/transitions.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';
import interviewService from '../services/interviewService.js';

const PARSE_STEPS = [
  { id: 1, label: 'Reading job description...', icon: '📄' },
  { id: 2, label: 'Identifying required skills...', icon: '🔍' },
  { id: 3, label: 'Analysing experience requirements...', icon: '📊' },
  { id: 4, label: 'Drafting interview plan...', icon: '🧠' },
];

function ParsingStep(props) {
  const step = props.step;
  const active = props.active;
  const done = props.done;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionDefault}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '1rem',
        padding: '0.875rem 1.25rem',
        borderRadius: '0.75rem',
        background: done
          ? 'rgba(45, 212, 191, 0.08)'
          : active
          ? 'rgba(255,255,255,0.05)'
          : 'transparent',
        border: done
          ? '1px solid rgba(45, 212, 191, 0.2)'
          : active
          ? '1px solid rgba(255,255,255,0.08)'
          : '1px solid transparent',
        transition: 'all 300ms ease',
      }}
    >
      <div
        style={{
          width: 36,
          height: 36,
          borderRadius: '50%',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1rem',
          background: done
            ? 'rgba(45,212,191,0.15)'
            : active
            ? 'rgba(255,255,255,0.08)'
            : 'transparent',
          flexShrink: 0,
        }}
      >
        {done ? '✓' : active ? (
          <div
            style={{
              width: 14,
              height: 14,
              border: '2px solid rgba(45,212,191,0.3)',
              borderTopColor: '#2DD4BF',
              borderRadius: '50%',
              animation: 'spin 0.7s linear infinite',
            }}
          />
        ) : step.icon}
      </div>
      <span
        style={{
          color: done ? '#2DD4BF' : active ? '#F9FAFB' : '#4B5563',
          fontSize: '0.9rem',
          fontWeight: done || active ? 500 : 400,
          transition: 'color 300ms ease',
        }}
      >
        {step.label}
      </span>
    </motion.div>
  );
}

function InterviewCreatePage() {
  const navigate = useNavigate();

  const [phase, setPhase] = useState('input');
  const [jdText, setJdText] = useState('');
  const [title, setTitle] = useState('');
  const [company, setCompany] = useState('');
  const [error, setError] = useState('');
  const [activeStep, setActiveStep] = useState(0);
  const [doneSteps, setDoneSteps] = useState([]);

  const charCount = jdText.length;
  const isValid = charCount >= 50;

  async function runParsingAnimation() {
    setPhase('parsing');
    setActiveStep(0);
    setDoneSteps([]);

    for (let i = 0; i < PARSE_STEPS.length; i++) {
      setActiveStep(i);
      await new Promise((r) => setTimeout(r, 700));
      setDoneSteps((prev) => [...prev, i]);
    }
  }

  async function handleSubmit() {
    if (!isValid) {
      setError('Please paste a job description (minimum 50 characters).');
      return;
    }
    setError('');

    await runParsingAnimation();

    try {
      const result = await interviewService.parseJD(
        jdText,
        title || undefined,
        company || undefined
      );
      navigate('/interview/plan', { state: { plan: result } });
    } catch (err) {
      const detail =
        err.response && err.response.data ? err.response.data.detail : null;
      setError(detail || 'Failed to parse job description. Please try again.');
      setPhase('input');
    }
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '5rem 1.5rem 3rem',
        position: 'relative',
      }}
    >
      <CrossGridBackground opacity={0.08} />

      <div
        style={{
          position: 'fixed',
          top: '20%',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 700,
          height: 700,
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(45,212,191,0.07) 0%, transparent 70%)',
          pointerEvents: 'none',
        }}
      />

      <div
        style={{
          position: 'relative',
          zIndex: 10,
          width: '100%',
          maxWidth: 720,
        }}
      >
        <AnimatePresence mode="wait">
          {phase === 'input' && (
            <motion.div
              key="input"
              initial="hidden"
              animate="visible"
              exit={{ opacity: 0, y: -20 }}
              variants={fadeInUp}
              transition={transitionSlow}
            >
              {/* Header */}
              <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
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
                    marginBottom: '1.5rem',
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
                    }}
                  />
                  AI-powered interview builder
                </div>
                <h1
                  style={{
                    fontSize: 'clamp(1.75rem, 4vw, 2.75rem)',
                    fontWeight: 800,
                    color: '#F9FAFB',
                    marginBottom: '0.75rem',
                    lineHeight: 1.2,
                  }}
                >
                  Create your{' '}
                  <span
                    style={{
                      background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                      WebkitBackgroundClip: 'text',
                      WebkitTextFillColor: 'transparent',
                      backgroundClip: 'text',
                    }}
                  >
                    AI interviewer
                  </span>
                </h1>
                <p style={{ color: '#6B7280', fontSize: '1rem', lineHeight: 1.65 }}>
                  Paste a job description and our AI will generate a tailored
                  interview plan with real questions.
                </p>
              </div>

              {/* Optional fields row */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '1rem',
                  marginBottom: '1rem',
                }}
              >
                <div>
                  <label
                    style={{
                      display: 'block',
                      fontSize: '0.8rem',
                      color: '#9CA3AF',
                      marginBottom: '0.375rem',
                      fontWeight: 500,
                    }}
                  >
                    Job title (optional)
                  </label>
                  <input
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Senior Backend Engineer"
                    style={{
                      width: '100%',
                      padding: '0.625rem 0.875rem',
                      background: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      borderRadius: '0.625rem',
                      color: '#F9FAFB',
                      fontSize: '0.875rem',
                      outline: 'none',
                      boxSizing: 'border-box',
                      transition: 'border-color 200ms ease',
                    }}
                    onFocus={(e) =>
                      (e.target.style.borderColor = 'rgba(45,212,191,0.4)')
                    }
                    onBlur={(e) =>
                      (e.target.style.borderColor = 'rgba(255,255,255,0.08)')
                    }
                  />
                </div>
                <div>
                  <label
                    style={{
                      display: 'block',
                      fontSize: '0.8rem',
                      color: '#9CA3AF',
                      marginBottom: '0.375rem',
                      fontWeight: 500,
                    }}
                  >
                    Company (optional)
                  </label>
                  <input
                    type="text"
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    placeholder="e.g. Acme Corp"
                    style={{
                      width: '100%',
                      padding: '0.625rem 0.875rem',
                      background: 'rgba(255,255,255,0.04)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      borderRadius: '0.625rem',
                      color: '#F9FAFB',
                      fontSize: '0.875rem',
                      outline: 'none',
                      boxSizing: 'border-box',
                      transition: 'border-color 200ms ease',
                    }}
                    onFocus={(e) =>
                      (e.target.style.borderColor = 'rgba(45,212,191,0.4)')
                    }
                    onBlur={(e) =>
                      (e.target.style.borderColor = 'rgba(255,255,255,0.08)')
                    }
                  />
                </div>
              </div>

              {/* JD textarea */}
              <div style={{ marginBottom: '1.25rem' }}>
                <label
                  style={{
                    display: 'block',
                    fontSize: '0.8rem',
                    color: '#9CA3AF',
                    marginBottom: '0.375rem',
                    fontWeight: 500,
                  }}
                >
                  Job description
                  <span style={{ color: '#F87171', marginLeft: '0.25rem' }}>*</span>
                </label>
                <textarea
                  value={jdText}
                  onChange={(e) => {
                    setJdText(e.target.value);
                    if (error) setError('');
                  }}
                  placeholder="Paste the full job description here...&#10;&#10;Our AI will extract skills, experience requirements, and role details to build a personalised interview tailored to this specific position."
                  rows={12}
                  style={{
                    width: '100%',
                    padding: '1rem',
                    background: 'rgba(17, 24, 39, 0.6)',
                    backdropFilter: 'blur(12px)',
                    WebkitBackdropFilter: 'blur(12px)',
                    border: error
                      ? '1px solid rgba(248,113,113,0.4)'
                      : '1px solid rgba(255,255,255,0.08)',
                    borderRadius: '0.875rem',
                    color: '#F9FAFB',
                    fontSize: '0.9rem',
                    outline: 'none',
                    resize: 'vertical',
                    lineHeight: 1.65,
                    boxSizing: 'border-box',
                    fontFamily: 'inherit',
                    transition: 'border-color 200ms ease',
                  }}
                  onFocus={(e) => {
                    e.target.style.borderColor = error
                      ? 'rgba(248,113,113,0.6)'
                      : 'rgba(45,212,191,0.35)';
                  }}
                  onBlur={(e) => {
                    e.target.style.borderColor = error
                      ? 'rgba(248,113,113,0.4)'
                      : 'rgba(255,255,255,0.08)';
                  }}
                />
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    marginTop: '0.375rem',
                  }}
                >
                  {error ? (
                    <p style={{ color: '#FCA5A5', fontSize: '0.8rem' }}>
                      {error}
                    </p>
                  ) : (
                    <span />
                  )}
                  <span
                    style={{
                      color: isValid ? '#34D399' : '#6B7280',
                      fontSize: '0.75rem',
                      transition: 'color 200ms ease',
                    }}
                  >
                    {charCount} chars {isValid ? '✓' : '(min 50)'}
                  </span>
                </div>
              </div>

              {/* Submit */}
              <button
                onClick={handleSubmit}
                disabled={!isValid}
                style={{
                  width: '100%',
                  padding: '1rem',
                  background: isValid
                    ? 'linear-gradient(135deg, #2DD4BF, #06B6D4)'
                    : 'rgba(255,255,255,0.06)',
                  color: isValid ? '#0A0E14' : '#4B5563',
                  border: 'none',
                  borderRadius: '0.75rem',
                  fontWeight: 700,
                  fontSize: '1rem',
                  cursor: isValid ? 'pointer' : 'not-allowed',
                  transition: 'all 200ms ease',
                  boxShadow: isValid
                    ? '0 0 24px rgba(45,212,191,0.28)'
                    : 'none',
                  fontFamily: 'inherit',
                }}
                onMouseEnter={(e) => {
                  if (isValid) e.currentTarget.style.opacity = '0.88';
                }}
                onMouseLeave={(e) => {
                  if (isValid) e.currentTarget.style.opacity = '1';
                }}
              >
                Generate interview plan →
              </button>
            </motion.div>
          )}

          {phase === 'parsing' && (
            <motion.div
              key="parsing"
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={transitionDefault}
              style={{ textAlign: 'center' }}
            >
              <div style={{ marginBottom: '2.5rem' }}>
                <div
                  style={{
                    width: 64,
                    height: 64,
                    borderRadius: '1rem',
                    background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '1.75rem',
                    margin: '0 auto 1.5rem',
                    boxShadow: '0 0 40px rgba(45,212,191,0.4)',
                    animation: 'pulseGlow 2s ease-in-out infinite',
                  }}
                >
                  🧠
                </div>
                <h2
                  style={{
                    fontSize: '1.5rem',
                    fontWeight: 700,
                    color: '#F9FAFB',
                    marginBottom: '0.5rem',
                  }}
                >
                  Building your interview
                </h2>
                <p style={{ color: '#6B7280', fontSize: '0.9rem' }}>
                  This takes a few seconds...
                </p>
              </div>

              <div
                style={{
                  background: 'rgba(17, 24, 39, 0.6)',
                  backdropFilter: 'blur(12px)',
                  WebkitBackdropFilter: 'blur(12px)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: '1rem',
                  padding: '1.5rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.5rem',
                  textAlign: 'left',
                }}
              >
                <motion.div
                  variants={staggerContainer}
                  initial="hidden"
                  animate="visible"
                >
                  {PARSE_STEPS.map((step, i) => (
                    <ParsingStep
                      key={step.id}
                      step={step}
                      active={activeStep === i}
                      done={doneSteps.includes(i)}
                    />
                  ))}
                </motion.div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes pulseGlow {
          0%, 100% { box-shadow: 0 0 40px rgba(45,212,191,0.4); }
          50% { box-shadow: 0 0 60px rgba(45,212,191,0.6); }
        }
        textarea::placeholder { color: #4B5563; }
        input::placeholder { color: #4B5563; }
      `}</style>
    </div>
  );
}

export default InterviewCreatePage;
