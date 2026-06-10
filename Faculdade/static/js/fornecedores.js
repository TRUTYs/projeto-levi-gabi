/**
 * Eight Sistemas — fornecedores.js
 * Controle dos formulários de cadastro/edição e filtro da tabela.
 */

function abrirCadastro() {
  document.getElementById("form-editar-forn").classList.remove("open");
  document.getElementById("form-novo-forn").classList.toggle("open");
  window.scrollTo({ top: 0, behavior: "smooth" });
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
  document.getElementById("form-editar-forn").classList.add("open");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function confirmarExclusao(id, nome) {
  if (confirm(`Excluir "${nome}"?\n\nOs produtos vinculados ficarão sem fornecedor.`)) {
    window.location.href = `/excluir_fornecedor/${id}`;
  }
}

function filtrarFornecedores() {
  const filtro = document.getElementById("inputPesquisaForn").value.toLowerCase();
  document.querySelectorAll("tbody tr").forEach((tr) => {
    const nome = tr.querySelector("td:nth-child(2)");
    if (nome)
      tr.style.display = nome.textContent.toLowerCase().includes(filtro) ? "" : "none";
  });
}
