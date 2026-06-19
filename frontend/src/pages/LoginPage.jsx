import { useState } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { useDispatch } from "react-redux";
import { setCredentials } from "../store/slices/authSlice.js";
import authService from "../services/authService.js";
import AuthSidePanel from "../components/auth/AuthSidePanel.jsx";

function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();

  const [form, setForm] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [loading, setLoading] = useState(false);

  const from =
    location.state && location.state.from
      ? location.state.from.pathname
      : "/dashboard";

  function validate() {
    const errs = {};
    if (!form.email.trim()) {
      errs.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(form.email)) {
      errs.email = "Enter a valid email";
    }
    if (!form.password) {
      errs.password = "Password is required";
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
        return Object.assign({}, prev, { [name]: "" });
      });
    }
    if (apiError) {
      setApiError("");
    }
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const errs = validate();
    if (Object.keys(errs).length > 0) {
      setErrors(errs);
      return;
    }

    setLoading(true);
    try {
      const loginResult = await authService.login(form);
      localStorage.setItem("access_token", loginResult.access_token);
      const user = await authService.getProfile();
      dispatch(setCredentials({ user: user, token: loginResult.access_token }));
      navigate(from, { replace: true });
    } catch (err) {
      const detail =
        err.response && err.response.data ? err.response.data.detail : null;
      const msg = detail || "Invalid email or password. Please try again.";
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  }

  function inputStyleFor(hasError) {
    return {
      width: "100%",
      padding: "0.75rem 1rem",
      background: "rgba(255,255,255,0.05)",
      border:
        "1px solid " +
        (hasError ? "rgba(248,113,113,0.5)" : "rgba(255,255,255,0.1)"),
      borderRadius: "0.625rem",
      color: "#F9FAFB",
      fontSize: "0.95rem",
      outline: "none",
      transition: "border-color 200ms ease",
      boxSizing: "border-box",
    };
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        width: "100%",
      }}
    >
      {/* Left — animated side panel, takes remaining space, hidden on small screens */}
      <div
        className="auth-side-panel"
        style={{
          flex: "1 1 0%",
          minWidth: 0,
        }}
      >
        <AuthSidePanel />
      </div>

      {/* Right — form card, fixed width, hugs the right edge */}
      <div
        className="auth-form-side"
        style={{
          flex: "0 0 480px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          padding: "2rem 3rem",
          minHeight: "100vh",
          boxSizing: "border-box",
        }}
      >
        <div style={{ width: "100%", maxWidth: 440 }}>
          <div style={{ textAlign: "center", marginBottom: "2.5rem" }}>
            <Link
              to="/"
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "0.625rem",
                textDecoration: "none",
              }}
            >
              <div
                style={{
                  width: 38,
                  height: 38,
                  borderRadius: "0.625rem",
                  background: "linear-gradient(135deg, #2DD4BF, #06B6D4)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: "0.875rem",
                  fontWeight: 800,
                  color: "#0A0E14",
                }}
              >
                CB
              </div>
              <span
                style={{
                  fontWeight: 700,
                  fontSize: "1.2rem",
                  color: "#F9FAFB",
                }}
              >
                Career
                <span
                  style={{
                    background: "linear-gradient(135deg, #2DD4BF, #06B6D4)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                    backgroundClip: "text",
                  }}
                >
                  Boost
                </span>
              </span>
            </Link>
          </div>

          <div
            style={{
              background: "rgba(17, 24, 39, 0.6)",
              backdropFilter: "blur(12px)",
              WebkitBackdropFilter: "blur(12px)",
              border: "1px solid rgba(255, 255, 255, 0.08)",
              borderRadius: "1rem",
              padding: "2.5rem",
            }}
          >
            <h1
              style={{
                fontSize: "1.75rem",
                fontWeight: 700,
                marginBottom: "0.5rem",
                color: "#F9FAFB",
                textAlign: "center",
              }}
            >
              Welcome back
            </h1>
            <p
              style={{
                color: "#6B7280",
                textAlign: "center",
                marginBottom: "2rem",
                fontSize: "0.9rem",
              }}
            >
              Sign in to continue your interview prep
            </p>

            {apiError ? (
              <div
                style={{
                  background: "rgba(248, 113, 113, 0.1)",
                  border: "1px solid rgba(248, 113, 113, 0.3)",
                  borderRadius: "0.5rem",
                  padding: "0.75rem 1rem",
                  marginBottom: "1.5rem",
                  color: "#FCA5A5",
                  fontSize: "0.875rem",
                }}
              >
                {apiError}
              </div>
            ) : null}

            <form onSubmit={handleSubmit} noValidate>
              <div style={{ marginBottom: "1.25rem" }}>
                <label
                  htmlFor="email"
                  style={{
                    display: "block",
                    fontSize: "0.875rem",
                    fontWeight: 500,
                    color: "#D1D5DB",
                    marginBottom: "0.5rem",
                  }}
                >
                  Email address
                </label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="you@example.com"
                  style={inputStyleFor(Boolean(errors.email))}
                  onFocus={function (e) {
                    e.target.style.borderColor = errors.email
                      ? "rgba(248,113,113,0.7)"
                      : "#2DD4BF";
                  }}
                  onBlur={function (e) {
                    e.target.style.borderColor = errors.email
                      ? "rgba(248,113,113,0.5)"
                      : "rgba(255,255,255,0.1)";
                  }}
                />
                {errors.email ? (
                  <p
                    style={{
                      color: "#FCA5A5",
                      fontSize: "0.8rem",
                      marginTop: "0.375rem",
                    }}
                  >
                    {errors.email}
                  </p>
                ) : null}
              </div>

              <div style={{ marginBottom: "1.75rem" }}>
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    marginBottom: "0.5rem",
                  }}
                >
                  <label
                    htmlFor="password"
                    style={{
                      fontSize: "0.875rem",
                      fontWeight: 500,
                      color: "#D1D5DB",
                    }}
                  >
                    Password
                  </label>
                  <a
                    href="#"
                    style={{
                      fontSize: "0.8rem",
                      color: "#2DD4BF",
                      textDecoration: "none",
                    }}
                  >
                    Forgot password?
                  </a>
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="current-password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Enter password"
                  style={inputStyleFor(Boolean(errors.password))}
                  onFocus={function (e) {
                    e.target.style.borderColor = errors.password
                      ? "rgba(248,113,113,0.7)"
                      : "#2DD4BF";
                  }}
                  onBlur={function (e) {
                    e.target.style.borderColor = errors.password
                      ? "rgba(248,113,113,0.5)"
                      : "rgba(255,255,255,0.1)";
                  }}
                />
                {errors.password ? (
                  <p
                    style={{
                      color: "#FCA5A5",
                      fontSize: "0.8rem",
                      marginTop: "0.375rem",
                    }}
                  >
                    {errors.password}
                  </p>
                ) : null}
              </div>

              <button
                type="submit"
                disabled={loading}
                style={{
                  width: "100%",
                  padding: "0.875rem",
                  background: loading
                    ? "rgba(45, 212, 191, 0.5)"
                    : "linear-gradient(135deg, #2DD4BF, #06B6D4)",
                  color: "#0A0E14",
                  border: "none",
                  borderRadius: "0.625rem",
                  fontWeight: 700,
                  fontSize: "1rem",
                  cursor: loading ? "not-allowed" : "pointer",
                  transition: "all 200ms ease",
                }}
              >
                {loading ? "Signing in..." : "Sign in"}
              </button>
            </form>

            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "1rem",
                margin: "1.75rem 0",
              }}
            >
              <div
                style={{
                  flex: 1,
                  height: 1,
                  background: "rgba(255,255,255,0.08)",
                }}
              />
              <span style={{ color: "#4B5563", fontSize: "0.8rem" }}>
                New to CareerBoost?
              </span>
              <div
                style={{
                  flex: 1,
                  height: 1,
                  background: "rgba(255,255,255,0.08)",
                }}
              />
            </div>

            <Link
              to="/signup"
              style={{
                display: "block",
                textAlign: "center",
                padding: "0.75rem",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(255,255,255,0.08)",
                borderRadius: "0.625rem",
                color: "#D1D5DB",
                textDecoration: "none",
                fontSize: "0.9rem",
                fontWeight: 500,
                transition: "all 200ms ease",
              }}
            >
              Create a free account
            </Link>
          </div>
        </div>
      </div>

      <style>{`
        @media (max-width: 900px) {
          .auth-side-panel { display: none; }
        }
        @media (max-width: 900px) {
          .auth-form-side { flex: 1 1 100% !important; }
        }
      `}</style>
    </div>
  );
}

export default LoginPage;
