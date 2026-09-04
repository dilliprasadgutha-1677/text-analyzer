const textInput = document.querySelector("#source-text");
const analyzeButton = document.querySelector("#analyze-button");
const clearButton = document.querySelector("#clear-button");
const summaryContent = document.querySelector("#summary-content");
const errorMessage = document.querySelector("#error-message");
const lengthButtons = document.querySelectorAll("[data-length]");
let selectedLength = "medium";

function updateLiveMetrics() {
  const text = textInput.value;
  const words = text.match(/\b[\w'-]+\b/g) || [];
  document.querySelector("#live-count").textContent = `${words.length} ${words.length === 1 ? "word" : "words"}`;
  document.querySelector("#word-count").textContent = words.length.toLocaleString();
  document.querySelector("#character-count").textContent = text.length.toLocaleString();
  document.querySelector("#sentence-count").textContent = text.trim() ? (text.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || []).filter(Boolean).length : 0;
  document.querySelector("#reading-time").textContent = words.length ? Math.max(1, Math.round(words.length / 200)) : 0;
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
}

function renderSummary(items) {
  if (!items.length) {
    summaryContent.innerHTML = '<div class="empty-state"><p>No takeaways found.</p><span>Try adding a little more text.</span></div>';
    return;
  }
  const list = document.createElement("ul");
  list.className = "summary-list";
  items.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    list.appendChild(listItem);
  });
  summaryContent.replaceChildren(list);
}

async function analyzeText() {
  errorMessage.hidden = true;
  if (!textInput.value.trim()) {
    showError("Add some text before analyzing it.");
    textInput.focus();
    return;
  }
  analyzeButton.disabled = true;
  analyzeButton.querySelector("span").textContent = "Analyzing...";
  summaryContent.innerHTML = '<div class="loading"><span class="spinner" aria-hidden="true"></span><span>Finding the signal in your text...</span></div>';
  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: textInput.value, length: selectedLength }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The analysis could not be completed.");
    document.querySelector("#word-count").textContent = data.metrics.word_count.toLocaleString();
    document.querySelector("#character-count").textContent = data.metrics.character_count.toLocaleString();
    document.querySelector("#sentence-count").textContent = data.metrics.sentence_count.toLocaleString();
    document.querySelector("#reading-time").textContent = data.metrics.reading_time;
    renderSummary(data.summary);
  } catch (error) {
    summaryContent.innerHTML = '<div class="empty-state"><p>Analysis paused.</p><span>Check the connection and try again.</span></div>';
    showError(error.message || "Unable to reach the analysis service.");
  } finally {
    analyzeButton.disabled = false;
    analyzeButton.querySelector("span").textContent = "Analyze & summarize";
  }
}

textInput.addEventListener("input", updateLiveMetrics);
analyzeButton.addEventListener("click", analyzeText);
clearButton.addEventListener("click", () => {
  textInput.value = "";
  updateLiveMetrics();
  errorMessage.hidden = true;
  summaryContent.innerHTML = '<div class="empty-state"><span class="empty-mark" aria-hidden="true">&darr;</span><p>Your key takeaways will appear here.</p><span>Paste text above and start an analysis.</span></div>';
  textInput.focus();
});
lengthButtons.forEach((button) => button.addEventListener("click", () => {
  selectedLength = button.dataset.length;
  lengthButtons.forEach((item) => item.classList.toggle("active", item === button));
}));