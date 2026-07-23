/*
 * logic.js — 表示補助のみ（金額フォーマット、テーブルのフィルタ／ソート）。
 *
 * 集計は Python 側（src/modules/processor.py）で確定済み。ここでは合算・按分・比率
 * などの集計は行わない。DATA.summary / DATA.records をそのまま扱う。
 */

// ---- 金額フォーマット ----
const yen = n => '¥' + Math.round(n || 0).toLocaleString('ja-JP');
const oku = n => ((n || 0) / 100000000).toFixed(2);
const man = n => Math.round((n || 0) / 10000).toLocaleString('ja-JP');

// ---- レコードの最上位フラグレベル（error > warn > null） ----
function topFlag(rec) {
  const fs = rec.flags || [];
  if (fs.some(f => f.level === 'error')) return 'error';
  if (fs.some(f => f.level === 'warn')) return 'warn';
  return null;
}

// ---- テーブル用：フィルタ（集計せず絞るだけ） ----
function filterRecords(records, { scope, dept, type }) {
  return records.filter(r => {
    if (scope === 'invest' && r.category === 'BAU') return false;
    if (scope === 'bau' && r.category !== 'BAU') return false;
    if (scope === 'flagged' && !topFlag(r)) return false;
    if (dept && r.dept !== dept) return false;
    if (type && r.category !== type) return false;
    return true;
  });
}

// ---- テーブル用：ソート（表示操作のみ） ----
function sortRecords(records, key, dir) {
  const arr = records.slice();
  arr.sort((a, b) => {
    let x = a[key], y = b[key];
    if (key === 'amount' || key === 'delta') { x = x || 0; y = y || 0; return (x - y) * dir; }
    x = (x == null ? '' : x).toString();
    y = (y == null ? '' : y).toString();
    return x.localeCompare(y, 'ja') * dir;
  });
  return arr;
}
