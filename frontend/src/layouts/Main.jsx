function Mark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <span />
      <span />
      <span />
    </span>
  );
}

export default function Main({ children, currentPage, onNavigate }) {
  const link = (event, href) => {
    event.preventDefault();
    onNavigate(href);
  };
  return (
    <div className="min-h-screen bg-ink text-white">
      <header className="site-header">
        <div className="shell nav-inner">
          <a href="/" className="brand" onClick={(event) => link(event, "/")}>
            <Mark />
            <span>datadrop</span>
          </a>
          <nav className="desktop-nav" aria-label="Primary navigation">
            <a className={currentPage === "home" ? "nav-link active" : "nav-link"} href="/" onClick={(event) => link(event, "/")}>
              Home
            </a>
            <a className={currentPage === "about" ? "nav-link active" : "nav-link"} href="/about" onClick={(event) => link(event, "/about")}>
              About
            </a>
          </nav>
          <a className="nav-login" href="/login" onClick={(event) => link(event, "/login")}>
            Log in <span aria-hidden="true">↗</span>
          </a>
        </div>
      </header>
      <main>{children}</main>
      <footer className="site-footer">
        <div className="shell footer-inner">
          <a href="/" className="brand footer-brand" onClick={(event) => link(event, "/")}>
            <Mark />
            <span>datadrop</span>
          </a>
          <p>Made for builders who need better data.</p>
          <p className="footer-copy">© 2024 Datadrop. Simple, safe, synthetic.</p>
        </div>
      </footer>
    </div>
  );
}
