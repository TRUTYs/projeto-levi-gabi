/**
 * Eight Sistemas — estoque.js
 * Controle dos formulários de produto, filtros e modal de confirmação.
 */

/* ── Abertura / fechamento de painéis ───────────────────────── */

function fecharTodos() {
  document.querySelectorAll(".form-panel").forEach((el) =>
    el.classList.remove("open")
  );
}

function abrirSomente(id) {
  fecharTodos();
  document.getElementById(id).classList.add("open");
  window.scrollTo({ top: 0, behavior: "smooth" });
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
  sel.value =
    fornId && fornId !== "None" && fornId !== "" ? fornId : "";

  abrirSomente("form-ajuste");
}

/* ── Filtros de tabela ──────────────────────────────────────── */

let filtroBaixoAtivo = false;

function aplicarFiltros() {
  const texto   = document.getElementById("inputPesquisa").value.toLowerCase();
  let   visiveis = 0;

  document.querySelectorAll("tbody tr").forEach((tr) => {
    const nomeCell = tr.querySelector("td:nth-child(2)");
    const baixo    = tr.dataset.baixo === "sim";

    const passaTexto = !nomeCell || nomeCell.textContent.toLowerCase().includes(texto);
    const passaBaixo = !filtroBaixoAtivo || baixo;

    const visivel   = passaTexto && passaBaixo;
    tr.style.display = visivel ? "" : "none";
    if (visivel) visiveis++;
  });

  const counter = document.getElementById("counter-produtos");
  if (counter) counter.textContent = `${visiveis} produto(s)`;
}

function filtrarProdutos() {
  aplicarFiltros();
}

function toggleFiltroBaixo() {
  filtroBaixoAtivo = !filtroBaixoAtivo;
  const btn   = document.getElementById("btn-filtro-baixo");
  const badge = document.getElementById("badge-baixo");

  if (filtroBaixoAtivo) {
    btn.style.borderColor = "var(--red)";
    btn.style.color       = "var(--red)";
    btn.style.background  = "var(--red-dim)";
    const total       = document.querySelectorAll('tbody tr[data-baixo="sim"]').length;
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
});
