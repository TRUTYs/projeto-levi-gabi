/**
 * Eight Sistemas — dashboard.js
 * Gráfico de barras interativo com Chart.js.
 */

document.addEventListener("DOMContentLoaded", () => {
  _renderizarGrafico();
  _animarBarrasMaisVendidos();
});

/* ── Gráfico de Entradas vs Saídas ─────────────────────────── */

function _renderizarGrafico() {
  const canvas = document.getElementById("chart-mov");
  if (!canvas || !window.CHART_DATA) return;

  const { labels, entradas, saidas } = window.CHART_DATA;

  // Paleta de cores do sistema
  const BLUE   = "#3B82F6";
  const PURPLE = "#8B5CF6";
  const GRID   = "rgba(38, 51, 72, 0.8)";   // --border
  const MUTED  = "#7A8FA8";                   // --muted
  const TEXT   = "#E8EFF8";                   // --text
  const CARD   = "#1A2235";                   // --card

  new Chart(canvas, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label:           "Entradas",
          data:            entradas,
          backgroundColor: BLUE + "CC",       // 80% opacidade
          hoverBackgroundColor: BLUE,
          borderRadius:    5,
          borderSkipped:   false,
          barPercentage:   0.6,
          categoryPercentage: 0.7,
        },
        {
          label:           "Saídas",
          data:            saidas,
          backgroundColor: PURPLE + "CC",
          hoverBackgroundColor: PURPLE,
          borderRadius:    5,
          borderSkipped:   false,
          barPercentage:   0.6,
          categoryPercentage: 0.7,
        },
      ],
    },
    options: {
      responsive:          true,
      maintainAspectRatio: false,
      animation: {
        duration: 700,
        easing:   "easeOutQuart",
      },
      plugins: {
        legend: {
          position: "top",
          align:    "start",
          labels: {
            color:       MUTED,
            font:        { size: 11, family: "'DM Sans', sans-serif" },
            boxWidth:    10,
            boxHeight:   10,
            borderRadius: 3,
            useBorderRadius: true,
            padding:     16,
          },
        },
        tooltip: {
          backgroundColor: CARD,
          borderColor:     GRID,
          borderWidth:     1,
          titleColor:      TEXT,
          bodyColor:       MUTED,
          padding:         10,
          cornerRadius:    8,
          displayColors:   true,
          callbacks: {
            label: ctx =>
              ` ${ctx.dataset.label}: ${ctx.parsed.y} unidade(s)`,
          },
        },
      },
      scales: {
        x: {
          grid:   { color: GRID, drawTicks: false },
          border: { display: false },
          ticks:  { color: MUTED, font: { size: 11 }, padding: 6 },
        },
        y: {
          beginAtZero: true,
          grid:        { color: GRID, drawTicks: false },
          border:      { display: false, dash: [4, 4] },
          ticks: {
            color:     MUTED,
            font:      { size: 11 },
            padding:   8,
            precision: 0,
          },
        },
      },
    },
  });
}

/* ── Animação das barras "Mais vendidos" ────────────────────── */

function _animarBarrasMaisVendidos() {
  // Inicia em 0% e expande para o valor real com delay escalonado
  document.querySelectorAll(".prod-fill[data-width]").forEach((el, i) => {
    setTimeout(() => {
      el.style.width = el.dataset.width + "%";
    }, 100 + i * 80);
  });
}
