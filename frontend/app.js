const state = { history: [], run: null, statusFilter: "all", category: "all" };

const $ = (selector) => document.querySelector(selector);
const articlesEl = $("#articles");
const template = $("#articleTemplate");
const runSelect = $("#runSelect");
const categorySelect = $("#categorySelect");

function formatDate(value) {
  if (!value) return "No run yet";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Asia/Kolkata",
  }).format(date);
}

function contentType(article) {
  return article.content_type === "technology" ? "technology" : "industry";
}

function reviewKey(article) {
  return "ev-research:" + (article.id || article.source_url) + ":reviewed";
}

function isReviewed(article) {
  return localStorage.getItem(reviewKey(article)) === "done";
}

function setReviewed(article) {
  const key = reviewKey(article);
  if (isReviewed(article)) localStorage.removeItem(key);
  else localStorage.setItem(key, "done");
  renderArticles();
}

function updateCategoryOptions() {
  const current = state.category;
  const categories = [...new Set((state.run?.articles || []).map((a) => a.category || "Other"))].sort();
  categorySelect.replaceChildren(new Option("All categories", "all"));
  for (const category of categories) categorySelect.append(new Option(category, category));
  if (categories.includes(current)) categorySelect.value = current;
  else state.category = "all";
}

function renderSummary() {
  const articles = state.run?.articles || [];
  $("#articleCount").textContent = articles.length;
  $("#techCount").textContent = articles.filter((a) => contentType(a) === "technology").length;
  $("#industryCount").textContent = articles.filter((a) => contentType(a) === "industry").length;
  $("#providerName").textContent = state.run?.ai_provider || "unknown";
  $("#generatedAt").textContent = "Generated " + formatDate(state.run?.generated_at);
  updateCategoryOptions();
}

function copyText(article) {
  const concepts = (article.key_concepts || []).join(", ");
  const questions = (article.interview_questions || [])
    .map((q, i) => String(i + 1) + ". " + q)
    .join("\n");

  const parts = [
    article.headline,
    "",
    article.summary,
    "",
  ];

  if (contentType(article) === "technology") {
    parts.push(
      "Current stack:",
      article.current_stack || "",
      "",
      "Relationship:",
      article.relationship || "",
      "",
      "Comparison:",
      article.comparison_note || "",
      "",
      "Limitations:",
      article.limitations || "",
      "",
      "Try it:",
      article.practical_example || "",
      ""
    );
  }

  parts.push(
    "Why it matters:",
    article.why_it_matters || "",
    "",
    "Key concepts: " + concepts,
    "",
    "Interview questions:",
    questions,
    "",
    "Next step: " + (article.next_step || ""),
    "",
    "Source: " + (article.source_url || "")
  );

  return parts.join("\n");
}

function renderArticles() {
  articlesEl.replaceChildren();
  let visible = 0;

  for (const article of state.run?.articles || []) {
    const reviewed = isReviewed(article);
    if (state.statusFilter === "todo" && reviewed) continue;
    if (state.statusFilter === "done" && !reviewed) continue;
    if (state.category !== "all" && article.category !== state.category) continue;

    visible += 1;
    const type = contentType(article);
    const card = template.content.firstElementChild.cloneNode(true);
    card.classList.add(type + "-card");

    const streamBadge = card.querySelector(".stream-badge");
    streamBadge.textContent = type === "technology" ? "Technology to learn" : "Industry update";
    streamBadge.classList.add(type);

    card.querySelector(".category-badge").textContent = article.category || "Automotive Software";
    card.querySelector(".source-name").textContent = article.source || "Source";
    card.querySelector(".headline").textContent = article.headline || article.source_title;
    card.querySelector(".source-title").textContent = article.source_title || "";
    card.querySelector(".summary-text").textContent = article.summary || "";
    card.querySelector(".why-text").textContent = article.why_it_matters || "";
    card.querySelector(".next-step-text").textContent = article.next_step || "";

    const badge = card.querySelector(".review-badge");
    const statusButton = card.querySelector(".status-button");
    if (reviewed) {
      badge.textContent = "Reviewed";
      badge.classList.add("done");
      statusButton.textContent = "Mark to learn";
      statusButton.classList.add("done");
    }

    if (type === "technology") {
      const comparison = card.querySelector(".comparison");
      comparison.hidden = false;
      card.querySelector(".current-stack").textContent = article.current_stack || "";
      card.querySelector(".relationship").textContent = article.relationship || "";
      card.querySelector(".comparison-note").textContent = article.comparison_note || "";
      card.querySelector(".limitations").textContent = article.limitations
        ? "Limit: " + article.limitations
        : "";

      const practical = card.querySelector(".practical");
      practical.hidden = !article.practical_example;
      card.querySelector(".practical-text").textContent = article.practical_example || "";
    }

    const concepts = card.querySelector(".concepts");
    for (const concept of article.key_concepts || []) {
      const pill = document.createElement("span");
      pill.className = "concept-pill";
      pill.textContent = concept;
      concepts.append(pill);
    }

    const questions = card.querySelector(".questions");
    for (const question of article.interview_questions || []) {
      const li = document.createElement("li");
      li.textContent = question;
      questions.append(li);
    }

    const sourceLink = card.querySelector(".source-link");
    sourceLink.href = article.source_url || "#";
    sourceLink.textContent = type === "technology" ? "Open official docs" : "Open source article";
    if (!article.source_url) sourceLink.hidden = true;

    card.querySelector(".copy-button").addEventListener("click", async (event) => {
      await navigator.clipboard.writeText(copyText(article));
      event.currentTarget.textContent = "Copied";
      setTimeout(() => {
        event.currentTarget.textContent = "Copy brief";
      }, 1200);
    });

    statusButton.addEventListener("click", () => setReviewed(article));
    articlesEl.append(card);
  }

  $("#emptyState").hidden = visible !== 0;
}

async function loadRun(path) {
  const response = await fetch(path, { cache: "no-store" });
  if (!response.ok) throw new Error("Could not load " + path + ": HTTP " + response.status);
  state.run = await response.json();
  renderSummary();
  renderArticles();
}

function renderRunPicker() {
  runSelect.replaceChildren();
  if (!state.history.length) {
    runSelect.append(new Option("No research runs yet", ""));
    runSelect.disabled = true;
    return;
  }

  for (const run of state.history) {
    runSelect.append(
      new Option(
        formatDate(run.generated_at) + " · " + run.article_count + " briefs",
        run.path
      )
    );
  }
}

async function init() {
  try {
    const response = await fetch("data/history.json", { cache: "no-store" });
    if (!response.ok) throw new Error("History request failed: HTTP " + response.status);
    const history = await response.json();
    state.history = history.runs || [];
    renderRunPicker();
    if (state.history.length) await loadRun(state.history[0].path);
    else await loadRun("data/latest.json");
  } catch (error) {
    articlesEl.innerHTML =
      '<div class="empty">Dashboard data could not be loaded. ' + error.message + "</div>";
  }
}

runSelect.addEventListener("change", () => {
  if (runSelect.value) loadRun(runSelect.value);
});

document.querySelectorAll(".filter").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".filter").forEach((item) => item.classList.remove("active"));
    button.classList.add("active");
    state.statusFilter = button.dataset.filter;
    renderArticles();
  });
});

categorySelect.addEventListener("change", () => {
  state.category = categorySelect.value;
  renderArticles();
});

init();
