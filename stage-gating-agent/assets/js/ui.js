/*
 * ui.js — DOM 描画。logic.js のフォーマット補助を使い、DATA.summary / DATA.records を
 * 画面に反映する。集計は行わず、Python が確定した値を描くだけ。
 */
const $ = id => document.getElementById(id);

// ---- データソース／審査バッジ ----
function renderHeader(summary) {
  const m = summary.meta || {};
  $('eyebrow').textContent = 'IT Budget Review — ' + (m.fy || '');
  const dot = $('srcdot'), t = $('srctext');
  dot.className = 'dot ok';
  const src = (m.sources && m.sources.length) ? m.sources.join(' + ') : '—';
  t.textContent = 'データソース：' + src + ' ／ 投資 ' + (m.investCount || 0) + '件・BAU ' + (m.bauCount || 0) + '件';
  const a = summary.audit || { errors: 0, warnings: 0 };
  const badge = $('audit-badge');
  if (a.errors > 0) badge.className = 'audit-badge err', badge.textContent = '差し戻し候補 ' + a.errors + '件 / 要確認 ' + a.warnings + '件';
  else if (a.warnings > 0) badge.className = 'audit-badge warn', badge.textContent = '要確認 ' + a.warnings + '件';
  else badge.className = 'audit-badge ok', badge.textContent = '審査フラグなし';
}

// ---- KPI ----
function renderKpis(summary) {
  const k = summary.kpi;
  $('k-total').innerHTML = oku(k.total) + '<span class="unit">億円</span>';
  $('k-total-m').textContent = '投資 ' + oku(k.investTotal) + '億 ＋ BAU ' + oku(k.bau) + '億 ／ 全' + (summary.meta.totalCount) + '件';
  $('k-normal').innerHTML = man(k.normal) + '<span class="unit">万円</span>';
  $('k-normal-m').textContent = k.normalCount + '件・要求総額の' + Math.round(k.normalPct) + '%';
  $('k-poc').innerHTML = man(k.poc) + '<span class="unit">万円</span>';
  $('k-poc-m').textContent = k.pocCount + '件・オプション枠対象';
  $('k-bau').innerHTML = oku(k.bau) + '<span class="unit">億円</span>';
  const sign = k.bauDelta >= 0 ? '+' : '−';
  $('k-bau-m').innerHTML = '前年比 <b style="color:' + (k.bauDelta >= 0 ? 'var(--up)' : 'var(--down)') + '">'
    + sign + man(Math.abs(k.bauDelta)) + '万円</b>（' + k.bauDeltaPct + '%）';
}

// ---- 汎用：単色バー ----
function renderBars(id, items, max, opts = {}) {
  const host = $(id); host.innerHTML = '';
  items.forEach(it => {
    const row = document.createElement('div'); row.className = 'bar-row';
    const color = it.color || '';
    const clsAttr = it.cls ? (' ' + it.cls) : '';
    const styleAttr = color ? (' style="background:' + color + '"') : '';
    row.innerHTML = '<div class="name" title="' + it.name + '">' + it.name + '</div>'
      + '<div class="track"><div class="fill' + clsAttr + '"' + styleAttr + ' data-w="' + (max ? it.v / max * 100 : 0) + '"></div></div>'
      + '<div class="amt">' + (it.amtHtml != null ? it.amtHtml : (man(it.v) + '万')) + '</div>';
    host.appendChild(row);
  });
  requestAnimationFrame(() => host.querySelectorAll('.fill').forEach(s => s.style.width = s.dataset.w + '%'));
}

// ---- 予算種別の構成 ----
function renderTypeBars(summary) {
  const items = summary.byType.map(t => ({
    name: t.name, v: t.value,
    cls: t.name === '通常投資' ? 'seg-normal' : (t.name === 'POC' ? 'seg-poc' : 'seg-bau')
  }));
  const max = Math.max(...items.map(i => i.v), 1);
  renderBars('bars-type', items, max);
}

// ---- 部門別（積み上げ） ----
function renderDeptBars(summary) {
  const dArr = summary.byDept;
  const max = Math.max(...dArr.map(d => d.total), 1);
  const host = $('bars-dept'); host.innerHTML = '';
  dArr.forEach(d => {
    const row = document.createElement('div'); row.className = 'bar-row';
    const segs = [['通常投資', 'var(--normal)'], ['POC', 'var(--poc)'], ['BAU', 'var(--bau)']]
      .filter(([k]) => d[k] > 0)
      .map(([k, c]) => '<span style="width:' + (d[k] / d.total * 100) + '%;background:' + c + '"></span>').join('');
    row.innerHTML = '<div class="name" title="' + d.dept + '">' + d.dept + '</div>'
      + '<div class="track"><div class="stack" data-w="' + (d.total / max * 100) + '">' + segs + '</div></div>'
      + '<div class="amt">' + man(d.total) + '万</div>';
    host.appendChild(row);
  });
  requestAnimationFrame(() => host.querySelectorAll('.stack').forEach(s => s.style.width = s.dataset.w + '%'));
}

// ---- POC パイプライン ----
function renderPocPipeline(summary) {
  const arr = summary.pocPipeline;
  const max = Math.max(...arr.map(g => g.amount), 1);
  const items = arr.map(g => ({
    name: g.gate2, v: g.amount, cls: 'seg-poc',
    amtHtml: g.count + '件 / ' + man(g.amount) + '万'
  }));
  renderBars('bars-gate2', items, max);
}

// ---- BAU コスト種別別（増減色） ----
function renderBauByType(summary) {
  const arr = summary.bauByType;
  const max = Math.max(...arr.map(c => c.amount), 1);
  const items = arr.map(c => {
    const color = c.delta > 0 ? 'var(--up)' : (c.delta < 0 ? 'var(--down)' : 'var(--flat)');
    const dtxt = c.delta === 0 ? '±0' : ((c.delta > 0 ? '+' : '−') + man(Math.abs(c.delta)) + '万');
    return {
      name: c.costType, v: c.amount, color,
      amtHtml: man(c.amount) + '万 <span style="color:' + color + ';font-size:11px">' + dtxt + '</span>'
    };
  });
  renderBars('bars-bau', items, max);
}

// ---- 月別 積み上げSVG（Python確定の monthly を描くだけ） ----
function svgStacked(monthly, maxTotal, ratio) {
  const { labels, normal, poc, bau } = monthly;
  const W = 340, H = 230, padL = 40, padB = 26, padT = 16, padR = 10;
  const plotW = W - padL - padR, plotH = H - padB - padT;
  const n = 12, gap = 0.30, step = plotW / n, bw = step * (1 - gap);
  const colors = { normal: 'var(--normal)', poc: 'var(--poc)', bau: 'var(--bau)' };
  let bars = '', axis = '', grid = '';
  const yTicks = ratio ? [0, 25, 50, 75, 100] : [0, 0.25, 0.5, 0.75, 1].map(f => f * maxTotal);
  yTicks.forEach(tv => {
    const frac = ratio ? tv / 100 : (maxTotal ? tv / maxTotal : 0);
    const y = padT + plotH * (1 - frac);
    grid += '<line x1="' + padL + '" y1="' + y.toFixed(1) + '" x2="' + (W - padR) + '" y2="' + y.toFixed(1) + '" stroke="var(--line-soft)" stroke-width="1"/>';
    const lbl = ratio ? tv + '%' : (tv / 1000000).toFixed(0);
    axis += '<text x="' + (padL - 5) + '" y="' + (y + 3).toFixed(1) + '" font-size="9" fill="var(--muted)" text-anchor="end">' + lbl + '</text>';
  });
  for (let i = 0; i < n; i++) {
    const x = padL + step * i + (step - bw) / 2;
    const t = normal[i] + poc[i] + bau[i];
    const denom = ratio ? (t || 1) : (maxTotal || 1);
    const hN = plotH * (normal[i] / denom), hP = plotH * (poc[i] / denom), hB = plotH * (bau[i] / denom);
    let yCur = padT + plotH;
    [['bau', hB, colors.bau], ['poc', hP, colors.poc], ['normal', hN, colors.normal]].forEach(([k, h, c]) => {
      if (h <= 0.1) return;
      const yy = yCur - h;
      bars += '<rect class="mbar-anim" x="' + x.toFixed(2) + '" y="' + yy.toFixed(2) + '" width="' + bw.toFixed(2) + '" height="' + h.toFixed(2) + '" fill="' + c
        + '" style="transform-origin:' + (x + bw / 2).toFixed(2) + 'px ' + (padT + plotH).toFixed(2) + 'px;transform:scaleY(0);transition:transform .8s cubic-bezier(.2,.7,.2,1) ' + (i * 0.03).toFixed(2) + 's"/>';
      yCur -= h;
    });
    axis += '<text x="' + (x + bw / 2).toFixed(2) + '" y="' + (padT + plotH + 13) + '" font-size="9" fill="var(--muted)" text-anchor="middle">' + labels[i] + '</text>';
  }
  const base = '<line x1="' + padL + '" y1="' + (padT + plotH) + '" x2="' + (W - padR) + '" y2="' + (padT + plotH) + '" stroke="var(--line)" stroke-width="1"/>';
  const unit = ratio ? '' : '<text x="' + (padL - 5) + '" y="10" font-size="8" fill="var(--muted)" text-anchor="end">百万</text>';
  const xunit = '<text x="' + (W - padR) + '" y="' + (padT + plotH + 13) + '" font-size="8" fill="var(--muted)" text-anchor="end">月</text>';
  return '<svg viewBox="0 0 ' + W + ' ' + H + '" style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg">' + grid + base + bars + axis + unit + xunit + '</svg>';
}

function renderMonthly(summary) {
  const m = summary.monthly;
  const totals = m.normal.map((_, i) => m.normal[i] + m.poc[i] + m.bau[i]);
  const maxTotal = Math.max(...totals, 1);
  $('chart-stack').innerHTML = svgStacked(m, maxTotal, false);
  $('chart-ratio').innerHTML = svgStacked(m, maxTotal, true);
  requestAnimationFrame(() => document.querySelectorAll('.mbar-anim').forEach(el => el.style.transform = 'scaleY(1)'));
}

// ---- 明細テーブル ----
function renderTable(rows) {
  const tb = $('tbody'); tb.innerHTML = '';
  rows.forEach(r => {
    const tag = r.category === '通常投資' ? 'normal' : (r.category === 'POC' ? 'poc' : 'bau');
    let delta = '<span class="delta flat">—</span>';
    if (r.delta != null) {
      if (r.delta > 0) delta = '<span class="delta up">+' + man(r.delta) + '万</span>';
      else if (r.delta < 0) delta = '<span class="delta down">−' + man(Math.abs(r.delta)) + '万</span>';
      else delta = '<span class="delta flat">±0</span>';
    }
    let badges = '';
    if (r.category === 'POC') badges += '<span class="flag">Gate2 ' + (r.gate2Time || '未設定') + '</span>';
    const lv = topFlag(r);
    if (lv) {
      const msg = (r.flags.find(f => f.level === lv) || {}).message || '';
      badges += '<span class="flag ' + (lv === 'error' ? 'err' : 'warn') + '" title="' + msg.replace(/"/g, '') + '">'
        + (lv === 'error' ? '差戻候補' : '要確認') + '</span>';
    }
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>' + r.dept + '</td>'
      + '<td><span class="tag ' + tag + '">' + r.category + '</span></td>'
      + '<td>' + r.name + badges + '</td>'
      + '<td>' + (r.vendor || '—') + '</td>'
      + '<td class="num">' + yen(r.amount) + '</td>'
      + '<td class="num">' + delta + '</td>'
      + '<td style="color:var(--muted);font-size:11.5px">' + (r.note || '') + '</td>';
    tb.appendChild(tr);
  });
  const sum = rows.reduce((s, r) => s + (r.amount || 0), 0);
  $('rowcount').textContent = '表示 ' + rows.length + '件 ／ 合計 ' + yen(sum);
}

// 部門セレクトの選択肢を作る（レコードから重複排除するだけ。集計ではない）
function fillDeptOptions(records) {
  const sel = $('sel-dept');
  [...new Set(records.map(r => r.dept))].sort((a, b) => a.localeCompare(b, 'ja')).forEach(d => {
    const o = document.createElement('option'); o.value = d; o.textContent = d; sel.appendChild(o);
  });
}
