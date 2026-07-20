/*
 * ui.js — DOM描画。scoring.js / allocation.js の計算結果を画面に反映する。
 * ロジック本体には触れず、表示だけを担当する。
 */
const $ = (id) => document.getElementById(id);
const fmt = (n) => (Math.round(n * 10) / 10).toLocaleString("ja-JP");

// ---- 延長ペナルティ「厳しさ」プリセット ------------------------------------
// scenario.json の既定値（threshold=2, penalty=0.15, cap=0.6）を
// レベル50（標準）にちょうど一致させてある。
const EXT_PRESETS = {
  0:   { threshold: 4, penalty: 0.08, cap: 0.30, label: "甘い" },
  25:  { threshold: 3, penalty: 0.12, cap: 0.45, label: "やや甘い" },
  50:  { threshold: 2, penalty: 0.15, cap: 0.60, label: "標準" },
  75:  { threshold: 2, penalty: 0.22, cap: 0.75, label: "やや厳しい" },
  100: { threshold: 1, penalty: 0.30, cap: 0.90, label: "厳しい" },
};

function renderControls(params) {
  $("budget").value = params.budgetM;
  $("lBudget").textContent = params.budgetM;
  $("margin").value = params.safetyMargin;
  $("lMargin").textContent = Math.round(params.safetyMargin * 100) + "%";
  $("useBundle").checked = params.useBundle;
  $("beta").value = params.betaBundle;
  $("lBeta").textContent = params.betaBundle.toFixed(2);
  $("betaSub").hidden = !params.useBundle;
  $("asOfDate").value = params.asOfDate;

  $("fixedLambda").textContent = FIXED_PARAMS.lambdaRisk.toFixed(2);
  $("fixedH").textContent = FIXED_PARAMS.leadTimeHMonths.toFixed(1);
}

function renderInactiveBlock(excludedInactive) {
  const panel = $("inactivePanel");
  const list = $("inactiveList");
  if (!excludedInactive.length) {
    panel.hidden = true;
    list.innerHTML = "";
    return;
  }
  panel.hidden = false;
  list.innerHTML = excludedInactive
    .map(
      (name) =>
        `<tr><td>${name}</td><td><span class="verdict v-inactive">対象外</span></td></tr>`
    )
    .join("");
}

// 残月(d_i)を「閾値=リードタイム基準h」でRAG化: 失効(d_i<0)=R、h超=G、それ以外=A
function ragForResidual(d_i) {
  if (d_i < 0) return "r";
  if (d_i > FIXED_PARAMS.leadTimeHMonths) return "g";
  return "a";
}

function extCell(r) {
  if (!r.extCount) return `<span class="ext-none">–</span>`;
  const cls = r.extPenalized ? "ext-bad" : "ext-ok";
  const title = r.extPenalized
    ? `延長${r.extCount}回でexecution_probを${Math.round(r.extPenalty * 100)}%割引`
    : `延長${r.extCount}回（ペナルティ未発動）`;
  return `<span class="ext-badge ${cls}" title="${title}">⚠×${r.extCount}</span>`;
}

function pCellTitle(r) {
  if (r.pSplitUsed) {
    const extNote = r.extPenalized ? `（延長ペナルティ${Math.round(r.extPenalty * 100)}%適用後）` : "";
    return `契約可能性${r.pContest.toFixed(2)} × 実行確度${r.pExecEffective.toFixed(2)}${extNote}`;
  }
  return `exec_probability ${r.pEffective.toFixed(2)}（単独値）`;
}

function renderTable(rows, selectedIds) {
  const tb = $("rankTable").querySelector("tbody");
  tb.innerHTML = rows
    .map((r) => {
      const vW = r.Vn * 100;
      const uW = r.U * 100;
      const rW = r.R * 100;
      const rag = ragForResidual(r.d_i);
      const checked = selectedIds.has(String(r.id)) ? "checked" : "";
      return `<tr class="${r.isBundle ? "bundle-row" : ""}">
        <td class="num"><input type="checkbox" class="row-select" data-id="${r.id}" ${checked}></td>
        <td>${r.name}${r.isBundle ? " 🔗" : ""}</td>
        <td class="num">${fmt(r.cost)}</td>
        <td class="num">${fmt(r.net)}</td>
        <td class="num" title="${pCellTitle(r)}">${r.pEffective.toFixed(2)}</td>
        <td class="num">${extCell(r)}</td>
        <td class="num"><span class="rag rag-${rag}"></span>${r.d_i.toFixed(1)}</td>
        <td>
          <div class="factor-score">
            <div class="factor-bars">
              <div class="frow"><span class="flabel-mini">V</span>
                <span class="fbar-single"><span class="fV" style="width:${vW}%"></span></span>
                <span class="fnum">${r.Vn.toFixed(2)}</span></div>
              <div class="frow"><span class="flabel-mini">U</span>
                <span class="fbar-single"><span class="fU" style="width:${uW}%"></span></span>
                <span class="fnum">${r.U.toFixed(2)}</span></div>
              <div class="frow"><span class="flabel-mini">R</span>
                <span class="fbar-single"><span class="fR" style="width:${rW}%"></span></span>
                <span class="fnum">${r.R.toFixed(2)}</span></div>
            </div>
            <div class="score-big">${r.score.toFixed(3)}</div>
          </div>
        </td>
        <td><span class="verdict ${r.verdict.cls}">${r.verdict.key}</span></td>
      </tr>`;
    })
    .join("");
}

// ---- チェックボックス選択に基づくKPI（本コミット額・期待ネット・資金差分） ----
// 「本コミット」はもはやアルゴリズムの自動判定ではなく、ユーザーがチェックした
// 案件そのもの。資金差分は手元資金Bとの差（黒字=プラス、資金ショート=マイナス）。
// RAGは 選択合計 <= 使用可能額(B×(1-安全余裕))=緑 / <= B=黄 / > B=赤。
function renderSelectionKpis(candidates, selectedIds, params) {
  const selected = candidates.filter((c) => selectedIds.has(String(c.id)));
  const committed = selected.reduce((s, c) => s + c.cost, 0);
  const expectedNet = selected.reduce((s, c) => s + c.pEffective * c.net, 0);
  // ROIは総回収ベース: p×想定リターン(コスト控除前) ÷ 切替コスト。
  // 損益分岐点は100%（=投じたコストをちょうど回収できる期待値）。
  // 100%未満は逆鞘（投じたコストの期待回収額がコストに届かない）。
  const expectedGrossReturn = selected.reduce((s, c) => s + c.pEffective * c.ret, 0);

  const actionable = candidates.filter((c) => c.d_i >= 0 && c.score >= 0.25).length;

  $("kActionable").textContent = actionable;
  $("kCommit").textContent = fmt(committed) + "M";
  $("kCommit").title = "チェックした案件の切替コスト合計";
  $("kReturn").textContent = fmt(expectedNet) + "M";
  $("kReturn").title = "チェックした案件の p×net 合計（確度で割り引いた期待ネット）";

  const kRoi = $("kRoi");
  ["g", "r"].forEach((k) => kRoi.closest(".kpi").classList.remove(`rag-light-${k}`));
  if (committed > 0) {
    const roi = expectedGrossReturn / committed;
    kRoi.textContent = `${Math.round(roi * 100)}%`;
    kRoi.closest(".kpi").classList.add(roi >= 1 ? "rag-light-g" : "rag-light-r");
  } else {
    kRoi.textContent = "–";
  }
  kRoi.title = "p×想定リターン(コスト控除前) ÷ 本コミット額。100%が損益分岐点、100%未満は逆鞘（投じたコストの期待回収額が届かない）";

  const B = params.budgetM;
  const margin = params.safetyMargin;
  const avail = B * (1 - margin);
  const diff = B - committed;
  const rag = committed > B ? "r" : committed > avail ? "a" : "g";

  const kDiff = $("kDiff");
  kDiff.textContent = `${diff >= 0 ? "+" : ""}${fmt(diff)}M`;
  kDiff.title = `手元資金${B}M − 選択合計${fmt(committed)}M（使用可能額${fmt(avail)}M・安全余裕${Math.round(margin * 100)}%）`;

  ["g", "a", "r"].forEach((k) => kDiff.closest(".kpi").classList.remove(`rag-light-${k}`));
  kDiff.closest(".kpi").classList.add(`rag-light-${rag}`);

  [$("lBudget"), $("lMargin")].forEach((el) => {
    ["g", "a", "r"].forEach((k) => el.classList.remove(`rag-light-${k}`));
    el.classList.add(`rag-light-${rag}`);
  });
}
