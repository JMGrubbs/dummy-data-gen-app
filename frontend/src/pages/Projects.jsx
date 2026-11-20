import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from "../services/api.js";

function formatDate(value) {
  if (!value) return "Date unavailable";
  const date = new Date(value);
  return Number.isNaN(date.getTime())
    ? value
    : new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric", year: "numeric" }).format(date);
}

export default function Projects({ onNavigate, onUnauthorized }) {
  const [projects, setProjects] = useState([]);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState(null);

  const loadProjects = useCallback(async () => {
    setStatus("loading");
    setError("");
    try {
      const payload = await api.projects.list();
      setProjects(payload?.projects || []);
      setStatus("ready");
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 401) {
        onUnauthorized();
        return;
      }
      setError(requestError instanceof ApiError ? requestError.message : "We could not load your projects.");
      setStatus("error");
    }
  }, [onUnauthorized]);

  useEffect(() => { loadProjects(); }, [loadProjects]);

  const removeProject = async (project) => {
    if (!window.confirm(`Delete “${project.name}”? This cannot be undone.`)) return;
    setDeletingId(project.id);
    setError("");
    try {
      await api.projects.remove(project.id);
      setProjects((current) => current.filter((item) => item.id !== project.id));
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 401) {
        onUnauthorized();
        return;
      }
      setError(requestError instanceof ApiError ? requestError.message : "We could not delete that project.");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="workspace-page">
      <div className="workspace-heading">
        <div><span className="eyebrow">PROJECTS</span><h1>Everything you’re building.</h1><p>Create, rename, and organize your Datadrop projects.</p></div>
        <button className="button button-primary" type="button" onClick={() => onNavigate("/projects/new")}>New project <span aria-hidden="true">＋</span></button>
      </div>

      {error && <div className="workspace-alert error-message" role="alert">{error}</div>}
      {status === "loading" && <div className="workspace-state" role="status">Loading projects…</div>}
      {status === "error" && <button className="button secondary-button" type="button" onClick={loadProjects}>Try again</button>}
      {status === "ready" && projects.length === 0 && (
        <div className="workspace-panel empty-state large-empty">
          <div className="empty-icon" aria-hidden="true">□</div><h2>No projects yet</h2><p>Create your first project to start organizing generated data.</p>
          <button className="button button-primary" type="button" onClick={() => onNavigate("/projects/new")}>Create your first project</button>
        </div>
      )}
      {status === "ready" && projects.length > 0 && (
        <section className="workspace-panel projects-panel">
          <div className="panel-heading"><div><span className="eyebrow">ALL PROJECTS</span><h2>{projects.length} {projects.length === 1 ? "project" : "projects"}</h2></div></div>
          <div className="project-list">
            {projects.map((project) => (
              <article className="project-row" key={project.id}>
                <div className="project-glyph" aria-hidden="true">{project.name.charAt(0).toUpperCase()}</div>
                <div className="project-main"><strong>{project.name}</strong><span>Created {formatDate(project.created_at)}</span></div>
                <div className="project-actions">
                  <button className="row-action" type="button" onClick={() => onNavigate(`/projects/${project.id}/edit`)}>Edit</button>
                  <button className="row-action danger-action" type="button" disabled={deletingId === project.id} onClick={() => removeProject(project)}>{deletingId === project.id ? "Deleting…" : "Delete"}</button>
                </div>
              </article>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
