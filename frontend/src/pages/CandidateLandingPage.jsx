import { useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer, staggerItem } from '../animations/variants.js';
import { transitionDefault, transitionSlow } from '../animations/transitions.js';
import { setInterviewContext } from '../store/slices/candidateSlice.js';
import interviewService from '../services/interviewService.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';
import StepProgressDots from '../components/candidate/StepProgressDots.jsx';
import { useState } from 'react';

const HIGHLIGHTS = [
  { icon: '🎤', text: 'Speak your answers naturally' },
  { icon: '🧠', text: 'AI evaluates in real time' },
  { icon: '📊', text: 'Get a detailed report after' },
];

function CandidateLandingPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();

  const [interview, setInterview] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(function () {
    async function load() {
      try {
        const data = await interviewService.getInterview(
          parseInt(interviewId)
        );
        setInterview(data);
        dispatch(
          setInterviewContext({
            interviewId: data.id,
            jobTitle: data.job ? data.job.title : 'Interview',
            company: data.job ? data.job.company : '',
            totalQuestions: data.questions
              ? data.questions.length
              : 0,
          })
        );
      } catch {
        setError('Interview not found or no longer available.');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [interviewId, dispatch]);

  if (loading) {
    return (
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          color: '#6B7280',
        }}
      >
        <div style={{ textAlign: 'center' }}>
          <div
            style={{
              width: 32,
              height: 32,
              border: '3px solid rgba(45,212,191,0.2)',
              borderTopColor: '#2DD4BF',
              borderRadius: '50%',
              margin: '0 auto 1rem',
              animation: 'spin 0.8s linear infinite',
            }}
          />
          Loading interview...
          <style>
            {'@keyframes spin { to { transform: rotate(360deg); } }'}
          </style>
        </div>
      </div>
    );
  }

  if (error) {
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
        <p style={{ fontSize: '1.1rem', color: '#FCA5A5' }}>{error}</p>
      </div>
    );
  }

  const jobTitle = interview && interview.job
    ? interview.job.title
    : 'Interview';
  const company = interview && interview.job
    ? interview.job.company
    : '';
  const totalQuestions = interview && interview.questions
    ? interview.questions.length
    : 0;

  return (
    <div
      style={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3rem 1.5rem',
        position: 'relative',
        textAlign: 'center',
      }}
    >
      <CrossGridBackground opacity={0.07} />

      <div
        style={{
          position: 'fixed',
          top: '20%',
          left: '50%',
          transform: 'translateX(-50%)',
          width: 600,
          height: 600,
          borderRadius: '50%',
          background:
            'radial-gradient(circle, rgba(45,212,191,0.08) 0%, transparent 70%)',
          pointerEvents: 'none',
        }}
      />

      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        transition={transitionSlow}
        style={{
          position: 'relative',
          zIndex: 10,
          maxWidth: 560,
          width: '100%',
        }}
      >
        {/* CB Logo */}
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          style={{
            width: 72,
            height: 72,
            borderRadius: '1.25rem',
            background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.75rem',
            fontWeight: 800,
            color: '#0A0E14',
            margin: '0 auto 2rem',
            boxShadow: '0 0 40px rgba(45,212,191,0.35)',
          }}
        >
          CB
        </motion.div>

        <p
          style={{
            color: '#9CA3AF',
            fontSize: '0.85rem',
            fontWeight: 500,
            marginBottom: '0.75rem',
            letterSpacing: '0.04em',
          }}
        >
          AI MOCK INTERVIEW
        </p>

        <h1
          style={{
            fontSize: 'clamp(1.75rem, 4vw, 2.5rem)',
            fontWeight: 800,
            color: '#F9FAFB',
            lineHeight: 1.2,
            marginBottom: '0.625rem',
          }}
        >
          Hi, welcome to your
          <br />
          <span
            style={{
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            {jobTitle.toLowerCase().includes('interview')
              ? jobTitle
              : jobTitle + ' interview'}
          </span>
        </h1>

        {company && (
          <p
            style={{
              color: '#6B7280',
              fontSize: '0.95rem',
              marginBottom: '0.5rem',
            }}
          >
            {company}
          </p>
        )}

        <p
          style={{
            color: '#4B5563',
            fontSize: '0.875rem',
            marginBottom: '2.5rem',
          }}
        >
          {totalQuestions} questions · ~{Math.ceil(totalQuestions * 3)} min
        </p>

        {/* Highlights */}
        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem',
            marginBottom: '2.5rem',
          }}
        >
          {HIGHLIGHTS.map(function (h) {
            return (
              <motion.div
                key={h.text}
                variants={staggerItem}
                transition={transitionDefault}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.875rem',
                  padding: '0.875rem 1.25rem',
                  background: 'rgba(17, 24, 39, 0.5)',
                  border: '1px solid rgba(255,255,255,0.07)',
                  borderRadius: '0.75rem',
                  textAlign: 'left',
                }}
              >
                <span style={{ fontSize: '1.2rem' }}>{h.icon}</span>
                <span
                  style={{ color: '#D1D5DB', fontSize: '0.9rem' }}
                >
                  {h.text}
                </span>
              </motion.div>
            );
          })}
        </motion.div>

        {/* CTA */}
        <button
          onClick={function () {
            navigate('/candidate/' + interviewId + '/form');
          }}
          style={{
            width: '100%',
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
            marginBottom: '1.5rem',
          }}
          onMouseEnter={function (e) {
            e.currentTarget.style.opacity = '0.88';
          }}
          onMouseLeave={function (e) {
            e.currentTarget.style.opacity = '1';
          }}
        >
          Let's begin →
        </button>

        <StepProgressDots total={4} current={0} />
        <p
          style={{
            color: '#4B5563',
            fontSize: '0.75rem',
            marginTop: '0.75rem',
          }}
        >
          Step 1 of 4
        </p>
      </motion.div>
    </div>
  );
}

export default CandidateLandingPage;
