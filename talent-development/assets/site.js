/* Skill Management Framework
   資料ページ共通スクリプト（固定ヘッダー／言語切替／読了目安／目次チップ／サイドTOC／進捗バー／トップへ戻る）
   Shared script for content pages: sticky header, language switch, reading time, TOC, progress bar.
   .pagenav が存在するページでのみ動作する。 */
(function () {
  "use strict";

  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  function $all(sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); }

  var pagenav = $(".pagenav");
  if (!pagenav) return; // index.html 等、資料ページ以外では何もしない

  // 資料の並び順（トップバーの位置表示・レイヤー表示に使用）
  // ── 言語判定（/ja/ ・ /en/ のディレクトリで決まる） ──
  var segs = location.pathname.split("/");
  var fileName = segs.pop() || "";
  var LANG = segs.pop() === "en" ? "en" : "ja";
  var STEM = fileName.replace(/\.html$/, "");

  var STRINGS = {
    ja: { home: "資料一覧", homeTitle: "フレームワーク地図へ", time: function (m) { return "読了目安 約" + m + "分"; },
          prev: "前の部", next: "次の部", onThisPage: "この部の目次", backTop: "トップへ戻る", cpm: 500 },
    en: { home: "Contents", homeTitle: "Back to the framework map", time: function (m) { return "About " + m + " min read"; },
          prev: "Previous part", next: "Next part", onThisPage: "ON THIS PAGE", backTop: "Back to top", cpm: 1100 }
  };
  var S = STRINGS[LANG];

  var DOCS = [
    { stem: "p1_premise",   ja: "第I部 ─ 前提",     en: "PART I ─ PREMISE" },
    { stem: "p2_position",  ja: "第II部 ─ 現在地",  en: "PART II ─ POSITION" },
    { stem: "p3_measure",   ja: "第III部 ─ 測定",   en: "PART III ─ MEASUREMENT" },
    { stem: "p4_demand",    ja: "第IV部 ─ 目標",    en: "PART IV ─ TARGET" },
    { stem: "p5_structure", ja: "第V部 ─ 構造",     en: "PART V ─ STRUCTURE" },
    { stem: "p6_execute",   ja: "第VI部 ─ 実行",    en: "PART VI ─ EXECUTION" },
    { stem: "p7_tools",     ja: "第VII部 ─ 道具",   en: "PART VII ─ TOOLING" },
    { stem: "p8_goal",      ja: "第VIII部 ─ 到達点", en: "PART VIII ─ END STATE" },
    { stem: "ref",          ja: "付録",             en: "APPENDIX" }
  ];

  document.body.classList.add("has-topbar");

  var h1El = $("h1");
  var titleText = h1El ? h1El.textContent.trim() : document.title;

  var idx = DOCS.map(function (d) { return d.stem; }).indexOf(STEM);
  var layerText = idx >= 0 ? DOCS[idx][LANG] : ($(".eyebrow") ? $(".eyebrow").textContent.trim() : "");

  var prevA = $(".pagenav .prev a");
  var nextA = $(".pagenav .next a");

  // ── 読了目安（日本語の文章密度を踏まえ、概ね500文字/分で概算） ──
  var slide = $(".slide");
  var charCount = slide ? slide.textContent.replace(/\s+/g, "").length : 0;
  var minutes = Math.max(1, Math.round(charCount / S.cpm));

  // ── 言語切替（同一ページの対訳版へ。ハッシュは維持する） ──
  var otherHref = "../" + (LANG === "ja" ? "en" : "ja") + "/" + fileName + location.hash;
  var homeHref = "../index.html?lang=" + LANG;

  // ── 固定ヘッダー ──
  var bar = document.createElement("div");
  bar.id = "site-topbar";
  bar.innerHTML =
    '<a class="tb-home" href="' + homeHref + '" title="' + S.homeTitle + '"><span class="tb-logo">SMF</span><span class="tb-home-label">' + S.home + "</span></a>" +
    '<span class="tb-sep">/</span>' +
    '<div class="tb-meta">' +
      '<div class="tb-eyebrow">' + layerText + "</div>" +
      '<div class="tb-title">' + titleText + "</div>" +
    "</div>" +
    (idx >= 0 ? '<div class="tb-pos">' + (idx + 1) + " / " + DOCS.length + "</div>" : "") +
    '<div class="tb-time">' + S.time(minutes) + "</div>" +
    '<div class="tb-lang">' +
      (LANG === "ja" ? '<span class="on">日本語</span><a href="' + otherHref + '" hreflang="en">EN</a>'
                     : '<a href="' + otherHref + '" hreflang="ja">日本語</a><span class="on">EN</span>') +
    "</div>" +
    '<div class="tb-nav">' +
      (prevA ? '<a class="tb-prev" href="' + prevA.getAttribute("href") + '" title="' + S.prev + '">←</a>' : '<span class="tb-prev off">←</span>') +
      (nextA ? '<a class="tb-next" href="' + nextA.getAttribute("href") + '" title="' + S.next + '">→</a>' : '<span class="tb-next off">→</span>') +
    "</div>";
  document.body.insertBefore(bar, document.body.firstChild);

  var progress = document.createElement("div");
  progress.id = "tb-progress";
  var progressFill = document.createElement("div");
  progressFill.id = "tb-progress-fill";
  progress.appendChild(progressFill);
  document.body.insertBefore(progress, bar.nextSibling);

  // ── セクション一覧の収集（.sec > .step を1セクションとして扱う） ──
  var secs = $all(".sec").filter(function (s) { return $(".step", s); });
  secs.forEach(function (s, i) { s.id = "sec-" + i; });

  function stepLabel(stepEl) {
    var clone = stepEl.cloneNode(true);
    var nSpan = $(".n", clone);
    var n = nSpan ? nSpan.textContent.trim() : "";
    if (nSpan) nSpan.parentNode.removeChild(nSpan);
    return { n: n, text: clone.textContent.trim() };
  }

  // ── 冒頭の目次チップ（本文の直前に、資料全体の見取り図として挿入） ──
  var lede = $(".lede");
  if (lede && secs.length >= 3) {
    var chipNav = document.createElement("div");
    chipNav.className = "doc-chipnav";
    secs.forEach(function (s, i) {
      var stepEl = $(".step", s);
      if (!stepEl) return;
      var lbl = stepLabel(stepEl);
      var a = document.createElement("a");
      a.href = "#sec-" + i;
      a.className = "chip";
      a.innerHTML = '<span class="chip-n">' + lbl.n + "</span>" + lbl.text;
      chipNav.appendChild(a);
    });
    lede.parentNode.insertBefore(chipNav, lede.nextSibling);
  }

  // ── サイドTOC（広い画面のみ表示。CSS側で幅により非表示制御） ──
  if (secs.length >= 3) {
    var toc = document.createElement("nav");
    toc.id = "site-toc";
    var label = document.createElement("div");
    label.className = "toc-label";
    label.textContent = S.onThisPage;
    toc.appendChild(label);
    var ul = document.createElement("ul");
    secs.forEach(function (s, i) {
      var stepEl = $(".step", s);
      if (!stepEl) return;
      var lbl = stepLabel(stepEl);
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "#sec-" + i;
      a.textContent = lbl.n + "　" + lbl.text;
      li.appendChild(a);
      ul.appendChild(li);
    });
    toc.appendChild(ul);
    document.body.appendChild(toc);

    if ("IntersectionObserver" in window) {
      var tocLinks = $all("a", toc);
      var obs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var link = toc.querySelector('a[href="#' + entry.target.id + '"]');
          if (!link) return;
          tocLinks.forEach(function (l) { l.classList.remove("active"); });
          link.classList.add("active");
        });
      }, { rootMargin: "-96px 0px -70% 0px", threshold: 0 });
      secs.forEach(function (s) { obs.observe(s); });
    }
  }

  // ── スクロール進捗 ──
  function updateProgress() {
    var de = document.documentElement;
    var scrollTop = de.scrollTop || document.body.scrollTop;
    var scrollH = (de.scrollHeight || document.body.scrollHeight) - de.clientHeight;
    var pct = scrollH > 0 ? Math.min(100, (scrollTop / scrollH) * 100) : 0;
    progressFill.style.width = pct + "%";
  }

  // ── トップへ戻るボタン ──
  var backTop = document.createElement("button");
  backTop.id = "tb-top";
  backTop.type = "button";
  backTop.title = S.backTop;
  backTop.setAttribute("aria-label", S.backTop);
  backTop.textContent = "↑";
  backTop.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
  document.body.appendChild(backTop);

  function onScroll() {
    updateProgress();
    var y = document.documentElement.scrollTop || document.body.scrollTop;
    backTop.classList.toggle("show", y > 700);
  }
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();
