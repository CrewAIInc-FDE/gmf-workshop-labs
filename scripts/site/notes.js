/* Speaker notes page: prev/next, jump, follow the slides window, clock and timer. */
(function () {
  var data = JSON.parse(document.getElementById('deck-data').textContent);
  var slides = data.slides, total = slides.length;
  var cards = Array.prototype.slice.call(document.querySelectorAll('.ncard'));
  var params = new URLSearchParams(location.search);
  var popup = params.get('follow') === '1';
  var cur = 1;
  var followBox = document.getElementById('follow');
  var jump = document.getElementById('jump');
  var nextEl = document.getElementById('next');
  var paceEl = document.getElementById('pace');
  var prevBtn = document.getElementById('prev');
  var nextBtn = document.getElementById('next-btn');
  var bc = null;
  try { if ('BroadcastChannel' in window) bc = new BroadcastChannel('workshop-deck:' + data.module); } catch (e) {}

  if (popup) document.body.classList.add('follow-mode');
  followBox.checked = popup;
  if (!bc) { followBox.disabled = true; followBox.checked = false; }

  function clamp(n) { return Math.max(1, Math.min(total, n)); }

  function pace() {
    var t = slides[cur - 1].time;
    if (!t) { paceEl.textContent = ''; return; }
    var p = t.split(':'), target = new Date();
    target.setHours(parseInt(p[0], 10), parseInt(p[1], 10), 0, 0);
    var mins = Math.round((target - new Date()) / 60000);
    var txt = 'By ' + t + ': ';
    if (mins > 0) txt += mins + ' min to spare';
    else if (mins === 0) txt += 'right on time';
    else txt += (-mins) + ' min behind';
    paceEl.textContent = txt;
  }

  function show(n, opts) {
    opts = opts || {};
    n = clamp(n);
    cur = n;
    cards.forEach(function (c, i) {
      var on = i + 1 === cur;
      c.classList.toggle('is-current', on);
      if (on) c.setAttribute('aria-current', 'true'); else c.removeAttribute('aria-current');
    });
    if (!popup && opts.scroll !== false) cards[cur - 1].scrollIntoView({ block: 'start' });
    if (popup) window.scrollTo(0, 0);
    jump.value = String(cur);
    prevBtn.setAttribute('aria-disabled', cur === 1 ? 'true' : 'false');
    nextBtn.setAttribute('aria-disabled', cur === total ? 'true' : 'false');
    nextEl.textContent = cur < total ? 'Next: ' + (cur + 1) + '. ' + slides[cur].title : 'Last slide';
    pace();
    if (opts.fromUser && followBox.checked && bc) { try { bc.postMessage({ type: 'goto', n: cur }); } catch (e) {} }
  }

  function go(n) { show(n, { fromUser: true }); }
  prevBtn.addEventListener('click', function () { go(cur - 1); });
  nextBtn.addEventListener('click', function () { go(cur + 1); });
  document.getElementById('jump-form').addEventListener('submit', function (e) {
    e.preventDefault();
    var n = parseInt(jump.value, 10);
    if (n >= 1) go(n); else jump.value = String(cur);
    jump.blur();
  });
  jump.addEventListener('focus', function () { jump.select(); });

  document.addEventListener('keydown', function (e) {
    if (e.ctrlKey || e.metaKey || e.altKey) return;
    var tag = e.target && e.target.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { e.preventDefault(); go(cur + 1); }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { e.preventDefault(); go(cur - 1); }
  });

  if (bc) {
    bc.onmessage = function (ev) {
      var m = ev.data || {};
      if (m.type === 'slide' && followBox.checked && typeof m.n === 'number') show(m.n);
    };
    followBox.addEventListener('change', function () { if (followBox.checked) bc.postMessage({ type: 'hello' }); });
    if (followBox.checked) bc.postMessage({ type: 'hello' });
  }

  /* ---- clock and timer ---- */
  var clockEl = document.getElementById('clock'), timerEl = document.getElementById('timer');
  var tbtn = document.getElementById('timer-btn'), treset = document.getElementById('timer-reset');
  var elapsed = 0, startedAt = null;
  function two(n) { return (n < 10 ? '0' : '') + n; }
  function tick() {
    var d = new Date();
    clockEl.textContent = two(d.getHours()) + ':' + two(d.getMinutes());
    var ms = elapsed + (startedAt ? Date.now() - startedAt : 0), s = Math.floor(ms / 1000);
    var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60);
    timerEl.textContent = (h ? h + ':' + two(m) : m) + ':' + two(s % 60);
    pace();
  }
  tbtn.addEventListener('click', function () {
    if (startedAt) { elapsed += Date.now() - startedAt; startedAt = null; tbtn.textContent = 'Resume timer'; }
    else { startedAt = Date.now(); tbtn.textContent = 'Pause timer'; }
    tick();
  });
  treset.addEventListener('click', function () { elapsed = 0; startedAt = null; tbtn.textContent = 'Start timer'; tick(); });
  setInterval(tick, 1000);
  tick();

  var m = /^#n-(\d+)$/.exec(location.hash || '');
  show(m ? parseInt(m[1], 10) : 1, { scroll: !!m });
})();
