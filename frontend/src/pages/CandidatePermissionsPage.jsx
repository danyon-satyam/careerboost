import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { fadeInUp, staggerContainer, staggerItem } from '../animations/variants.js';
import { transitionDefault } from '../animations/transitions.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';
import StepProgressDots from '../components/candidate/StepProgressDots.jsx';
import { usePermissions } from '../hooks/usePermissions.js';

function PermissionRow(props) {
  const icon = props.icon;
  const title = props.title;
  const description = props.description;
  const granted = props.granted;
  const error = props.error;
  const onRequest = props.onRequest;

  return (
    <motion.div
      variants={staggerItem}
      transition={transitionDefault}
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '1.125rem 1.25rem',
        background: granted
          ? 'rgba(45,212,191,0.06)'
          : 'rgba(17,24,39,0.5)',
        border: granted
          ? '1px solid rgba(45,212,191,0.2)'
          : '1px solid rgba(255,255,255,0.07)',
        borderRadius: '0.875rem',
        gap: '1rem',
        transition: 'all 300ms ease',
      }}
    >
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.875rem', flex: 1 }}>
        <div
          style={{
            width: 40,
            height: 40,
            borderRadius: '0.625rem',
            background: granted
              ? 'rgba(45,212,191,0.15)'
              : 'rgba(255,255,255,0.06)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.1rem',
            flexShrink: 0,
          }}
        >
          {granted ? '✓' : icon}
        </div>
        <div>
          <p
            style={{
              color: granted ? '#2DD4BF' : '#F9FAFB',
              fontWeight: 600,
              fontSize: '0.9rem',
              marginBottom: '0.2rem',
            }}
          >
            {title}
          </p>
          <p style={{ color: '#6B7280', fontSize: '0.8rem' }}>
            {error ? (
              <span style={{ color: '#FCA5A5' }}>{error}</span>
            ) : description}
          </p>
        </div>
      </div>

      {!granted && (
        <button
          onClick={onRequest}
          style={{
            padding: '0.5rem 1rem',
            background: 'rgba(45,212,191,0.1)',
            border: '1px solid rgba(45,212,191,0.25)',
            borderRadius: '0.5rem',
            color: '#2DD4BF',
            fontSize: '0.8rem',
            fontWeight: 600,
            cursor: 'pointer',
            fontFamily: 'inherit',
            whiteSpace: 'nowrap',
            flexShrink: 0,
            transition: 'all 200ms ease',
          }}
          onMouseEnter={function (e) {
            e.currentTarget.style.background = 'rgba(45,212,191,0.18)';
          }}
          onMouseLeave={function (e) {
            e.currentTarget.style.background = 'rgba(45,212,191,0.1)';
          }}
        >
          Allow
        </button>
      )}
    </motion.div>
  );
}

function CandidatePermissionsPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();
  const {
    permissions,
    errors,
    requestCamera,
    requestMicrophone,
    requestFullscreen,
    allGranted,
  } = usePermissions();

  const grantedCount = Object.values(permissions).filter(Boolean).length;

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
      }}
    >
      <CrossGridBackground opacity={0.06} />

      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        transition={transitionDefault}
        style={{
          position: 'relative',
          zIndex: 10,
          width: '100%',
          maxWidth: 520,
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h1
            style={{
              fontSize: '1.75rem',
              fontWeight: 700,
              color: '#F9FAFB',
              marginBottom: '0.5rem',
            }}
          >
            Allow permissions
          </h1>
          <p style={{ color: '#6B7280', fontSize: '0.9rem' }}>
            Grant the following to start your interview.
          </p>
        </div>

        <motion.div
          variants={staggerContainer}
          initial="hidden"
          animate="visible"
          style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem',
            marginBottom: '2rem',
          }}
        >
          <PermissionRow
            icon="📷"
            title="Camera"
            description="Required to show your video during the interview"
            granted={permissions.camera}
            error={errors.camera}
            onRequest={requestCamera}
          />
          <PermissionRow
            icon="🎤"
            title="Microphone"
            description="Required to capture your spoken answers"
            granted={permissions.microphone}
            error={errors.microphone}
            onRequest={requestMicrophone}
          />
          <PermissionRow
            icon="🖥️"
            title="Fullscreen"
            description="Keeps the interview environment distraction-free"
            granted={permissions.fullscreen}
            error={errors.fullscreen}
            onRequest={requestFullscreen}
          />
        </motion.div>

        {/* Progress indicator */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '0.75rem 1rem',
            background: 'rgba(255,255,255,0.03)',
            border: '1px solid rgba(255,255,255,0.06)',
            borderRadius: '0.625rem',
            marginBottom: '1.5rem',
          }}
        >
          <span style={{ color: '#6B7280', fontSize: '0.825rem' }}>
            Permissions granted
          </span>
          <span
            style={{
              color: allGranted ? '#2DD4BF' : '#9CA3AF',
              fontWeight: 600,
              fontSize: '0.875rem',
            }}
          >
            {grantedCount} / 3
          </span>
        </div>

        <button
          onClick={function () {
            navigate('/candidate/' + interviewId + '/live');
          }}
          disabled={!allGranted}
          style={{
            width: '100%',
            padding: '1rem',
            background: allGranted
              ? 'linear-gradient(135deg, #2DD4BF, #06B6D4)'
              : 'rgba(255,255,255,0.06)',
            color: allGranted ? '#0A0E14' : '#4B5563',
            border: 'none',
            borderRadius: '0.75rem',
            fontWeight: 700,
            fontSize: '1rem',
            cursor: allGranted ? 'pointer' : 'not-allowed',
            fontFamily: 'inherit',
            transition: 'all 200ms ease',
            boxShadow: allGranted
              ? '0 0 24px rgba(45,212,191,0.28)'
              : 'none',
            marginBottom: '1.5rem',
          }}
        >
          {allGranted ? 'Enter interview →' : 'Grant all permissions to continue'}
        </button>

        <div style={{ textAlign: 'center' }}>
          <StepProgressDots total={4} current={3} />
          <p
            style={{
              color: '#4B5563',
              fontSize: '0.75rem',
              marginTop: '0.75rem',
            }}
          >
            Step 4 of 4
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default CandidatePermissionsPage;
