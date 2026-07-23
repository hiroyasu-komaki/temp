/*
 * main.js — 初期化と結線。DATA（集計済み）を各描画関数へ渡し、テーブルの
 * フィルタ／ソート操作だけをハンドリングする。集計は一切行わない。
 */
let tableState = { scope: 'all', dept: '', type: '', sortKey: 'amount', sortDir: -1 };

function refreshTable() {
  const filtered = filterRecords(DATA.records || [], tableState);
  const sorted = sortRecords(filtered, tableState.sortKey, tableState.sortDir);
  renderTable(sorted);
}

function init() {
  const summary = DATA.summary || {};
  if (!summary.kpi) {
    $('srctext').textContent = 'データがありません。src/main.py run を実行してください。';
    $('srcdot').className = 'dot warn';
    return;
  }
  renderHeader(summary);
  renderKpis(summary);
  renderTypeBars(summary);
  renderDeptBars(summary);
  renderPocPipeline(summary);
  renderBauByType(summary);
  renderMonthly(summary);

  fillDeptOptions(DATA.records || []);
  refreshTable();

  // 表示スコープ切替
  $('tgl-scope').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    document.querySelectorAll('#tgl-scope button').forEach(x => x.classList.remove('on'));
    b.classList.add('on'); tableState.scope = b.dataset.scope; refreshTable();
  });
  $('sel-dept').addEventListener('change', e => { tableState.dept = e.target.value; refreshTable(); });
  $('sel-type').addEventListener('change', e => { tableState.type = e.target.value; refreshTable(); });
  document.querySelectorAll('#tbl thead th').forEach(th => {
    th.addEventListener('click', () => {
      const k = th.dataset.k;
      if (tableState.sortKey === k) tableState.sortDir *= -1;
      else { tableState.sortKey = k; tableState.sortDir = (k === 'amount' || k === 'delta') ? -1 : 1; }
      refreshTable();
    });
  });
}

document.addEventListener('DOMContentLoaded', init);
