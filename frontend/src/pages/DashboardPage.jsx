import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth.js';
import analyticsService from '../services/analyticsService.js';
import StatsGrid from '../components/dashboard/StatsGrid.jsx';
import QuickActions from '../components/dashboard/QuickActions.jsx';
import ProgressChart from '../components/dashboard/ProgressChart.jsx';
import RecentActivity from '../components/dashboard/RecentActivity.jsx';
import { fadeInUp } from '../animations/variants.js';
import { transitionDefault } from '../animations/transitions.js';

const cardStyle = {
  background: 'rgba(17, 24, 39, 0.6)',
  backdropFilter: 'blur(12px)',
  WebkitBackdropFilter: 'blur(12px)',
  border: '1px solid rgba(255, 255, 255, 0.08)',
  borderRadius: '1rem',
  padding: '1.5rem',
};

function SectionTitle(props) {
  return (
    <h2
      style={{
        color: '#F9FAFB',
        fontSize: '1rem',
        fontWeight: 600,
        marginBottom: '1.25rem',
      }}
    >
      {props.children}
    </h2>
  );
}

function DashboardPage() {
  const auth = useAuth();
  const user = auth.user;

  const [dashboard, setDashboard] = useState(null);
  const [interviewAnalytics, setInterviewAnalytics] = useState(null);
  const [typingAnalytics, setTypingAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(function () {
    async function loadData() {
      try {
        const results = await Promise.all([
          analyticsService.getDashboard(),
          analyticsService.getInterviewAnalytics(),
          analyticsService.getTypingAnalytics(),
        ]);
        setDashboard(results[0]);
        setInterviewAnalytics(results[1]);
        setTypingAnalytics(results[2]);
      } catch {
        setError('Failed to load dashboard data. Please try again.');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const firstName =
    user && user.full_name ? user.full_name.split(' ')[0] : 'there';

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
              animation: 'dashboardSpin 0.8s linear infinite',
            }}
          />
          Loading your dashboard...
          <style>{'@keyframes dashboardSpin { to { transform: rotate(360deg); } }'}</style>
        </div>
      </div>
    );
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        padding: '6rem 2rem 4rem',
        maxWidth: 1200,
        margin: '0 auto',
      }}
    >
      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        transition={transitionDefault}
        style={{ marginBottom: '2.5rem' }}
      >
        <h1
          style={{
            color: '#F9FAFB',
            fontSize: '1.75rem',
            fontWeight: 700,
            marginBottom: '0.375rem',
          }}
        >
          Welcome back, {firstName}
        </h1>
        <p style={{ color: '#6B7280', fontSize: '0.9rem' }}>
          Here's how your interview prep is going.
        </p>
      </motion.div>

      {error ? (
        <div
          style={{
            background: 'rgba(248, 113, 113, 0.1)',
            border: '1px solid rgba(248, 113, 113, 0.3)',
            borderRadius: '0.625rem',
            padding: '0.875rem 1rem',
            marginBottom: '2rem',
            color: '#FCA5A5',
            fontSize: '0.875rem',
          }}
        >
          {error}
        </div>
      ) : null}

      <div style={{ marginBottom: '2rem' }}>
        <StatsGrid data={dashboard} />
      </div>

      <div style={{ marginBottom: '2.5rem' }}>
        <SectionTitle>Quick actions</SectionTitle>
        <QuickActions />
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: '1fr 1fr',
          gap: '1.5rem',
          marginBottom: '2.5rem',
        }}
      >
        <div style={cardStyle}>
          <SectionTitle>Interview score trend</SectionTitle>
          <ProgressChart
            trend={interviewAnalytics ? interviewAnalytics.score_trend : null}
            label={'Trend: ' + (interviewAnalytics ? interviewAnalytics.trend : 'no_data')}
            color="#2DD4BF"
          />
        </div>
        <div style={cardStyle}>
          <SectionTitle>Typing speed trend</SectionTitle>
          <ProgressChart
            trend={typingAnalytics ? typingAnalytics.wpm_trend : null}
            label={'Best: ' + (typingAnalytics ? typingAnalytics.best_wpm : 0) + ' WPM'}
            color="#34D399"
          />
        </div>
      </div>

      <div style={cardStyle}>
        <SectionTitle>Recent activity</SectionTitle>
        <RecentActivity
          interviewTrend={interviewAnalytics ? interviewAnalytics.score_trend : []}
          typingTrend={typingAnalytics ? typingAnalytics.wpm_trend : []}
        />
      </div>
    </div>
  );
}

export default DashboardPage;
