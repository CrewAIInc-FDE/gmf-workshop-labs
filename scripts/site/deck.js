/* Slides page: present mode, keyboard control, number jump, speaker window sync. */
(function () {
  var deck = document.getElementById('deck');
  if (!deck) return;
  var slides = Array.prototype.slice.call(deck.querySelectorAll('.slide'));
  var total = slides.length;
  if (!total) return;
  var moduleName = deck.getAttribute('data-module');
  var notesUrl = deck.getAttribute('data-notes-url');
  var live = document.getElementById('live');
  var hud = document.getElementById('jump-hud');
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('.toc a[href^="#slide-"]'));
  var cur = 1, presenting = false, enteredFullscreen = false, buf = '', bufTimer = null;
  var bc = null;
  try { if ('BroadcastChannel' in window) bc = new BroadcastChannel('workshop-deck:' + moduleName); } catch (e) {}

  function clamp(n) { return Math.max(1, Math.min(total, n)); }
  function post(msg) { if (bc) { try { bc.postMessage(msg); } catch (e) {} } }
  function announce() { post({ type: 'slide', n: cur, total: total }); }

  function markActive() {
    tocLinks.forEach(function (a, i) {
      var on = (i + 1 === cur);
      a.classList.toggle('active', on);
      if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
    var link = tocLinks[cur - 1];
    if (link && link.scrollIntoView && !presenting) link.scrollIntoView({ block: 'nearest' });
  }

  function setCurrent(n, opts) {
    opts = opts || {};
    n = clamp(n);
    var changed = n !== cur;
    cur = n;
    slides.forEach(function (s, i) { s.classList.toggle('is-current', i + 1 === cur); });
    if (presenting) {
      try { history.replaceState(null, '', '#slide-' + cur); } catch (e) {}
      if (live) live.textContent = 'Slide ' + cur + ' of ' + total + ': ' + slides[cur - 1].querySelector('.slide-title').textContent;
    } else if (opts.scroll) {
      slides[cur - 1].scrollIntoView({ block: 'start' });
    }
    markActive();
    if (changed || opts.force) announce();
  }

  /* ---- scroll mode: the current slide is the one nearest the top third ---- */
  var ticking = false;
  function onScroll() {
    if (presenting || ticking) return;
    ticking = true;
    window.requestAnimationFrame(function () {
      ticking = false;
      var line = window.innerHeight * 0.33, best = 1, bestD = Infinity;
      slides.forEach(function (s, i) {
        var r = s.getBoundingClientRect();
        var d = (r.top <= line && r.bottom > line) ? 0 : Math.min(Math.abs(r.top - line), Math.abs(r.bottom - line));
        if (d < bestD) { bestD = d; best = i + 1; }
      });
      if (best !== cur) setCurrent(best);
    });
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  /* ---- present mode ---- */
  function enterPresent() {
    if (presenting) return;
    presenting = true;
    document.body.classList.add('presenting');
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    setCurrent(cur, { force: true });
    var el = document.documentElement;
    if (el.requestFullscreen) {
      el.requestFullscreen().then(function () { enteredFullscreen = true; }, function () {});
    }
  }
  var blank = document.createElement('div');
  blank.className = 'blank-screen'; blank.setAttribute('aria-hidden', 'true');
  document.body.appendChild(blank);
  function setBlank(kind) {
    var cur_ = blank.classList.contains('white') ? 'w' : blank.classList.contains('on') ? 'b' : '';
    var next = cur_ === kind ? '' : kind;
    blank.classList.toggle('on', !!next);
    blank.classList.toggle('white', next === 'w');
  }
  function unblank() { blank.classList.remove('on', 'white'); }

  function exitPresent() {
    if (!presenting) return;
    presenting = false;
    unblank();
    clearBuf();
    document.body.classList.remove('presenting');
    if (document.fullscreenElement && document.exitFullscreen) { enteredFullscreen = false; document.exitFullscreen().catch(function () {}); }
    enteredFullscreen = false;
    slides[cur - 1].scrollIntoView({ block: 'start' });
    var b = document.getElementById('present-btn');
    if (b) b.focus({ preventScroll: true });
  }
  document.addEventListener('fullscreenchange', function () {
    if (!document.fullscreenElement && presenting && enteredFullscreen) exitPresent();
  });

  /* ---- type a number, press Enter ---- */
  function showBuf() {
    if (!hud) return;
    hud.hidden = !buf;
    hud.textContent = buf ? 'Go to slide ' + buf + ' of ' + total + '  (Enter)' : '';
  }
  function clearBuf() { buf = ''; clearTimeout(bufTimer); showBuf(); }
  function pushDigit(d) {
    if (buf.length >= 3) buf = '';
    buf += d;
    clearTimeout(bufTimer);
    bufTimer = setTimeout(clearBuf, 5000);
    showBuf();
  }

  function openSpeaker() {
    if (!notesUrl) return;
    var w = window.open(notesUrl + '?follow=1', 'workshop-speaker', 'popup=yes,width=1100,height=820');
    if (w) { try { w.focus(); } catch (e) {} }
    setTimeout(announce, 600);
  }

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var t = e.target, tag = t && t.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || (t && t.isContentEditable)) return;
    var k = e.key;
    if (k === 'p' || k === 'P') { e.preventDefault(); if (presenting) exitPresent(); else enterPresent(); return; }
    if (k === 's' || k === 'S') { e.preventDefault(); openSpeaker(); return; }
    if (!presenting) return;
    if (k === 'b' || k === 'B' || k === '.') { e.preventDefault(); setBlank('b'); return; }
    if (k === 'w' || k === 'W') { e.preventDefault(); setBlank('w'); return; }
    if (k === 'Escape' && blank.classList.contains('on')) { e.preventDefault(); unblank(); return; }
    if (blank.classList.contains('on')) unblank();
    if (k >= '0' && k <= '9' && k.length === 1) { e.preventDefault(); pushDigit(k); return; }
    if (k === 'Enter') {
      e.preventDefault();
      if (buf) { var n = parseInt(buf, 10); clearBuf(); if (n >= 1) setCurrent(n); }
      return;
    }
    if (k === 'Backspace') { e.preventDefault(); buf = buf.slice(0, -1); showBuf(); return; }
    if (k === 'Escape') { e.preventDefault(); if (buf) clearBuf(); else exitPresent(); return; }
    if (k === 'ArrowRight' || k === 'ArrowDown' || k === 'PageDown' || (k === ' ' && !e.shiftKey)) { e.preventDefault(); setCurrent(cur + 1); return; }
    if (k === 'ArrowLeft' || k === 'ArrowUp' || k === 'PageUp' || (k === ' ' && e.shiftKey)) { e.preventDefault(); setCurrent(cur - 1); return; }
    if (k === 'Home') { e.preventDefault(); setCurrent(1); return; }
    if (k === 'End') { e.preventDefault(); setCurrent(total); return; }
  });

  /* click: right two thirds forward, left third back (present mode only) */
  deck.addEventListener('click', function (e) {
    if (!presenting || e.target.closest('a, button')) return;
    var x = e.clientX / window.innerWidth;
    setCurrent(x < 0.33 ? cur - 1 : cur + 1);
  });

  var pb = document.getElementById('present-btn');
  if (pb) pb.addEventListener('click', enterPresent);
  var sb = document.getElementById('speaker-btn');
  if (sb) sb.addEventListener('click', openSpeaker);
  var xb = document.getElementById('exit-present');
  if (xb) xb.addEventListener('click', exitPresent);

  /* ---- speaker window sync ---- */
  if (bc) {
    bc.onmessage = function (ev) {
      var m = ev.data || {};
      if (m.type === 'hello') announce();
      else if (m.type === 'goto' && typeof m.n === 'number') {
        setCurrent(m.n, { scroll: !presenting });
      }
    };
  }

  /* ---- initial slide from #slide-N ---- */
  var m = /^#slide-(\d+)$/.exec(location.hash || '');
  if (m) setCurrent(parseInt(m[1], 10)); else { setCurrent(1); }
  announce();
})();
