const Arrow = () => (
  <span aria-hidden="true" className="arrow">
    ↗
  </span>
);

function DataPreview() {
  const rows = [
    ["Alex Morgan", "alex@example.com", "active"],
    ["Jamie Chen", "jamie@example.com", "active"],
    ["Sam Rivera", "sam@example.com", "pending"],
    ["Taylor Brooks", "taylor@example.com", "active"],
  ];
  return (
    <div className="preview-card" aria-label="Example generated dataset">
      <div className="preview-top">
        <div className="window-dots">
          <i />
          <i />
          <i />
        </div>
        <span>users.json</span>
        <span className="preview-more">•••</span>
      </div>
      <div className="preview-head">
        <span>name</span>
        <span>email</span>
        <span>status</span>
      </div>
      {rows.map(([name, email, status]) => (
        <div className="preview-row" key={email}>
          <span>{name}</span>
          <span>{email}</span>
          <b className={status}>{status}</b>
        </div>
      ))}
      <div className="preview-foot">
        <span>
          <span className="green-dot" /> 4 records generated
        </span>
        <span>
          JSON <em>⌄</em>
        </span>
      </div>
    </div>
  );
}

export default function Home({ onNavigate }) {
  return (
    <>
      <section className="hero-section shell">
        <div className="hero-copy">
          <div className="pill">
            <span className="spark">✦</span> A calmer way to build
          </div>
          <h1>
            Data that feels <span>real.</span>
            <br />
            Made in seconds.
          </h1>
          <p className="hero-subtitle">Generate realistic, production-ready dummy data without the spreadsheets, scripts, or guesswork.</p>
          <div className="hero-actions">
            <button className="button button-primary" onClick={() => onNavigate("/login")}>
              Start generating <Arrow />
            </button>
            <a className="text-link" href="#how-it-works">
              See how it works <Arrow />
            </a>
          </div>
          <div className="trust-row">
            <div className="avatar-stack">
              <i>J</i>
              <i>M</i>
              <i>A</i>
              <i>+</i>
            </div>
            <span>Loved by 2,000+ builders</span>
          </div>
        </div>
        <div className="hero-visual">
          <div className="visual-glow" />
          <DataPreview />
          <div className="float-chip chip-top">
            ✦ <span>Smart schemas</span>
          </div>
          <div className="float-chip chip-bottom">
            <span className="green-dot" /> Ready to export
          </div>
        </div>
      </section>
      <section className="logo-strip">
        <div className="shell logo-inner">
          <span>TRUSTED BY TEAMS AT</span>
          <strong>northstar</strong>
          <strong>
            arc<span>°</span>
          </strong>
          <strong className="mono-logo">
            BLOCK<span>LAB</span>
          </strong>
          <strong className="serif-logo">Morrow</strong>
        </div>
      </section>
      <section className="feature-section shell" id="how-it-works">
        <div className="section-kicker">WHY DATADROP</div>
        <h2>
          Less setup. <span>More making.</span>
        </h2>
        <p className="section-intro">Everything you need to move from an empty database to a believable product experience.</p>
        <div className="feature-grid">
          <article className="feature-card">
            <div className="feature-icon purple">✣</div>
            <h3>Feels like the real thing</h3>
            <p>Thoughtfully generated names, addresses, and relationships that make your prototypes feel alive.</p>
            <a
              href="/about"
              onClick={(event) => {
                event.preventDefault();
                onNavigate("/about");
              }}
            >
              Learn more <Arrow />
            </a>
          </article>
          <article className="feature-card">
            <div className="feature-icon mint">⌁</div>
            <h3>Your format, your way</h3>
            <p>Shape the schema, choose the format, and export exactly what your stack expects.</p>
            <a
              href="/login"
              onClick={(event) => {
                event.preventDefault();
                onNavigate("/login");
              }}
            >
              Try it free <Arrow />
            </a>
          </article>
          <article className="feature-card">
            <div className="feature-icon yellow">↯</div>
            <h3>Ready when you are</h3>
            <p>Skip the setup and get useful data in seconds. No credit card, no long onboarding.</p>
            <a
              href="/login"
              onClick={(event) => {
                event.preventDefault();
                onNavigate("/login");
              }}
            >
              Get started <Arrow />
            </a>
          </article>
        </div>
      </section>
      <section className="cta-section shell">
        <div className="cta-card">
          <div>
            <div className="section-kicker">YOUR NEXT PROJECT</div>
            <h2>
              Make your demo <span>believable.</span>
            </h2>
          </div>
          <button className="button button-light" onClick={() => onNavigate("/login")}>
            Create your first dataset <Arrow />
          </button>
        </div>
      </section>
    </>
  );
}
