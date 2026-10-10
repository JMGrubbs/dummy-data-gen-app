import { useState } from "react";
import { api, ApiError } from "../services/api.js";

export default function Login({ onNavigate }) {
  const [showPassword, setShowPassword] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();
  };

  return (
    <section className="login-page shell">
      <div className="login-intro">
        <div className="pill">
          <span className="spark">✦</span> Welcome back
        </div>
        <h1>
          Make something
          <br />
          <span>real today.</span>
        </h1>
        <p>Pick up where you left off, or start with a fresh dataset in seconds.</p>
        <div className="login-quote">
          <span>“</span>
          <p>Datadrop took our prototype from empty to convincing in an afternoon.</p>
          <small>— Mina Patel, Product Designer</small>
        </div>
      </div>
      <div className="login-card">
        <div className="login-card-head">
          <h2>Log in to Datadrop</h2>
          <p>
            New here? <button onClick={() => onNavigate("/")}>Explore Datadrop</button>
          </p>
        </div>
        {submitted && (
          <div className="success-message" role="status">
            You’re all set to start generating.
          </div>
        )}
        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}
        <form
          onSubmit={async (event) => {
            event.preventDefault();
            setError("");
            setSubmitted(false);
            setIsSubmitting(true);
            const form = new FormData(event.currentTarget);
            try {
              await api.login(form.get("email"), form.get("password"));
              setSubmitted(true);
            } catch (requestError) {
              setError(requestError instanceof ApiError ? requestError.message : "Unable to log in right now. Please try again.");
            } finally {
              setIsSubmitting(false);
            }
          }}
        >
          <label htmlFor="email">Email address</label>
          <input id="email" name="email" type="email" placeholder="you@company.com" required />
          <div className="password-label">
            <label htmlFor="password">Password</label>
            <button type="button" onClick={() => setShowPassword((value) => !value)}>
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          <input id="password" name="password" type={showPassword ? "text" : "password"} placeholder="••••••••••" required />
          <a href="#forgot" className="forgot-link">
            Forgot password?
          </a>
          <button className="button button-primary form-submit" type="submit" disabled={isSubmitting}>
            {isSubmitting ? (
              "Logging in…"
            ) : (
              <>
                Log in <span aria-hidden="true">↗</span>
              </>
            )}
          </button>
        </form>
        <div className="or-divider">
          <span>or</span>
        </div>
        <button className="social-button" type="button">
          <span className="google-g">G</span> Continue with Google
        </button>
        <p className="terms">
          By continuing, you agree to our <a href="#terms">Terms</a> and <a href="#privacy">Privacy Policy</a>.
        </p>
      </div>
    </section>
  );
}
