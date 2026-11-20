import { useEffect, useState } from "react";
import { api, ApiError } from "../services/api.js";

function formatDate(value) {
  if (!value) return "Date unavailable";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(date);
}

export default function Dashboard({ onNavigate, onUnauthorized }) {
  const [projects, setProjects] = useState([]);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");

  useEffect(() => {
    let active = true;
    api.projects.list()
      .then((payload) => {
        if (!active) return;
        setProjects(payload?.projects || []);
        setStatus("ready");
      })
      .catch((requestError) => {
        if (!active) return;
        if (requestError instanceof ApiError && requestError.status === 401) {
          onUnauthorized();
          return;
        }
        setError(requestError instanceof ApiError ? requestError.message : "We could not load your workspace.");
        setStatus("error");
      });
    return () => { active = false; };
  }, [onUnauthorized]);

  const recentProjects = [...projects]
    .sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0))
    .slice(0, 4);

  return (
    <div className="workspace-page">
      <div className="workspace-heading">
        <div>
          <span className="eyebrow">WORKSPACE OVERVIEW</span>
          <h1>Good to see you.</h1>
          <p>Keep track of your projects and jump back into building.</p>
        </div>
        <button className="button button-primary" type="button" onClick={() => onNavigate("/projects/new")}>New project <span aria-hidden="true">＋</span></button>
      </div>

      {status === "loading" && <div className="workspace-state" role="status">Loading your workspace…</div>}
      {status === "error" && <div className="workspace-state error-message" role="alert">{error}</div>}

      {status === "ready" && (
        <>
          <section className="metric-grid" aria-label="Project summary">
            <article className="metric-card accent-card">
              <span>Total projects</span>
              <strong>{projects.length}</strong>
              <p>Projects in your workspace</p>
            </article>
            <article className="metric-card">
              <span>Latest project</span>
              <strong className="metric-project-name">{recentProjects[0]?.name || "Nothing yet"}</strong>
              <p>{recentProjects[0] ? `Created ${formatDate(recentProjects[0].created_at)}` : "Create your first project to get started"}</p>
            </article>
          </section>

          <section className="workspace-panel">
            <div className="panel-heading">
              <div><span className="eyebrow">RECENT WORK</span><h2>Your projects</h2></div>
              <button className="quiet-button" type="button" onClick={() => onNavigate("/projects")}>View all <span aria-hidden="true">→</span></button>
            </div>
            {recentProjects.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon" aria-hidden="true">✦</div>
                <h3>Start with a project</h3>
                <p>Projects give your generated data a place to live and stay organized.</p>
                <button className="button button-primary" type="button" onClick={() => onNavigate("/projects/new")}>Create a project</button>
              </div>
            ) : (
              <div className="project-list compact-list">
                {recentProjects.map((project) => (
                  <article className="project-row" key={project.id}>
                    <div className="project-glyph" aria-hidden="true">{project.name.charAt(0).toUpperCase()}</div>
                    <div className="project-main"><strong>{project.name}</strong><span>Created {formatDate(project.created_at)}</span></div>
                    <button className="row-action" type="button" onClick={() => onNavigate(`/projects/${project.id}/edit`)}>Edit <span aria-hidden="true">→</span></button>
                  </article>
                ))}
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
