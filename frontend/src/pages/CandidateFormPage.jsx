import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import { fadeInUp } from '../animations/variants.js';
import { transitionDefault } from '../animations/transitions.js';
import { setCandidateDetails } from '../store/slices/candidateSlice.js';
import CrossGridBackground from '../components/layout/CrossGridBackground.jsx';
import StepProgressDots from '../components/candidate/StepProgressDots.jsx';

function inputStyle(hasError) {
  return {
    width: '100%',
    padding: '0.75rem 1rem',
    background: 'rgba(255,255,255,0.05)',
    border:
      '1px solid ' +
      (hasError
        ? 'rgba(248,113,113,0.5)'
        : 'rgba(255,255,255,0.1)'),
    borderRadius: '0.625rem',
    color: '#F9FAFB',
    fontSize: '0.9rem',
    outline: 'none',
    boxSizing: 'border-box',
    fontFamily: 'inherit',
    transition: 'border-color 200ms ease',
  };
}

function Label(props) {
  return (
    <label
      htmlFor={props.htmlFor}
      style={{
        display: 'block',
        fontSize: '0.825rem',
        fontWeight: 500,
        color: '#D1D5DB',
        marginBottom: '0.5rem',
      }}
    >
      {props.children}
    </label>
  );
}

function CandidateFormPage() {
  const { interviewId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const context = useSelector(function (state) {
    return state.candidate;
  });

  const [form, setForm] = useState({
    full_name: context.candidate.full_name || '',
    email: context.candidate.email || '',
    experience_years: context.candidate.experience_years || '',
    gender: context.candidate.gender || '',
  });
  const [errors, setErrors] = useState({});

  function validate() {
    const errs = {};
    if (!form.full_name.trim()) {
      errs.full_name = 'Full name is required';
    }
    if (!form.email.trim()) {
      errs.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      errs.email = 'Enter a valid email';
    }
    if (!form.experience_years) {
      errs.experience_years = 'Experience is required';
    }
    return errs;
  }

  function handleChange(e) {
    const name = e.target.name;
    const value = e.target.value;
    setForm(function (prev) {
      return Object.assign({}, prev, { [name]: value });
    });
    if (errors[name]) {
      setErrors(function (prev) {
        return Object.assign({}, prev, { [name]: '' });
      });
    }
  }

  function handleSubmit() {
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }
    dispatch(setCandidateDetails(form));
    navigate('/candidate/' + interviewId + '/instructions');
  }

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
      <CrossGridBackground opacity={0.07} />

      <motion.div
        initial="hidden"
        animate="visible"
        variants={fadeInUp}
        transition={transitionDefault}
        style={{
          position: 'relative',
          zIndex: 10,
          width: '100%',
          maxWidth: 480,
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
            Your details
          </h1>
          <p style={{ color: '#6B7280', fontSize: '0.9rem' }}>
            {context.jobTitle
              ? 'Joining the ' + context.jobTitle + ' interview'
              : 'Tell us a little about yourself'}
          </p>
        </div>

        <div
          style={{
            background: 'rgba(17, 24, 39, 0.6)',
            backdropFilter: 'blur(12px)',
            WebkitBackdropFilter: 'blur(12px)',
            border: '1px solid rgba(255,255,255,0.08)',
            borderRadius: '1rem',
            padding: '2rem',
          }}
        >
          {/* Full name */}
          <div style={{ marginBottom: '1.25rem' }}>
            <Label htmlFor="full_name">Full name</Label>
            <input
              id="full_name"
              name="full_name"
              type="text"
              autoComplete="name"
              value={form.full_name}
              onChange={handleChange}
              placeholder="Enter your full name"
              style={inputStyle(Boolean(errors.full_name))}
              onFocus={function (e) {
                e.target.style.borderColor = errors.full_name
                  ? 'rgba(248,113,113,0.7)'
                  : '#2DD4BF';
              }}
              onBlur={function (e) {
                e.target.style.borderColor = errors.full_name
                  ? 'rgba(248,113,113,0.5)'
                  : 'rgba(255,255,255,0.1)';
              }}
            />
            {errors.full_name ? (
              <p
                style={{
                  color: '#FCA5A5',
                  fontSize: '0.78rem',
                  marginTop: '0.375rem',
                }}
              >
                {errors.full_name}
              </p>
            ) : null}
          </div>

          {/* Email */}
          <div style={{ marginBottom: '1.25rem' }}>
            <Label htmlFor="email">Email address</Label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={form.email}
              onChange={handleChange}
              placeholder="you@example.com"
              style={inputStyle(Boolean(errors.email))}
              onFocus={function (e) {
                e.target.style.borderColor = errors.email
                  ? 'rgba(248,113,113,0.7)'
                  : '#2DD4BF';
              }}
              onBlur={function (e) {
                e.target.style.borderColor = errors.email
                  ? 'rgba(248,113,113,0.5)'
                  : 'rgba(255,255,255,0.1)';
              }}
            />
            {errors.email ? (
              <p
                style={{
                  color: '#FCA5A5',
                  fontSize: '0.78rem',
                  marginTop: '0.375rem',
                }}
              >
                {errors.email}
              </p>
            ) : null}
          </div>

          {/* Experience + Gender row */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '1rem',
              marginBottom: '1.75rem',
            }}
          >
            <div>
              <Label htmlFor="experience_years">
                Years of experience
              </Label>
              <select
                id="experience_years"
                name="experience_years"
                value={form.experience_years}
                onChange={handleChange}
                style={Object.assign({}, inputStyle(Boolean(errors.experience_years)), {
                  appearance: 'none',
                  WebkitAppearance: 'none',
                  cursor: 'pointer',
                })}
                onFocus={function (e) {
                  e.target.style.borderColor = '#2DD4BF';
                }}
                onBlur={function (e) {
                  e.target.style.borderColor = errors.experience_years
                    ? 'rgba(248,113,113,0.5)'
                    : 'rgba(255,255,255,0.1)';
                }}
              >
                <option value="" style={{ background: '#111827' }}>
                  Select...
                </option>
                <option value="0" style={{ background: '#111827' }}>
                  Fresher (0)
                </option>
                <option value="1" style={{ background: '#111827' }}>
                  1 year
                </option>
                <option value="2" style={{ background: '#111827' }}>
                  2 years
                </option>
                <option value="3" style={{ background: '#111827' }}>
                  3 years
                </option>
                <option value="5" style={{ background: '#111827' }}>
                  4-5 years
                </option>
                <option value="7" style={{ background: '#111827' }}>
                  6-8 years
                </option>
                <option value="10" style={{ background: '#111827' }}>
                  9+ years
                </option>
              </select>
              {errors.experience_years ? (
                <p
                  style={{
                    color: '#FCA5A5',
                    fontSize: '0.78rem',
                    marginTop: '0.375rem',
                  }}
                >
                  {errors.experience_years}
                </p>
              ) : null}
            </div>

            <div>
              <Label htmlFor="gender">
                Gender{' '}
                <span style={{ color: '#4B5563' }}>(optional)</span>
              </Label>
              <select
                id="gender"
                name="gender"
                value={form.gender}
                onChange={handleChange}
                style={Object.assign({}, inputStyle(false), {
                  appearance: 'none',
                  WebkitAppearance: 'none',
                  cursor: 'pointer',
                })}
                onFocus={function (e) {
                  e.target.style.borderColor = '#2DD4BF';
                }}
                onBlur={function (e) {
                  e.target.style.borderColor = 'rgba(255,255,255,0.1)';
                }}
              >
                <option value="" style={{ background: '#111827' }}>
                  Prefer not to say
                </option>
                <option
                  value="male"
                  style={{ background: '#111827' }}
                >
                  Male
                </option>
                <option
                  value="female"
                  style={{ background: '#111827' }}
                >
                  Female
                </option>
                <option
                  value="non_binary"
                  style={{ background: '#111827' }}
                >
                  Non-binary
                </option>
              </select>
            </div>
          </div>

          <button
            onClick={handleSubmit}
            style={{
              width: '100%',
              padding: '0.875rem',
              background: 'linear-gradient(135deg, #2DD4BF, #06B6D4)',
              color: '#0A0E14',
              border: 'none',
              borderRadius: '0.625rem',
              fontWeight: 700,
              fontSize: '1rem',
              cursor: 'pointer',
              fontFamily: 'inherit',
              transition: 'opacity 200ms ease',
            }}
            onMouseEnter={function (e) {
              e.currentTarget.style.opacity = '0.88';
            }}
            onMouseLeave={function (e) {
              e.currentTarget.style.opacity = '1';
            }}
          >
            Continue →
          </button>
        </div>

        <div
          style={{
            textAlign: 'center',
            marginTop: '1.5rem',
          }}
        >
          <StepProgressDots total={4} current={1} />
          <p
            style={{
              color: '#4B5563',
              fontSize: '0.75rem',
              marginTop: '0.75rem',
            }}
          >
            Step 2 of 4
          </p>
        </div>
      </motion.div>
    </div>
  );
}

export default CandidateFormPage;
