import { useEffect, useState } from "react";
import { api, ApiError } from "../services/api.js";

export default function ProjectEditor({ projectId, onNavigate, onUnauthorized }) {
  const isEditing = Boolean(projectId);
  const [name, setName] = useState("");
  const [status, setStatus] = useState(isEditing ? "loading" : "ready");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!isEditing) return undefined;
    let active = true;
    api.projects.get(projectId)
      .then((payload) => {
        if (!active) return;
        const project = payload?.projects?.[0];
        if (!project) {
          setError("That project could not be found.");
          setStatus("error");
          return;
        }
        setName(project.name);
        setStatus("ready");
      })
      .catch((requestError) => {
        if (!active) return;
        if (requestError instanceof ApiError && requestError.status === 401) {
          onUnauthorized();
          return;
        }
        setError(requestError instanceof ApiError ? requestError.message : "We could not load that project.");
        setStatus("error");
      });
    return () => { active = false; };
  }, [isEditing, onUnauthorized, projectId]);

  const saveProject = async (event) => {
    event.preventDefault();
    const cleanName = name.trim();
    if (!cleanName) {
      setError("Enter a project name.");
      return;
    }
    setStatus("saving");
    setError("");
    try {
      if (isEditing) await api.projects.update(projectId, cleanName);
      else await api.projects.create(cleanName);
      onNavigate("/projects");
    } catch (requestError) {
      if (requestError instanceof ApiError && requestError.status === 401) {
        onUnauthorized();
        return;
      }
      setError(requestError instanceof ApiError ? requestError.message : "We could not save that project.");
      setStatus("ready");
    }
  };

  return (
    <div className="workspace-page editor-page">
      <button className="back-button" type="button" onClick={() => onNavigate("/projects")}><span aria-hidden="true">←</span> Back to projects</button>
      <div className="workspace-heading editor-heading">
        <div><span className="eyebrow">{isEditing ? "EDIT PROJECT" : "NEW PROJECT"}</span><h1>{isEditing ? "Give it a better name." : "Start something new."}</h1><p>{isEditing ? "Update the project name without changing its history." : "Create a home for the data and workflows you’re building."}</p></div>
      </div>

      {status === "loading" && <div className="workspace-state" role="status">Loading project…</div>}
      {status === "error" && <div className="workspace-state error-message" role="alert">{error}</div>}
      {(status === "ready" || status === "saving") && (
        <form className="project-form workspace-panel" onSubmit={saveProject}>
          {error && <div className="error-message" role="alert">{error}</div>}
          <label htmlFor="project-name">Project name</label>
          <input id="project-name" name="name" value={name} onChange={(event) => setName(event.target.value)} autoFocus maxLength="120" placeholder="e.g. Customer portal demo" required />
          <p className="field-help">Choose a short name you’ll recognize in your workspace.</p>
          <div className="form-actions">
            <button className="button secondary-button" type="button" onClick={() => onNavigate("/projects")}>Cancel</button>
            <button className="button button-primary" type="submit" disabled={status === "saving"}>{status === "saving" ? "Saving…" : isEditing ? "Save changes" : "Create project"}</button>
          </div>
        </form>
      )}
    </div>
  );
}
