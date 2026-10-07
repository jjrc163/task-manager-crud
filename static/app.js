const listEl = document.getElementById("list");
const emptyEl = document.getElementById("empty");
const formEl = document.getElementById("new-task");
const titleEl = document.getElementById("title");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
}

function render(tasks) {
  listEl.innerHTML = "";
  emptyEl.hidden = tasks.length > 0;

  for (const task of tasks) {
    const li = document.createElement("li");
    li.className = "item" + (task.done ? " done" : "");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.done;
    checkbox.addEventListener("change", async () => {
      await api(`/api/tasks/${task.id}`, {
        method: "PATCH",
        body: JSON.stringify({ done: checkbox.checked }),
      });
      refresh();
    });

    const span = document.createElement("span");
    span.className = "title";
    span.textContent = task.title;

    const del = document.createElement("button");
    del.className = "delete";
    del.textContent = "✕";
    del.title = "Delete";
    del.addEventListener("click", async () => {
      await api(`/api/tasks/${task.id}`, { method: "DELETE" });
      refresh();
    });

    li.append(checkbox, span, del);
    listEl.append(li);
  }
}

async function refresh() {
  try {
    render(await api("/api/tasks"));
  } catch (error) {
    console.error(error);
  }
}

formEl.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = titleEl.value.trim();
  if (!title) return;
  await api("/api/tasks", { method: "POST", body: JSON.stringify({ title }) });
  titleEl.value = "";
  refresh();
});

refresh();