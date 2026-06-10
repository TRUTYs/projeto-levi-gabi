/**
 * Eight Sistemas — dashboard.js
 * Renderiza o gráfico de barras de entradas vs. saídas.
 * Os dados são injetados pelo template via variáveis globais.
 */

document.addEventListener("DOMContentLoaded", () => {
  const barsEl = document.getElementById("chart-bars");
  if (!barsEl || !window.CHART_DATA) return;

  const { labels, entradas, saidas } = window.CHART_DATA;
  const maxVal = Math.max(...entradas, ...saidas, 1);

  labels.forEach((mes, i) => {
    const hE = Math.max(Math.round((entradas[i] / maxVal) * 100), 3);
    const hS = Math.max(Math.round((saidas[i]   / maxVal) * 100), 3);

    const wrap = document.createElement("div");
    wrap.className = "bar-wrap";
    wrap.innerHTML = `
      <div class="bars">
        <div class="bar entrada" style="height:${hE}%;width:12px"
             title="Entradas ${mes}: ${entradas[i]}"></div>
        <div class="bar saida"  style="height:${hS}%;width:12px"
             title="Saídas ${mes}: ${saidas[i]}"></div>
      </div>
      <div class="bar-lbl">${mes}</div>`;
    barsEl.appendChild(wrap);
  });
});
