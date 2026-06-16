/**
 * Eight Sistemas — fornecedores.js
 * Formulários, filtro e ordenação da tabela de fornecedores.
 */

/* ── Abertura / fechamento de painéis ───────────────────────── */

function abrirCadastro() {
  document.getElementById("form-editar-forn").classList.remove("open");
  const painel = document.getElementById("form-novo-forn");
  painel.classList.toggle("open");
  if (painel.classList.contains("open")) {
    requestAnimationFrame(() => painel.scrollIntoView({ behavior: "smooth", block: "start" }));
  }
}

function fecharEdicao() {
  document.getElementById("form-editar-forn").classList.remove("open");
  document.getElementById("form-novo-forn").classList.remove("open");
}

function prepararEdicao(id, nome, contato, email, cnpj, local) {
  document.getElementById("form-novo-forn").classList.remove("open");
  document.getElementById("edit-nome-forn").value    = nome;
  document.getElementById("edit-contato-forn").value = contato;
  document.getElementById("edit-email-forn").value   = email;
  document.getElementById("edit-cnpj-forn").value    = cnpj;
  document.getElementById("edit-local-forn").value   = local;
  document.getElementById("edit-forn-form").action   = `/editar_fornecedor/${id}`;

  const painel = document.getElementById("form-editar-forn");
  painel.classList.add("open");
  requestAnimationFrame(() => painel.scrollIntoView({ behavior: "smooth", block: "start" }));
}

function confirmarExclusao(id, nome) {
  if (confirm(`Excluir "${nome}"?\n\nOs produtos vinculados ficarão sem fornecedor.`)) {
    window.location.href = `/excluir_fornecedor/${id}`;
  }
}

/* ── Filtro de pesquisa ─────────────────────────────────────── */

function filtrarFornecedores() {
  const filtro = document.getElementById("inputPesquisaForn").value.toLowerCase();
  document.querySelectorAll("tbody tr").forEach(tr => {
    const nome = tr.querySelector("td:nth-child(2)");
    if (nome)
      tr.style.display = nome.textContent.toLowerCase().includes(filtro) ? "" : "none";
  });
}

/* ── Ordenação de tabela ────────────────────────────────────── */

let ordemAtual = { col: null, dir: "asc" };

/**
 * Ordena a tabela pela coluna indicada.
 * Segunda chamada na mesma coluna inverte a direção.
 * @param {"id"|"nome"} coluna
 */
function ordenarPor(coluna) {
  const tbody = document.querySelector("tbody");
  if (!tbody) return;

  if (ordemAtual.col === coluna) {
    ordemAtual.dir = ordemAtual.dir === "asc" ? "desc" : "asc";
  } else {
    ordemAtual.col = coluna;
    ordemAtual.dir = "asc";
  }

  const linhas = Array.from(tbody.querySelectorAll("tr"));

  linhas.sort((a, b) => {
    if (coluna === "id") {
      const valA = parseInt(a.querySelector("td:nth-child(1)").textContent.trim(), 10);
      const valB = parseInt(b.querySelector("td:nth-child(1)").textContent.trim(), 10);
      return ordemAtual.dir === "asc" ? valA - valB : valB - valA;
    }

    if (coluna === "nome") {
      const valA = a.querySelector("td:nth-child(2)").textContent.trim().toLowerCase();
      const valB = b.querySelector("td:nth-child(2)").textContent.trim().toLowerCase();
      const cmp  = valA.localeCompare(valB, "pt-BR");
      return ordemAtual.dir === "asc" ? cmp : -cmp;
    }

    return 0;
  });

  linhas.forEach(tr => tbody.appendChild(tr));
  _atualizarIconesOrdem();
}

function _atualizarIconesOrdem() {
  const mapa = { id: "th-id", nome: "th-nome" };

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

document.addEventListener("DOMContentLoaded", () => _atualizarIconesOrdem());
