/*
 * main.js — UIコントロールと計算(scoring.js)を結線する。
 *
 * ダッシュボード上で動かせるのは意図的に5項目のみ:
 *   評価基準日, budget_m, safety_margin, use_bundle(+beta_bundle), 延長への厳しさ
 * lambda_risk と lead_time_h_months は説明が難しいため固定表示のみ（FIXED_PARAMS）。
 *
 * 「本コミット額」「着手分の期待ネット」は自動配分アルゴリズムではなく、
 * ユーザーが優先度ランキングでチェックした案件から直接集計する
 * （チェックボックス = 「対象」列）。資金差分・RAGはその選択と手元資金/安全余裕の比較。
 */

let currentParams = { ...DEFAULT_PARAMS };
let currentExtLevel = 50; // 延長への厳しさ（0〜100、既定=標準=scenario.jsonの値と一致）
let currentCandidates = [];
const selectedIds = new Set(); // チェックした案件のid（文字列化して保持、既定は未選択）

function applyExtLevel(level) {
  const preset = EXT_PRESETS[level];
  currentParams.extThreshold = preset.threshold;
  currentParams.extPenalty = preset.penalty;
  currentParams.extPenaltyCap = preset.cap;
  $("lExtLevel").textContent = `${preset.label}（延長${preset.threshold}回目から、1回${Math.round(preset.penalty * 100)}%減、上限${Math.round(preset.cap * 100)}%）`;
}

function updateKpis() {
  renderSelectionKpis(currentCandidates, selectedIds, currentParams);
}

function recompute() {
  const { candidates, excludedInactive } = scoreAll(currentParams);
  currentCandidates = candidates;

  renderInactiveBlock(excludedInactive);
  renderTable(candidates, selectedIds);
  updateKpis();
}

function init() {
  currentParams = { ...DEFAULT_PARAMS };
  applyExtLevel(currentExtLevel);
  renderControls(currentParams);
  $("extLevel").value = currentExtLevel;

  $("asOfDate").addEventListener("change", (e) => {
    currentParams.asOfDate = e.target.value || BASE_AS_OF;
    recompute();
  });

  $("budget").addEventListener("input", (e) => {
    currentParams.budgetM = Number(e.target.value);
    $("lBudget").textContent = currentParams.budgetM;
    updateKpis();
  });

  $("margin").addEventListener("input", (e) => {
    currentParams.safetyMargin = Number(e.target.value);
    $("lMargin").textContent = Math.round(currentParams.safetyMargin * 100) + "%";
    updateKpis();
  });

  $("useBundle").addEventListener("change", (e) => {
    currentParams.useBundle = e.target.checked;
    $("betaSub").hidden = !currentParams.useBundle;
    recompute();
  });

  $("beta").addEventListener("input", (e) => {
    currentParams.betaBundle = Number(e.target.value);
    $("lBeta").textContent = currentParams.betaBundle.toFixed(2);
    recompute();
  });

  $("extLevel").addEventListener("input", (e) => {
    currentExtLevel = Number(e.target.value);
    applyExtLevel(currentExtLevel);
    recompute();
  });

  // チェックボックスは行の再描画のたびに作り直されるため、テーブル本体に
  // イベント委譲する（テーブル要素自体は再描画されず残り続ける）。
  $("rankTable").addEventListener("change", (e) => {
    if (!e.target.classList.contains("row-select")) return;
    const id = e.target.dataset.id;
    if (e.target.checked) {
      selectedIds.add(id);
    } else {
      selectedIds.delete(id);
    }
    updateKpis();
  });

  recompute();
}

document.addEventListener("DOMContentLoaded", init);
