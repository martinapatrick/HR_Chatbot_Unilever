const toggle = document.getElementById("chat-toggle");
const panel = document.getElementById("chat-panel");
const closeBtn = document.getElementById("chat-close");
const messages = document.getElementById("chat-messages");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");

function getSessionId() {
  let id = null;
  try { id = localStorage.getItem("hr_session"); } catch (e) {}
  if (!id) {
    id = crypto.randomUUID();
    try { localStorage.setItem("hr_session", id); } catch (e) {}
  }
  return id;
}
const sessionId = getSessionId();

function addMessage(text, who) {
  const div = document.createElement("div");
  div.className = "msg " + who;
  div.textContent = text;
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

toggle.addEventListener("click", () => {
  panel.hidden = !panel.hidden;
  if (!panel.hidden && !messages.children.length) {
    addMessage("Hi! I'm the Unilever HR Assistant. Ask me about our HR policies.", "bot");
  }
  if (!panel.hidden) input.focus();
});
closeBtn.addEventListener("click", () => { panel.hidden = true; });

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, "user");
  input.value = "";
  const btn = form.querySelector("button");
  btn.disabled = true;
  const typing = addMessage("Typing...", "bot typing");
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message: text }),
    });
    const data = await res.json();
    typing.className = "msg bot";
    typing.textContent = data.reply || "Sorry, something went wrong.";
  } catch (err) {
    typing.className = "msg bot";
    typing.textContent = "Sorry, I couldn't reach the server.";
  }
  btn.disabled = false;
  messages.scrollTop = messages.scrollHeight;
});
