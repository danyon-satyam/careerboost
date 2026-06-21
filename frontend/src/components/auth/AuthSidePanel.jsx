import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { fadeIn } from '../../animations/variants.js';
import { transitionBounce, transitionSlow } from '../../animations/transitions.js';

const FEATURES = [
  { icon: '🎤', text: 'Practice with a real AI interviewer' },
  { icon: '⌨️', text: 'Track your typing speed and accuracy' },
  { icon: '💼', text: 'Get AI-matched job recommendations' },
  { icon: '📊', text: 'Watch your readiness score grow' },
];

function FloatingOrb(props) {
  const size = props.size;
  const top = props.top;
  const left = props.left;
  const delay = props.delay;
  const color = props.color;

  return (
    <div
      style={{
        position: 'absolute',
        top: top,
        left: left,
        width: size,
        height: size,
        borderRadius: '50%',
        background:
          'radial-gradient(circle, ' + color + ' 0%, transparent 70%)',
        animation: 'floatOrb 6s ease-in-out infinite',
        animationDelay: delay,
        pointerEvents: 'none',
      }}
    />
  );
}

function AuthSidePanel() {
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(function () {
    const interval = setInterval(function () {
      setActiveIndex(function (prev) {
        return (prev + 1) % FEATURES.length;
      });
    }, 2800);
    return function () {
      clearInterval(interval);
    };
  }, []);

  return (
    <div
      style={{
        width: '100%',
        height: '100%',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'hidden',
        minHeight: '100vh',
        padding: '3rem',
        boxSizing: 'border-box',
      }}
    >
      <FloatingOrb size={280} top="10%" left="15%" delay="0s" color="rgba(45,212,191,0.18)" />
      <FloatingOrb size={200} top="55%" left="60%" delay="1.5s" color="rgba(6,182,212,0.14)" />
      <FloatingOrb size={160} top="70%" left="10%" delay="3s" color="rgba(45,212,191,0.12)" />

      {/* Orbiting ring decoration */}
      <div
        style={{
          position: 'absolute',
          width: 380,
          height: 380,
          borderRadius: '50%',
          border: '1px solid rgba(45,212,191,0.15)',
          animation: 'spinSlow 20s linear infinite',
        }}
      >
        <div
          style={{
            position: 'absolute',
            top: -6,
            left: '50%',
            width: 12,
            height: 12,
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
            boxShadow: '0 0 16px rgba(45,212,191,0.6)',
          }}
        />
      </div>
      <div
        style={{
          position: 'absolute',
          width: 280,
          height: 280,
          borderRadius: '50%',
          border: '1px solid rgba(6,182,212,0.12)',
          animation: 'spinSlowReverse 14s linear infinite',
        }}
      >
        <div
          style={{
            position: 'absolute',
            bottom: -5,
            left: '50%',
            width: 10,
            height: 10,
            borderRadius: '50%',
            background: '#06B6D4',
            boxShadow: '0 0 12px rgba(6,182,212,0.6)',
          }}
        />
      </div>

      {/* Center content */}
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeIn}
        transition={transitionSlow}
        style={{ position: 'relative', zIndex: 10, textAlign: 'center', maxWidth: 380 }}
      >
        <motion.div
          initial={{ scale: 0, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={transitionBounce}
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
            animation: 'pulseGlow 3s ease-in-out infinite',
          }}
        >
          CB
        </motion.div>

        <h2
          style={{
            color: '#F9FAFB',
            fontSize: '1.5rem',
            fontWeight: 700,
            marginBottom: '0.75rem',
            lineHeight: 1.3,
          }}
        >
          Your AI-powered path to the offer
        </h2>
        <p style={{ color: '#6B7280', fontSize: '0.9rem', marginBottom: '2.5rem' }}>
          Join thousands prepping smarter, not harder.
        </p>

        {/* Rotating feature row */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            padding: '0.875rem 1.25rem',
            background: 'rgba(255,255,255,0.04)',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '0.75rem',
            minHeight: 52,
          }}
        >
          <span style={{ fontSize: '1.2rem' }}>{FEATURES[activeIndex].icon}</span>
          <span style={{ color: '#D1D5DB', fontSize: '0.875rem', fontWeight: 500 }}>
            {FEATURES[activeIndex].text}
          </span>
        </div>

        {/* Dots */}
        <div style={{ display: 'flex', gap: '0.4rem', justifyContent: 'center', marginTop: '1.25rem' }}>
          {FEATURES.map(function (_, i) {
            return (
              <div
                key={i}
                style={{
                  width: i === activeIndex ? 18 : 6,
                  height: 6,
                  borderRadius: '999px',
                  background: i === activeIndex ? '#2DD4BF' : 'rgba(255,255,255,0.15)',
                  transition: 'all 300ms ease',
                }}
              />
            );
          })}
        </div>
      </motion.div>

      <style>{`
        @keyframes floatOrb {
          0%, 100% { transform: translate(0, 0); }
          50% { transform: translate(20px, -20px); }
        }
        @keyframes spinSlow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        @keyframes spinSlowReverse {
          from { transform: rotate(360deg); }
          to { transform: rotate(0deg); }
        }
        @keyframes pulseGlow {
          0%, 100% { box-shadow: 0 0 40px rgba(45,212,191,0.35); }
          50% { box-shadow: 0 0 60px rgba(45,212,191,0.55); }
        }
      `}</style>
    </div>
  );
}

export default AuthSidePanel;
