/**
 * Eight Sistemas — estoque.js
 * Formulários, filtros, ordenação de tabela e modal de produto existente.
 */

/* ── Abertura / fechamento de painéis ───────────────────────── */

function fecharTodos() {
  document.querySelectorAll(".form-panel").forEach(el => el.classList.remove("open"));
}

function abrirSomente(id) {
  fecharTodos();
  const painel = document.getElementById(id);
  painel.classList.add("open");
  // Rola até o painel após ele ser renderizado
  requestAnimationFrame(() => {
    painel.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

/* ── Preparar formulários de ação ───────────────────────────── */

function prepararVenda(id, nome) {
  document.getElementById("titulo-venda").innerText = "Vendendo: " + nome;
  document.getElementById("form-venda-final").action = `/vender_produto/${id}`;
  abrirSomente("form-venda");
}

function prepararReposicao(id, nome) {
  document.getElementById("titulo-reposicao").innerText = "Repondo: " + nome;
  document.getElementById("form-reposicao-final").action = `/comprar_produto/${id}`;
  abrirSomente("form-reposicao");
}

function prepararEdicao(id, nome, cat, qtd, preco, custo, fornId) {
  document.getElementById("edit-nome").value  = nome;
  document.getElementById("edit-desc").value  = cat;
  document.getElementById("edit-qtd").value   = qtd;
  document.getElementById("edit-preco").value = preco;
  document.getElementById("edit-custo").value = custo;
  document.getElementById("edit-form").action = `/editar_produto/${id}`;

  const sel = document.getElementById("edit-forn");
  sel.value = fornId && fornId !== "None" && fornId !== "" ? fornId : "";

  abrirSomente("form-ajuste");
}

/* ── Filtros de tabela ──────────────────────────────────────── */

let filtroBaixoAtivo = false;

function aplicarFiltros() {
  const texto = document.getElementById("inputPesquisa").value.toLowerCase();
  let visiveis = 0;

  document.querySelectorAll("tbody tr").forEach(tr => {
    const nomeCell = tr.querySelector("td:nth-child(2)");
    const baixo    = tr.dataset.baixo === "sim";

    const passaTexto = !nomeCell || nomeCell.textContent.toLowerCase().includes(texto);
    const passaBaixo = !filtroBaixoAtivo || baixo;

    const visivel    = passaTexto && passaBaixo;
    tr.style.display = visivel ? "" : "none";
    if (visivel) visiveis++;
  });

  const counter = document.getElementById("counter-produtos");
  if (counter) counter.textContent = `${visiveis} produto(s)`;
}

function filtrarProdutos() { aplicarFiltros(); }

function toggleFiltroBaixo() {
  filtroBaixoAtivo = !filtroBaixoAtivo;
  const btn   = document.getElementById("btn-filtro-baixo");
  const badge = document.getElementById("badge-baixo");

  if (filtroBaixoAtivo) {
    btn.style.borderColor = "var(--red)";
    btn.style.color       = "var(--red)";
    btn.style.background  = "var(--red-dim)";
    const total         = document.querySelectorAll('tbody tr[data-baixo="sim"]').length;
    badge.textContent   = total;
    badge.style.display = "inline";
  } else {
    btn.style.borderColor = "";
    btn.style.color       = "";
    btn.style.background  = "";
    badge.style.display   = "none";
  }
  aplicarFiltros();
}

/* ── Ordenação de tabela ────────────────────────────────────── */

// Estado de ordenação: { col: "id"|"nome"|"quantidade", dir: "asc"|"desc" }
let ordemAtual = { col: null, dir: "asc" };

/**
 * Ordena a tabela pela coluna indicada.
 * Segunda chamada na mesma coluna inverte a direção.
 * @param {"id"|"nome"|"quantidade"} coluna
 */
function ordenarPor(coluna) {
  const tbody = document.querySelector("tbody");
  if (!tbody) return;

  // Alterna direção se já estava ordenado por essa coluna
  if (ordemAtual.col === coluna) {
    ordemAtual.dir = ordemAtual.dir === "asc" ? "desc" : "asc";
  } else {
    ordemAtual.col = coluna;
    ordemAtual.dir = "asc";
  }

  const linhas = Array.from(tbody.querySelectorAll("tr"));

  linhas.sort((a, b) => {
    let valA, valB;

    if (coluna === "id") {
      valA = parseInt(a.dataset.id  || a.querySelector("td:nth-child(1)").textContent.trim(), 10);
      valB = parseInt(b.dataset.id  || b.querySelector("td:nth-child(1)").textContent.trim(), 10);
      return ordemAtual.dir === "asc" ? valA - valB : valB - valA;
    }

    if (coluna === "quantidade") {
      // Remove o emoji ⚠️ antes de parsear
      valA = parseInt(a.querySelector("td:nth-child(4)").textContent.trim(), 10) || 0;
      valB = parseInt(b.querySelector("td:nth-child(4)").textContent.trim(), 10) || 0;
      return ordemAtual.dir === "asc" ? valA - valB : valB - valA;
    }

    if (coluna === "nome") {
      valA = a.querySelector("td:nth-child(2)").textContent.trim().toLowerCase();
      valB = b.querySelector("td:nth-child(2)").textContent.trim().toLowerCase();
      const cmp = valA.localeCompare(valB, "pt-BR");
      return ordemAtual.dir === "asc" ? cmp : -cmp;
    }

    return 0;
  });

  // Reinsere as linhas na nova ordem
  linhas.forEach(tr => tbody.appendChild(tr));

  // Atualiza os ícones nos cabeçalhos
  _atualizarIconesOrdem();
}

function _atualizarIconesOrdem() {
  // Mapa col → id do th
  const mapa = { id: "th-id", nome: "th-nome", quantidade: "th-qtd" };

  Object.entries(mapa).forEach(([col, thId]) => {
    const th   = document.getElementById(thId);
    const icon = th && th.querySelector(".sort-icon");
    if (!icon) return;

    if (ordemAtual.col === col) {
      icon.textContent = ordemAtual.dir === "asc" ? " ↑" : " ↓";
      th.style.color   = "var(--blue)";
    } else {
      icon.textContent = " ↕";
      th.style.color   = "";
    }
  });
}

/* ── Modal produto existente ────────────────────────────────── */

function fecharModalProduto() {
  document.getElementById("modal-produto-existente").style.display = "none";
}

function abrirModalProduto(id, nome, qtd) {
  document.getElementById("modal-msg-produto").innerHTML = `
    O produto <strong>${nome}</strong> já está cadastrado no sistema.<br>
    Deseja adicionar <strong>${qtd}</strong> unidade(s) ao estoque existente?<br>
    <span style="font-size:12px;color:var(--muted2);">
      Os outros campos (preço, categoria, fornecedor) <strong>não serão alterados</strong>.
    </span>`;
  document.getElementById("modal-confirmar-btn").href =
    `/confirmar_adicionar_produto/${id}/${qtd}`;
  document.getElementById("modal-produto-existente").style.display = "flex";
}

/* ── Inicialização ──────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {
  // Confirmação pendente vinda do flash (produto existente)
  const pendente = document.getElementById("confirmacao-pendente");
  if (pendente) {
    const { id, nome, qtd } = pendente.dataset;
    abrirModalProduto(id, nome, qtd);
  }

  // Ativa filtro de estoque baixo se vier da URL ?filtro_baixo=1
  if (new URLSearchParams(window.location.search).get("filtro_baixo") === "1") {
    toggleFiltroBaixo();
  }

  // Inicializa ícones ↕ nos cabeçalhos clicáveis
  _atualizarIconesOrdem();
});
