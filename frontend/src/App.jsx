import { useCallback, useEffect, useState } from "react";
import Main from "./layouts/Main.jsx";
import DashboardLayout from "./layouts/DashboardLayout.jsx";
import Home from "./pages/Home.jsx";
import About from "./pages/About.jsx";
import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Projects from "./pages/Projects.jsx";
import ProjectEditor from "./pages/ProjectEditor.jsx";
import { api, ApiError } from "./services/api.js";

function routeForPath(pathname) {
  if (pathname === "/about") return { page: "about", protected: false };
  if (pathname === "/login") return { page: "login", protected: false };
  if (pathname === "/dashboard") return { page: "dashboard", protected: true };
  if (pathname === "/projects") return { page: "projects", protected: true };
  if (pathname === "/projects/new") return { page: "project-new", protected: true };
  const editMatch = pathname.match(/^\/projects\/([^/]+)\/edit$/);
  if (editMatch) return { page: "project-edit", projectId: decodeURIComponent(editMatch[1]), protected: true };
  return { page: "home", protected: false };
}

export default function App() {
  const [pathname, setPathname] = useState(window.location.pathname);
  const [user, setUser] = useState(null);
  const [authStatus, setAuthStatus] = useState("unknown");
  const [authError, setAuthError] = useState("");
  const route = routeForPath(pathname);

  useEffect(() => {
    const handlePopState = () => setPathname(window.location.pathname);
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const navigate = useCallback((href, { replace = false } = {}) => {
    if (href === window.location.pathname) return;
    window.history[replace ? "replaceState" : "pushState"]({}, "", href);
    setPathname(href);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, []);

  const clearSession = useCallback(() => {
    setUser(null);
    setAuthStatus("unauthenticated");
    navigate("/login", { replace: true });
  }, [navigate]);

  useEffect(() => {
    if (!route.protected || authStatus !== "unknown") return;
    let active = true;
    api.me()
      .then((currentUser) => {
        if (!active) return;
        setUser(currentUser);
        setAuthError("");
        setAuthStatus("authenticated");
      })
      .catch((requestError) => {
        if (!active) return;
        if (requestError instanceof ApiError && (requestError.status === 401 || requestError.status === 403)) {
          clearSession();
          return;
        }
        setAuthError("We could not reach your workspace. Check your connection and try again.");
        setAuthStatus("error");
      });
    return () => { active = false; };
  }, [authStatus, clearSession, route.protected]);

  useEffect(() => {
    if (route.protected && authStatus === "unauthenticated") {
      navigate("/login", { replace: true });
    }
  }, [authStatus, navigate, route.protected]);

  const handleLogin = (currentUser) => {
    setUser(currentUser);
    setAuthStatus("authenticated");
    navigate("/dashboard");
  };

  const handleLogout = async () => {
    try {
      await api.logout();
    } catch {
      // The local session should still be cleared when the server is unavailable.
    } finally {
      clearSession();
    }
  };

  if (route.protected && authStatus === "error") {
    return (
      <div className="full-page-loader auth-failure" role="alert">
        <div>
          <span className="eyebrow">CONNECTION ERROR</span>
          <h1>Your workspace didn’t open.</h1>
          <p>{authError}</p>
          <button className="button button-primary" type="button" onClick={() => setAuthStatus("unknown")}>Try again</button>
        </div>
      </div>
    );
  }

  if (route.protected && authStatus !== "authenticated") {
    return <div className="full-page-loader" role="status">Opening your workspace…</div>;
  }

  if (route.protected && authStatus === "authenticated") {
    return (
      <DashboardLayout currentPath={pathname} onNavigate={navigate} onLogout={handleLogout} user={user}>
        {route.page === "dashboard" && <Dashboard onNavigate={navigate} onUnauthorized={clearSession} />}
        {route.page === "projects" && <Projects onNavigate={navigate} onUnauthorized={clearSession} />}
        {route.page === "project-new" && <ProjectEditor onNavigate={navigate} onUnauthorized={clearSession} />}
        {route.page === "project-edit" && <ProjectEditor projectId={route.projectId} onNavigate={navigate} onUnauthorized={clearSession} />}
      </DashboardLayout>
    );
  }

  return (
    <Main currentPage={route.page} onNavigate={navigate}>
      {route.page === "about" && <About onNavigate={navigate} />}
      {route.page === "login" && <Login onNavigate={navigate} onAuthenticated={handleLogin} />}
      {route.page === "home" && <Home onNavigate={navigate} />}
    </Main>
  );
}
