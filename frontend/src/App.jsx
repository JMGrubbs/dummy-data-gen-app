import { useEffect, useState } from "react";
import Main from "./layouts/Main.jsx";
import Home from "./pages/Home.jsx";
import About from "./pages/About.jsx";
import Login from "./pages/Login.jsx";

function pageForPath(pathname) {
  if (pathname === "/about") return "about";
  if (pathname === "/login") return "login";
  return "home";
}

export default function App() {
  const [page, setPage] = useState(() => pageForPath(window.location.pathname));
  useEffect(() => {
    const handlePopState = () => setPage(pageForPath(window.location.pathname));
    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);
  const navigate = (href) => {
    if (href === window.location.pathname) return;
    window.history.pushState({}, "", href);
    setPage(pageForPath(href));
    window.scrollTo({ top: 0, behavior: "smooth" });
  };
  return <Main currentPage={page} onNavigate={navigate}>{page === "about" && <About onNavigate={navigate} />}{page === "login" && <Login onNavigate={navigate} />}{page === "home" && <Home onNavigate={navigate} />}</Main>;
}
