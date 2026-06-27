import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer } from '../animations/variants.js';
import { transitionDefault, transitionSlow } from '../animations/transitions.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';
import InstructionCard from '../components/candidate/InstructionCard.jsx';
import StepProgressDots from '../components/candidate/StepProgressDots.jsx';

const INSTRUCTIONS = [
  {
    icon: '🎤',
    title: 'Speak your answers clearly',
    description:
      'The AI uses your browser\'s speech recognition to transcribe your answers in real time. Speak at a natural pace in a quiet environment.',
    accent: '#2DD4BF',
  },
  {
    icon: '📷',
    title: 'Keep your camera on',
    description:
      'Your webcam feed is shown during the interview. Make sure your face is well lit and centred in the frame.',
    accent: '#06B6D4',
  },
  {
    icon: '🖥️',
    title: 'Stay on this tab',
    description:
      'Switching tabs or windows during the interview is logged as a potential integrity flag. Please keep this tab active throughout.',
    accent: '#FBBF24',
  },
  {
    icon: '⌨️',
    title: 'Use the whiteboard when needed',
    description:
      'For technical questions you can draw diagrams or write pseudocode on the built-in whiteboard. It\'s optional but encouraged.',
    accent: '#34D399',
  },
  {
    icon: '⏱️',
    title: 'Take your time',
    description:
      'There is no hard time limit per question. Think before you speak — quality of reasoning matters more than speed.',
    accent: '#A78BFA',
  },
  {
    icon: '🔒',
    title: 'This session is recorded',
    description:
      'Your responses are evaluated and stored to generate your performance report. The session is confidential.',
    accent: '#F87171',
  },
];

function CandidateInstructionsPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: '100vh',
        padding: '4rem 1.5rem',
        position: 'relative',
      }}
    >
      <CrossGridBackground opacity={0.06} />

      <div
        style={{
          maxWidth: 680,
          margin: '0 auto',
          position: 'relative',
          zIndex: 10,
        }}
      >
        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeInUp}
          transition={transitionSlow}
          style={{ textAlign: 'center', marginBottom: '2.5rem' }}
        >
          <h1
            style={{
              fontSize: 'clamp(1.5rem, 3.5vw, 2rem)',
              fontWeight: 700,
              color: '#F9FAFB',
              marginBottom: '0.625rem',
            }}
          >
            Before you begin
          </h1>
          <p style={{ color: '#6B7280', fontSize: '0.9rem' }}>
            Read these carefully — they'll help you perform your best.
          </p>
        </motion.div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.875rem',
            marginBottom: '2.5rem',
          }}
        >
          {INSTRUCTIONS.map(function (item) {
            return (
              <InstructionCard
                key={item.title}
                icon={item.icon}
                title={item.title}
                description={item.description}
                accent={item.accent}
              />
            );
          })}
        </motion.div>

        <motion.div
          initial="hidden"
          animate="visible"
          variants={fadeInUp}
          transition={{ ...transitionDefault, delay: 0.3 }}
        >
          <button
            onClick={function () {
              navigate(
                '/candidate/' + interviewId + '/permissions'
              );
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
              transition: 'opacity 200ms ease',
              marginBottom: '1.5rem',
            }}
            onMouseEnter={function (e) {
              e.currentTarget.style.opacity = '0.88';
            }}
            onMouseLeave={function (e) {
              e.currentTarget.style.opacity = '1';
            }}
          >
            I understand, continue →
          </button>

          <div style={{ textAlign: 'center' }}>
            <StepProgressDots total={4} current={2} />
            <p
              style={{
                color: '#4B5563',
                fontSize: '0.75rem',
                marginTop: '0.75rem',
              }}
            >
              Step 3 of 4
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default CandidateInstructionsPage;
