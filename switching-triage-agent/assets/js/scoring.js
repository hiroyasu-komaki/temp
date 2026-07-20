/*
 * scoring.js — Score = V × U × R の計算と束ね評価。
 *
 * src/modules/scoring.py の移植版。式・閾値は direction/scoring_methodology.md
 * に対応する。数式を変える場合は、Python側・methodology・このファイルを
 * すべて更新すること（乖離させない）。
 *
 * λ（lambdaRisk）と h（leadTimeHMonths）は FIXED_PARAMS として scenario.json
 * の値に固定し、ダッシュボードのUIでは調整できないようにしている
 * （効果の説明が難しいため。詳細は input/scenario.json 参照）。
 */

// ---- 実行確度 p の解決（延長ペナルティ込み）------------------------------
//
// contestProb と execProb が両方あればその積を使う（後方互換で単独値へフォールバック）。
// extCount が extThreshold 以上なら execProb を割り引く。
function effectiveP(item, params) {
  const contest = item.contestProb;
  const execP = item.execProb;
  const ext = item.extCount || 0;

  const extThreshold = params.extThreshold;
  const extPenalty = params.extPenalty;
  const extCap = params.extPenaltyCap;

  let penalty = 0;
  let penalized = false;
  if (execP != null && ext >= extThreshold) {
    const over = ext - extThreshold + 1;
    penalty = Math.min(extPenalty * over, extCap);
    penalized = true;
  }

  let p, pContest, pExecEff, splitUsed;
  if (contest != null && execP != null) {
    pExecEff = execP * (1 - penalty);
    p = contest * pExecEff;
    pContest = contest;
    splitUsed = true;
  } else {
    const base = item.execProbability;
    p = ext >= extThreshold ? base * (1 - penalty) : base;
    penalized = ext >= extThreshold && penalty > 0;
    pContest = null;
    pExecEff = null;
    splitUsed = false;
  }

  return {
    p: Math.max(0, Math.min(1, p)),
    pContest,
    pExecEffective: pExecEff,
    extCount: ext,
    extPenalized: penalized,
    extPenalty: Math.round(penalty * 1000) / 1000,
    pSplitUsed: splitUsed,
  };
}

// ---- 基準日シフトを反映した expiry (残月数) ------------------------------
//
// Python本体では as_of_date は表示ラベルのみで expiry_months は
// CSV入力時点ですでに基準日からの相対値として固定されている（動的な
// 再計算はしない）。ダッシュボードでは as_of_date を「動かして試せる」
// パラメータにする意味を持たせるため、BASE_AS_OF からのシフト分だけ
// 各契約の expiryM を前later/後ろへずらす。これは本体パイプラインには
// ない、ダッシュボード側だけの拡張ロジック。
function monthsBetween(fromISO, toISO) {
  const a = new Date(fromISO + "T00:00:00");
  const b = new Date(toISO + "T00:00:00");
  const days = (b - a) / (1000 * 60 * 60 * 24);
  return days / 30.4375; // 平均月長で近似
}

function shiftedExpiry(item, params) {
  const shift = monthsBetween(BASE_AS_OF, params.asOfDate);
  return item.expiryM - shift;
}

// ---- 単一候補の因子計算 ---------------------------------------------------
function factors(item, params) {
  const lam = FIXED_PARAMS.lambdaRisk;
  const h = FIXED_PARAMS.leadTimeHMonths;

  const pinfo = effectiveP(item, params);
  const p = pinfo.p;

  const net = item.ret - item.cost;
  const Vraw = p * net * (1 - lam * (1 - p));

  const expiryM = shiftedExpiry(item, params);
  const d_i = expiryM - item.lead;

  let U;
  if (d_i < 0) {
    U = 0;
  } else {
    U = 1 / (1 + d_i / h);
  }

  const g = Math.min(Math.max(d_i, 0) / h, 1);
  const R = 1 - item.retSigma * g;

  return { net, Vraw, d_i, U, R, pEffective: p, ...pinfo };
}

// ---- 束ね（ベンダー単位バンドル）------------------------------------------
function buildBundles(activeContracts, params) {
  const beta = params.betaBundle;
  const byVendor = {};
  activeContracts.forEach((c) => {
    (byVendor[c.vendor] ??= []).push(c);
  });

  const bundles = [];
  for (const [vendor, members] of Object.entries(byVendor)) {
    if (members.length < 2) continue;
    const n = members.length;
    const ret = beta * members.reduce((s, m) => s + m.ret, 0);
    const cost = members.reduce((s, m) => s + m.cost, 0);
    let prodP = 1;
    members.forEach((m) => {
      prodP *= effectiveP(m, params).p;
    });
    const p = Math.pow(prodP, 1 / Math.sqrt(n));
    const retSigma = Math.max(...members.map((m) => m.retSigma));
    const expiryM = Math.min(...members.map((m) => shiftedExpiry(m, params)));
    const lead = Math.max(...members.map((m) => m.lead));

    bundles.push({
      id: `B-${vendor}`,
      name: `${vendor} 一括（${n}件）`,
      type: "Bundle",
      vendor,
      _shiftedExpiryM: expiryM, // すでにシフト済みなので factors() 内で二重シフトしない
      spend: members.reduce((s, m) => s + m.spend, 0),
      lead,
      cost,
      costSigma: 0,
      ret,
      retSigma,
      execProbability: p,
      contestProb: null,
      execProb: null,
      extCount: 0,
      active: 1,
      isBundle: true,
      members: members.map((m) => m.id),
    });
  }
  return bundles;
}

// バンドル候補は expiryM をすでにシフト済みで保持しているため、
// factors() 呼び出し時に二重シフトしないよう専用パスを通す。
function factorsForBundle(bundle, params) {
  const lam = FIXED_PARAMS.lambdaRisk;
  const h = FIXED_PARAMS.leadTimeHMonths;
  const p = bundle.execProbability; // 束ねは合成済み確度をそのまま持つ
  const net = bundle.ret - bundle.cost;
  const Vraw = p * net * (1 - lam * (1 - p));
  const d_i = bundle._shiftedExpiryM - bundle.lead;
  let U = d_i < 0 ? 0 : 1 / (1 + d_i / h);
  const g = Math.min(Math.max(d_i, 0) / h, 1);
  const R = 1 - bundle.retSigma * g;
  return {
    net, Vraw, d_i, U, R, pEffective: p,
    pContest: null, pExecEffective: null, extCount: 0,
    extPenalized: false, extPenalty: 0, pSplitUsed: false,
  };
}

// ---- 判定ラベル ------------------------------------------------------------
function verdictOf(d_i, score, Vn, U, R) {
  if (d_i < 0) return { key: "失効", cls: "v-lapse" };
  if (score >= 0.25) return { key: "即着手", cls: "v-act" };
  if (U >= 0.5 && R < 0.7) return { key: "人間判断", cls: "v-judge" };
  if (Vn > 0.3 && U < 0.4) return { key: "温存", cls: "v-hold" };
  if (Vn < 0.1) return { key: "捨てる候補", cls: "v-drop" };
  return { key: "検討", cls: "v-check" };
}

// ---- メイン: 候補集合を構築してスコアリング --------------------------------
function scoreAll(params) {
  const active = CONTRACTS.filter((c) => Number(c.active) === 1);
  const excludedInactive = CONTRACTS.filter((c) => Number(c.active) !== 1).map((c) => c.name);

  let candidates = active.map((c) => ({ ...c, isBundle: false }));

  // 束ねは個別合計より有利かどうかに関わらず、常にランキングに候補として
  // 併記する（構成契約を除外・置換しない）。どちらを選ぶかはユーザーが
  // チェックボックスで手動選択する。
  if (params.useBundle) {
    const bundles = buildBundles(active, params);
    bundles.forEach((b) => candidates.push(b));
  }

  candidates = candidates.map((c) => {
    const f = c.isBundle ? factorsForBundle(c, params) : factors(c, params);
    return { ...c, ...f };
  });

  const maxV = Math.max(1e-9, ...candidates.map((c) => Math.max(c.Vraw, 0)));
  candidates.forEach((c) => {
    c.Vn = Math.max(c.Vraw, 0) / maxV;
    c.score = c.Vn * c.U * c.R;
    c.verdict = verdictOf(c.d_i, c.score, c.Vn, c.U, c.R);
  });
  candidates.sort((a, b) => b.score - a.score);

  return { candidates, excludedInactive };
}
