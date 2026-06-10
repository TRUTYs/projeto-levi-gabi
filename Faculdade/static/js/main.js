/**
 * Eight Sistemas — main.js
 * Utilitários globais: flash auto-dismiss, máscaras de input.
 */

/* ── Flash auto-dismiss ─────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", () => {
  const flashes = document.querySelectorAll(".flash-msg");
  if (!flashes.length) return;

  setTimeout(() => {
    flashes.forEach((el) => {
      el.style.transition = "opacity .4s";
      el.style.opacity    = "0";
      setTimeout(() => el.remove(), 400);
    });
  }, 5000);
});

/* ── Máscaras de input ──────────────────────────────────────── */

/**
 * Aplica máscara de telefone: (00) 00000-0000
 * @param {HTMLInputElement} input
 */
function maskTelefone(input) {
  let v = input.value.replace(/\D/g, "");
  v =
    v.length <= 10
      ? v.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4})(\d)/, "$1-$2")
      : v.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d)/, "$1-$2");
  input.value = v;
}

/**
 * Aplica máscara de CNPJ: 00.000.000/0000-00
 * @param {HTMLInputElement} input
 */
function maskCNPJ(input) {
  let v = input.value.replace(/\D/g, "");
  v = v
    .replace(/^(\d{2})(\d)/, "$1.$2")
    .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
    .replace(/\.(\d{3})(\d)/, ".$1/$2")
    .replace(/(\d{4})(\d)/, "$1-$2");
  input.value = v;
}
