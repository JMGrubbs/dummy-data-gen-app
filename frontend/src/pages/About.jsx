const Arrow = () => (
  <span aria-hidden="true" className="arrow">
    ↗
  </span>
);

export default function About({ onNavigate }) {
  return (
    <>
      <section className="about-hero shell">
        <div className="section-kicker">OUR STORY</div>
        <h1>
          Good tools get
          <br />
          <span>out of the way.</span>
        </h1>
        <p>Datadrop exists to make the unglamorous parts of building feel effortless — so you can spend your energy on the ideas that matter.</p>
      </section>
      <section className="about-body shell">
        <div className="about-statement">
          <span className="quote-mark">“</span>
          <h2>We believe placeholder data shouldn’t look like placeholder data.</h2>
        </div>
        <div className="about-copy">
          <p>
            Every great product starts with a sketch. But the leap from a sketch to something you can share is often filled with fake names, broken
            states, and empty tables.
          </p>
          <p>
            Datadrop gives builders a quick, thoughtful way to fill that gap. We make realistic synthetic data that lets your product speak for itself
            — long before the backend is ready.
          </p>
        </div>
      </section>
      <section className="values-section">
        <div className="shell">
          <div className="section-kicker">WHAT WE VALUE</div>
          <div className="values-grid">
            <article>
              <span className="value-number">01</span>
              <h3>Useful by default</h3>
              <p>Less configuration, more momentum. Sensible defaults help you get to a good result immediately.</p>
            </article>
            <article>
              <span className="value-number">02</span>
              <h3>Details matter</h3>
              <p>Believability lives in the small things: formats, relationships, and data that tells a coherent story.</p>
            </article>
            <article>
              <span className="value-number">03</span>
              <h3>Built with care</h3>
              <p>Simple on the surface, considered underneath. We make tools we want to use ourselves.</p>
            </article>
          </div>
        </div>
      </section>
      <section className="about-cta shell">
        <h2>
          Ready to make something <span>real?</span>
        </h2>
        <button className="button button-primary" onClick={() => onNavigate("/login")}>
          Start generating <Arrow />
        </button>
      </section>
    </>
  );
}
