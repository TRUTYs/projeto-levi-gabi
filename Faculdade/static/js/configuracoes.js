/**
 * Eight Sistemas — configuracoes.js
 * Controle dos formulários e confirmações da página de configurações.
 */

function fecharTodos() {
  document.querySelectorAll(".form-panel").forEach(el => el.classList.remove("open"));
}

function abrirSomente(id) {
  fecharTodos();
  const painel = document.getElementById(id);
  painel.classList.add("open");
  requestAnimationFrame(() => painel.scrollIntoView({ behavior: "smooth", block: "start" }));
}

function prepararEdicao(id, nome, email, tipo) {
  document.getElementById("edit-nome").value  = nome;
  document.getElementById("edit-email").value = email;
  document.getElementById("edit-tipo").value  = tipo;
  document.getElementById("form-editar-action").action = `/configuracoes/editar/${id}`;
  abrirSomente("form-editar-usuario");
}

function confirmarExclusao(id, nome) {
  if (confirm(`Excluir o usuário "${nome}"?\n\nEsta ação não pode ser desfeita.`)) {
    window.location.href = `/configuracoes/excluir/${id}`;
  }
}
