import { Link } from 'react-router-dom';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';

// ── Design constants ─────────────────────────────────────
const SECTION_MAX_WIDTH = 1200;
const SECTION_PADDING = '5rem 2rem';

// ── Reusable components ──────────────────────────────────

function FeatureCard({ icon, title, description }) {
  return (
    <div
      style={{
        flex: '1 1 320px',
        maxWidth: 380,
        padding: '1.75rem',
        background: 'rgba(17, 24, 39, 0.6)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '1rem',
        transition: 'all 250ms ease',
        cursor: 'default',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem',
      }}
      onMouseEnter={(e) => {
        e.currentTarget.style.borderColor = 'rgba(45, 212, 191, 0.3)';
        e.currentTarget.style.transform = 'translateY(-3px)';
        e.currentTarget.style.boxShadow =
          '0 8px 32px rgba(45, 212, 191, 0.1)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.08)';
        e.currentTarget.style.transform = 'translateY(0)';
        e.currentTarget.style.boxShadow = 'none';
      }}
    >
      <div
        style={{
          width: 48,
          height: 48,
          borderRadius: '0.75rem',
          background: 'rgba(45, 212, 191, 0.1)',
          border: '1px solid rgba(45, 212, 191, 0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '1.4rem',
          flexShrink: 0,
        }}
      >
        {icon}
      </div>
      <div>
        <h3
          style={{
            color: '#F9FAFB',
            fontWeight: 600,
            fontSize: '1.05rem',
            marginBottom: '0.5rem',
          }}
        >
          {title}
        </h3>
        <p
          style={{
            color: '#6B7280',
            fontSize: '0.875rem',
            lineHeight: 1.7,
          }}
        >
          {description}
        </p>
      </div>
    </div>
  );
}

function StatItem({ value, label }) {
  return (
    <div style={{ textAlign: 'center' }}>
      <div
        style={{
          fontSize: '2rem',
          fontWeight: 800,
          background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          lineHeight: 1.1,
          marginBottom: '0.375rem',
        }}
      >
        {value}
      </div>
      <div style={{ color: '#6B7280', fontSize: '0.8rem', fontWeight: 500 }}>
        {label}
      </div>
    </div>
  );
}

function StepCard({ number, title, description }) {
  return (
    <div
      style={{
        flex: '1 1 180px',
        padding: '1.5rem',
        background: 'rgba(17, 24, 39, 0.5)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        border: '1px solid rgba(255, 255, 255, 0.07)',
        borderRadius: '1rem',
      }}
    >
      <div
        style={{
          fontSize: '1.75rem',
          fontWeight: 800,
          background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          lineHeight: 1,
          marginBottom: '0.75rem',
        }}
      >
        {number}
      </div>
      <h3
        style={{
          fontWeight: 600,
          fontSize: '0.95rem',
          color: '#F9FAFB',
          marginBottom: '0.5rem',
        }}
      >
        {title}
      </h3>
      <p style={{ color: '#6B7280', fontSize: '0.825rem', lineHeight: 1.6 }}>
        {description}
      </p>
    </div>
  );
}

function SectionLabel({ children }) {
  return (
    <p
      style={{
        color: '#2DD4BF',
        fontWeight: 600,
        fontSize: '0.75rem',
        letterSpacing: '0.12em',
        textTransform: 'uppercase',
        marginBottom: '0.875rem',
      }}
    >
      {children}
    </p>
  );
}

function SectionHeading({ children }) {
  return (
    <h2
      style={{
        fontSize: 'clamp(1.75rem, 3.5vw, 2.5rem)',
        fontWeight: 700,
        color: '#F9FAFB',
        lineHeight: 1.2,
        marginBottom: '1rem',
      }}
    >
      {children}
    </h2>
  );
}

function scrollTo(id) {
  const el = document.getElementById(id);
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Main component ───────────────────────────────────────

function LandingPage() {
  return (
    <div
      style={{
        minHeight: '100vh',
        color: '#F9FAFB',
        fontFamily: "'Inter', sans-serif",
        overflowX: 'hidden',
      }}
    >

      {/* ── Navbar ───────────────────────────────────── */}
      <nav
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          zIndex: 100,
          height: 60,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 2.5rem',
          background: 'rgba(10, 14, 20, 0.9)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderBottom: '1px solid rgba(255,255,255,0.05)',
        }}
      >
        {/* Logo */}
        <button
          onClick={() => scrollTo('hero')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.625rem',
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            padding: 0,
          }}
        >
          <div
            style={{
              width: 32,
              height: 32,
              borderRadius: '0.5rem',
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '0.75rem',
              fontWeight: 800,
              color: '#0A0E14',
            }}
          >
            CB
          </div>
          <span
            style={{ fontWeight: 700, fontSize: '1.05rem', color: '#F9FAFB' }}
          >
            Career
            <span
              style={{
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              Boost
            </span>
          </span>
        </button>

        {/* Nav links */}
        <div style={{ display: 'flex', gap: '2.5rem', alignItems: 'center' }}>
          {[
            { label: 'Features', id: 'features' },
            { label: 'How it works', id: 'how-it-works' },
            { label: 'Pricing', id: 'pricing' },
          ].map(({ label, id }) => (
            <button
              key={id}
              onClick={() => scrollTo(id)}
              style={{
                background: 'none',
                border: 'none',
                color: '#9CA3AF',
                fontSize: '0.875rem',
                cursor: 'pointer',
                fontFamily: 'inherit',
                padding: 0,
                transition: 'color 200ms ease',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.color = '#F9FAFB')}
              onMouseLeave={(e) =>
                (e.currentTarget.style.color = '#9CA3AF')
              }
            >
              {label}
            </button>
          ))}
        </div>

        {/* Auth */}
        <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
          <Link
            to="/login"
            style={{
              color: '#9CA3AF',
              textDecoration: 'none',
              fontSize: '0.875rem',
              padding: '0.4rem 0.875rem',
              borderRadius: '0.5rem',
              transition: 'color 200ms ease',
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.color = '#F9FAFB')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.color = '#9CA3AF')
            }
          >
            Log in
          </Link>
          <Link
            to="/signup"
            style={{
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              color: '#0A0E14',
              textDecoration: 'none',
              fontWeight: 600,
              fontSize: '0.875rem',
              padding: '0.5rem 1.125rem',
              borderRadius: '0.5rem',
              whiteSpace: 'nowrap',
              transition: 'opacity 200ms ease',
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.opacity = '0.85')
            }
            onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
          >
            Get started free
          </Link>
        </div>
      </nav>

      {/* ── Hero ─────────────────────────────────────── */}
      <section
        id="hero"
        style={{
          position: 'relative',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          textAlign: 'center',
          // 60px = navbar height, 40px breathing room top, 60px bottom
          padding: '100px 2rem 60px',
        }}
      >
        <CrossGridBackground opacity={0.1} />

        {/* Glow blobs */}
        <div
          style={{
            position: 'absolute',
            top: '25%',
            left: '15%',
            width: 420,
            height: 420,
            borderRadius: '50%',
            background:
              'radial-gradient(circle, rgba(45,212,191,0.1) 0%, transparent 70%)',
            pointerEvents: 'none',
          }}
        />
        <div
          style={{
            position: 'absolute',
            bottom: '20%',
            right: '12%',
            width: 320,
            height: 320,
            borderRadius: '50%',
            background:
              'radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%)',
            pointerEvents: 'none',
          }}
        />

        <div
          style={{ position: 'relative', zIndex: 10, maxWidth: 760 }}
        >
          {/* Badge */}
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              background: 'rgba(45, 212, 191, 0.08)',
              border: '1px solid rgba(45, 212, 191, 0.22)',
              borderRadius: '9999px',
              padding: '0.35rem 1rem',
              fontSize: '0.78rem',
              color: '#2DD4BF',
              marginBottom: '1.75rem',
              fontWeight: 500,
              letterSpacing: '0.01em',
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
            Powered by Gemini AI · 100% Free
          </div>

          {/* Headline */}
          <h1
            style={{
              fontSize: 'clamp(2.25rem, 5.5vw, 4rem)',
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: '1.25rem',
              letterSpacing: '-0.025em',
              color: '#F9FAFB',
            }}
          >
            Ace every interview
            <br />
            with{' '}
            <span
              style={{
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              AI-powered
            </span>{' '}
            prep
          </h1>

          {/* Sub */}
          <p
            style={{
              fontSize: 'clamp(0.95rem, 1.8vw, 1.125rem)',
              color: '#9CA3AF',
              lineHeight: 1.75,
              maxWidth: 540,
              margin: '0 auto 2.25rem',
            }}
          >
            Practice with a real AI interviewer, track your typing speed,
            discover matching jobs — all in one platform built for serious
            candidates.
          </p>

          {/* CTAs */}
          <div
            style={{
              display: 'flex',
              gap: '0.875rem',
              justifyContent: 'center',
              flexWrap: 'wrap',
              marginBottom: '3.5rem',
            }}
          >
            <Link
              to="/signup"
              style={{
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                color: '#0A0E14',
                textDecoration: 'none',
                fontWeight: 700,
                fontSize: '0.95rem',
                padding: '0.8rem 1.875rem',
                borderRadius: '0.625rem',
                boxShadow: '0 0 24px rgba(45,212,191,0.32)',
                transition: 'all 200ms ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow =
                  '0 0 36px rgba(45,212,191,0.52)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow =
                  '0 0 24px rgba(45,212,191,0.32)';
              }}
            >
              Start practicing free →
            </Link>
            <Link
              to="/login"
              style={{
                background: 'rgba(255,255,255,0.04)',
                color: '#F9FAFB',
                textDecoration: 'none',
                fontWeight: 500,
                fontSize: '0.95rem',
                padding: '0.8rem 1.875rem',
                borderRadius: '0.625rem',
                border: '1px solid rgba(255,255,255,0.1)',
                transition: 'all 200ms ease',
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.borderColor =
                  'rgba(45,212,191,0.35)';
                e.currentTarget.style.color = '#2DD4BF';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.borderColor =
                  'rgba(255,255,255,0.1)';
                e.currentTarget.style.color = '#F9FAFB';
              }}
            >
              Sign in
            </Link>
          </div>

          {/* Stats */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr auto 1fr auto 1fr',
              alignItems: 'center',
              gap: '0.5rem',
              padding: '1.5rem 2rem',
              background: 'rgba(255,255,255,0.03)',
              borderRadius: '0.875rem',
              border: '1px solid rgba(255,255,255,0.07)',
              backdropFilter: 'blur(8px)',
              WebkitBackdropFilter: 'blur(8px)',
              maxWidth: 480,
              margin: '0 auto',
            }}
          >
            <StatItem value="10K+" label="Interviews completed" />
            <div
              style={{
                width: 1,
                height: 36,
                background: 'rgba(255,255,255,0.1)',
              }}
            />
            <StatItem value="93%" label="Avg test coverage" />
            <div
              style={{
                width: 1,
                height: 36,
                background: 'rgba(255,255,255,0.1)',
              }}
            />
            <StatItem value="$0" label="Forever free" />
          </div>
        </div>
      </section>

      {/* ── Features ─────────────────────────────────── */}
      <section
        id="features"
        style={{ padding: SECTION_PADDING, scrollMarginTop: 60 }}
      >
        <div style={{ maxWidth: SECTION_MAX_WIDTH, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <SectionLabel>Everything you need</SectionLabel>
            <SectionHeading>Three platforms, one goal</SectionHeading>
            <p
              style={{
                color: '#6B7280',
                maxWidth: 480,
                margin: '0 auto',
                lineHeight: 1.65,
                fontSize: '0.9rem',
              }}
            >
              AI interview practice, typing training, and job matching
              — in one focused platform.
            </p>
          </div>

          <div
            style={{
              display: 'flex',
              gap: '1.25rem',
              flexWrap: 'wrap',
              justifyContent: 'center',
            }}
          >
            <FeatureCard
              icon="🎤"
              title="AI Mock Interviews"
              description="Practice with a Gemini-powered AI interviewer that adapts questions to your resume and job description. Get scored answers and follow-up questions."
            />
            <FeatureCard
              icon="⌨️"
              title="Typing Practice"
              description="Improve your typing speed with Monkeytype-inspired tests at easy, medium, hard, and code difficulty levels. Track WPM and accuracy over time."
            />
            <FeatureCard
              icon="💼"
              title="Smart Job Portal"
              description="Upload your resume and get AI-ranked job matches based on skill overlap, experience, and semantic profile similarity."
            />
            <FeatureCard
              icon="📊"
              title="Analytics Dashboard"
              description="Track interview score trends, typing speed progress, and your overall job-readiness score in one clean dashboard."
            />
            <FeatureCard
              icon="🧠"
              title="NLP Answer Analysis"
              description="Every spoken answer is evaluated by spaCy NLP and Gemini AI — real-time feedback on clarity, depth, and technical accuracy."
            />
            <FeatureCard
              icon="🔒"
              title="100% Free Stack"
              description="Gemini 2.0 Flash (1500 req/day), DuckDuckGo search, spaCy offline NLP. No credit card, no paid APIs, no limits that matter."
            />
          </div>
        </div>
      </section>

      {/* ── How it works ─────────────────────────────── */}
      <section
        id="how-it-works"
        style={{ padding: SECTION_PADDING, scrollMarginTop: 60 }}
      >
        <div style={{ maxWidth: SECTION_MAX_WIDTH, margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
            <SectionLabel>How it works</SectionLabel>
            <SectionHeading>
              From signup to offer-ready in days
            </SectionHeading>
          </div>
          <div
            style={{
              display: 'flex',
              gap: '1rem',
              flexWrap: 'wrap',
              justifyContent: 'center',
            }}
          >
            <StepCard
              number="01"
              title="Create your account"
              description="Sign up free — no credit card needed."
            />
            <StepCard
              number="02"
              title="Upload your resume"
              description="AI parses your skills and experience automatically."
            />
            <StepCard
              number="03"
              title="Browse matching jobs"
              description="Get ranked recommendations based on your profile."
            />
            <StepCard
              number="04"
              title="Practice interviews"
              description="Speak your answers, get AI scores and feedback."
            />
            <StepCard
              number="05"
              title="Track your progress"
              description="Watch scores improve in your analytics dashboard."
            />
          </div>
        </div>
      </section>

      {/* ── Pricing ──────────────────────────────────── */}
      <section
        id="pricing"
        style={{ padding: SECTION_PADDING, scrollMarginTop: 60 }}
      >
        <div
          style={{
            maxWidth: 560,
            margin: '0 auto',
            textAlign: 'center',
          }}
        >
          <SectionLabel>Pricing</SectionLabel>
          <SectionHeading>
            Simple pricing — always{' '}
            <span
              style={{
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              free
            </span>
          </SectionHeading>
          <p
            style={{
              color: '#6B7280',
              lineHeight: 1.65,
              marginBottom: '2.5rem',
              fontSize: '0.9rem',
            }}
          >
            CareerBoost is built on a 100% free AI stack. No subscriptions,
            no credits, no paywalls.
          </p>

          <div
            style={{
              padding: '2.5rem 2rem',
              background: 'rgba(17, 24, 39, 0.6)',
              backdropFilter: 'blur(12px)',
              WebkitBackdropFilter: 'blur(12px)',
              border: '1px solid rgba(45, 212, 191, 0.25)',
              borderRadius: '1.25rem',
              boxShadow: '0 0 40px rgba(45, 212, 191, 0.08)',
            }}
          >
            <div
              style={{
                fontSize: '3.5rem',
                fontWeight: 800,
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
                lineHeight: 1,
                marginBottom: '0.5rem',
              }}
            >
              $0
            </div>
            <p
              style={{
                color: '#9CA3AF',
                marginBottom: '2rem',
                fontSize: '0.875rem',
              }}
            >
              Forever free · No credit card required
            </p>

            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '0.625rem',
                marginBottom: '2rem',
                textAlign: 'left',
              }}
            >
              {[
                'Unlimited AI mock interviews',
                'AI-generated adaptive questions',
                'Gemini-powered answer evaluation',
                'Typing practice at all difficulty levels',
                'Smart job matching & recommendations',
                'Resume parsing & skill extraction',
                'Analytics dashboard & progress tracking',
                'DuckDuckGo-powered web search context',
              ].map((f) => (
                <div
                  key={f}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.75rem',
                    fontSize: '0.875rem',
                    color: '#D1D5DB',
                  }}
                >
                  <span
                    style={{
                      color: '#2DD4BF',
                      fontWeight: 700,
                      flexShrink: 0,
                    }}
                  >
                    ✓
                  </span>
                  {f}
                </div>
              ))}
            </div>

            <Link
              to="/signup"
              style={{
                display: 'block',
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                color: '#0A0E14',
                textDecoration: 'none',
                fontWeight: 700,
                fontSize: '0.95rem',
                padding: '0.875rem',
                borderRadius: '0.625rem',
                textAlign: 'center',
                transition: 'opacity 200ms ease',
              }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.opacity = '0.85')
              }
              onMouseLeave={(e) => (e.currentTarget.style.opacity = '1')}
            >
              Get started free →
            </Link>
          </div>
        </div>
      </section>

      {/* ── Final CTA ────────────────────────────────── */}
      <section
        style={{
          padding: SECTION_PADDING,
          textAlign: 'center',
          position: 'relative',
        }}
      >
        <CrossGridBackground opacity={0.06} />
        <div style={{ position: 'relative', zIndex: 10 }}>
          <h2
            style={{
              fontSize: 'clamp(1.75rem, 4vw, 3rem)',
              fontWeight: 800,
              marginBottom: '1rem',
              lineHeight: 1.2,
              color: '#F9FAFB',
            }}
          >
            Ready to land your{' '}
            <span
              style={{
                background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              dream role?
            </span>
          </h2>
          <p
            style={{
              color: '#9CA3AF',
              marginBottom: '2.25rem',
              fontSize: '1rem',
            }}
          >
            Join CareerBoost today — completely free, forever.
          </p>
          <Link
            to="/signup"
            style={{
              display: 'inline-block',
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              color: '#0A0E14',
              textDecoration: 'none',
              fontWeight: 700,
              fontSize: '1rem',
              padding: '0.9rem 2.25rem',
              borderRadius: '0.75rem',
              boxShadow: '0 0 28px rgba(45,212,191,0.38)',
              transition: 'all 200ms ease',
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-3px)';
              e.currentTarget.style.boxShadow =
                '0 0 44px rgba(45,212,191,0.55)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow =
                '0 0 28px rgba(45,212,191,0.38)';
            }}
          >
            Get started free →
          </Link>
        </div>
      </section>

      {/* ── Footer ───────────────────────────────────── */}
      <footer
        style={{
          padding: '1.75rem 2rem',
          textAlign: 'center',
          borderTop: '1px solid rgba(255,255,255,0.05)',
        }}
      >
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.5rem',
            marginBottom: '0.5rem',
          }}
        >
          <div
            style={{
              width: 18,
              height: 18,
              borderRadius: '0.25rem',
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
            }}
          />
          <span style={{ fontWeight: 600, color: '#6B7280', fontSize: '0.875rem' }}>
            CareerBoost
          </span>
        </div>
        <p style={{ color: '#4B5563', fontSize: '0.8rem' }}>
          © 2026 CareerBoost. Built with FastAPI + React + Gemini AI.
        </p>
      </footer>
    </div>
  );
}

export default LandingPage;
