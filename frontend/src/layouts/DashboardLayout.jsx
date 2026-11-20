function Mark() {
  return (
    <span className="brand-mark" aria-hidden="true">
      <span />
      <span />
      <span />
    </span>
  );
}

function NavIcon({ children }) {
  return <span className="app-nav-icon" aria-hidden="true">{children}</span>;
}

export default function DashboardLayout({ children, currentPath, onNavigate, onLogout, user }) {
  const go = (event, href) => {
    event.preventDefault();
    onNavigate(href);
  };
  const username = user?.username || user?.email || "Your account";

  return (
    <div className="app-shell">
      <aside className="app-sidebar">
        <a className="brand app-brand" href="/dashboard" onClick={(event) => go(event, "/dashboard")}>
          <Mark />
          <span>datadrop</span>
        </a>
        <nav className="app-nav" aria-label="Workspace navigation">
          <a className={currentPath === "/dashboard" ? "active" : ""} aria-current={currentPath === "/dashboard" ? "page" : undefined} href="/dashboard" onClick={(event) => go(event, "/dashboard")}>
            <NavIcon>⌂</NavIcon> Overview
          </a>
          <a className={currentPath.startsWith("/projects") ? "active" : ""} aria-current={currentPath.startsWith("/projects") ? "page" : undefined} href="/projects" onClick={(event) => go(event, "/projects")}>
            <NavIcon>□</NavIcon> Projects
          </a>
        </nav>
        <div className="sidebar-account">
          <div className="account-avatar">{username.charAt(0).toUpperCase()}</div>
          <div>
            <strong>{username}</strong>
            <button type="button" onClick={onLogout}>Log out</button>
          </div>
        </div>
      </aside>
      <div className="app-stage">
        <header className="app-mobile-header">
          <a className="brand" href="/dashboard" onClick={(event) => go(event, "/dashboard")}>
            <Mark /> <span>datadrop</span>
          </a>
          <nav aria-label="Mobile workspace navigation">
            <a href="/dashboard" onClick={(event) => go(event, "/dashboard")}>Overview</a>
            <a href="/projects" onClick={(event) => go(event, "/projects")}>Projects</a>
          </nav>
        </header>
        <main className="app-content">{children}</main>
      </div>
    </div>
  );
}
