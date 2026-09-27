import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

function App() {
  return (
    <main className="shell">
      <p className="eyebrow">PLACEcheck</p>
      <h1>Encontre o imóvel certo.</h1>
      <p className="subtitle">O agregador de imóveis está sendo preparado.</p>
      <div className="search-placeholder">A busca por imóveis estará disponível em breve.</div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
