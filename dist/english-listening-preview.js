/* James Real. Original-format English cards; generated locally, with no upload. */
(function () {
  'use strict';
  const DATA = window.JR_ENGLISH_DATA;
  if (!DATA) return;
  const TYPES = {
    vocabulary: { label: 'Vocabulary', bg: '#efd6d5', fg: '#382d2e', border: '#9b4f53', ink: '#b82c30' },
    phrases: { label: 'Phrasal verbs', bg: '#f1dfcf', fg: '#3d3028', border: '#96633f', ink: '#ad5018' },
    idioms: { label: 'Idioms & slang', bg: '#efe6bd', fg: '#383426', border: '#806c27', ink: '#926a0c' },
    daily: { label: 'Life phrases', bg: '#dce6d8', fg: '#2d382e', border: '#526f4f', ink: '#1c5840' },
    reflection: { label: 'Quote', bg: '#dce5ee', fg: '#2c3540', border: '#4e6e8b', ink: '#244890' },
    grammar: { label: 'Grammar', bg: '#e7dfec', fg: '#382f40', border: '#7b628c', ink: '#503773' },
    smalltalk: { label: 'Small talk', bg: '#e3e1df', fg: '#353331', border: '#5f5b58', ink: '#25272c' },
    essay: { label: 'Essay', bg: '#f1eadc', fg: '#37322b', border: '#81735e', ink: '#81735d' }
  };
  const ALIASES = { phrasal: 'phrases', idiom: 'idioms', life: 'daily', quote: 'reflection', 'small-talk': 'smalltalk' };
  const LEVELS = [
    ['A1', 'Beginner', 'Start with the everyday.'], ['A2', 'Elementary', 'Build a little confidence.'],
    ['B1', 'Intermediate', 'Tell your own story.'], ['B2', 'Upper intermediate', 'Express your point of view.'],
    ['C1', 'Advanced', 'Find the precise words.'], ['C2', 'Proficient', 'Make room for nuance.']
  ];
  const DATES = (window.JR_ENGLISH_DATES || Object.keys(DATA)).slice().sort().reverse();
  const currentDate = window.jrToday?.() || DATES[0];
  const defaultDate = DATES.find(d=>d<=currentDate)||DATES.at(-1);
  let editionLoading = null;
  const params = new URLSearchParams(location.search);
  let date = DATES.includes(params.get('jr-date')) ? params.get('jr-date') : defaultDate;
  let level = LEVELS.some(l => l[0] === params.get('jr-level')) ? params.get('jr-level') : 'A1';
  let filter = TYPES[params.get('jr-type')] ? params.get('jr-type') : 'all';
  let completed = {};
  let storageAvailable = true;
  let speechId = '', speechGeneration = 0, currentUtterance = null;
  let paintGeneration = 0;
  const SAMPLE_DATE='2026-10-27';
  const LEVEL_PACES={A1:.75,A2:.80,B1:.85,B2:.90,C1:.95,C2:1};
  const sampleAudioByLevel=new Map(),samplePreparations=new Map();
  function prepareSampleAudio(){
    if(date!==SAMPLE_DATE||samplePreparations.has(level))return;
    const selectedLevel=level;
    const pending=fetch('assets/lesson-audio/'+SAMPLE_DATE+'/'+selectedLevel+'/manifest.json?v=quotestory1').then(r=>{if(!r.ok)throw Error('Sample not ready');return r.json();}).then(manifest=>{
      sampleAudioByLevel.set(selectedLevel,manifest);
      Object.values(manifest.cards).forEach(card=>{
        for(const url of [card.title,card.conversation,card.reading].filter(Boolean))window.JRVoicePlayer?.prepareFile(url).catch(()=>{});
      });
    }).catch(()=>{samplePreparations.delete(selectedLevel);});
    samplePreparations.set(selectedLevel,pending);
  }
  const KEY = 'james-real-english-progress-v1';
  const imageCache = new Map(), posterCache = new Map(), photoDataCache = new Map(), previewCache = new Map();
  const diagnostics = [];
  try { completed = JSON.parse(localStorage.getItem(KEY) || '{}'); if (!completed || Array.isArray(completed) || typeof completed !== 'object') completed = {}; }
  catch (_) { storageAvailable = false; }
  const escape = value => String(value == null ? '' : value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const text = value => Array.isArray(value) ? value.join(' ') : String(value || '');
  const typeOf = card => ALIASES[card.type || card.image] || card.type || card.image || 'vocabulary';
  const palette = card => TYPES[typeOf(card)] || TYPES.vocabulary;
  const unit = () => DATA[date]?.[level];
  const count = () => unit().cards.filter(c => completed[c.id]).length;
  const cardById = id => unit()?.cards.find(c => c.id === id);
  const dateOf = card => /^\d{4}-\d{2}-\d{2}/.exec(card.id)?.[0] || date;
  const levelOf = card => /-(A1|A2|B1|B2|C1|C2)-/.exec(card.id)?.[1] || card.level || level;
  const fileName = (card, ink) => ['Everyday English',levelOf(card),dateOf(card),typeOf(card)==='phrases'?'Phrasal verb':palette(card).label,String(card.categoryNumber || card.number).padStart(2,'0')].join(' - ') + (ink?' - ink saving':'') + '.png';
  function announce(message) { const el = document.getElementById('jr-en-status'); if (el) el.textContent = message; }
  function saveProgress() { try { localStorage.setItem(KEY, JSON.stringify(completed)); storageAvailable = true; } catch (_) { storageAvailable = false; } }
  function exerciseText(card) { return text(card.exercise).split(/\n?Model Answer\s*:/i)[0].trim(); }
  function answerText(card) { return text(card.answer) || text(card.exercise).split(/Model Answer\s*:/i).slice(1).join('Model Answer:').trim(); }
  function roles(card) { return card.paragraphRoles || ['Introduction — main idea', 'Body 1 — point + example', 'Body 2 — point + example', 'Conclusion — bring the ideas together']; }
  function structureText(card) { return 'Introduction → Body 1 → Body 2 → Conclusion. ' + text(card.structure); }
  function answerHTML(card) { return '<details class="jr-en-answer"><summary>Reveal model answer <span aria-hidden="true">＋</span></summary><p>' + escape(answerText(card)) + '</p></details>'; }
  function guideHTML(card) { return typeOf(card) === 'essay' ? '<details class="jr-en-writing-guide"><summary>A four-paragraph writing guide <span aria-hidden="true">＋</span></summary><ol>' + roles(card).map(r => '<li>' + escape(text(r)) + '</li>').join('') + '</ol><p>' + escape(card.structure) + '</p></details>' : ''; }

  function sections(card) {
    if(typeOf(card)==='reflection'&&card.quoteBackground)return [['The story',text(card.quoteBackground)],['A closer look',text(card.quoteCloserLook)],['Your turn',exerciseText(card)]];
    const rows = [];
    if (card.meaning) rows.push(['Meaning', text(card.meaning)]);
    if (['vocabulary','phrases','idioms','daily','reflection'].includes(typeOf(card)) && card.synonyms?.length) rows.push(['Synonyms', (Array.isArray(card.synonyms) ? card.synonyms.join('; ') : text(card.synonyms)) + (card.synonymNote ? '\n' + text(card.synonymNote) : '')]);
    if (card.example) rows.push(['In context', text(card.example)]);
    if (card.notes) rows.push(['Usage note', text(card.notes)]);
    if (card.conversation) rows.push(['Conversation', text(card.conversation).replace(/\\n/g, '\n')]);
    rows.push(['Your turn', exerciseText(card)]);
    return rows;
  }
  function accessibleHTML(card) {
    const details = [];
    if (card.ipa) details.push('<p class="jr-en-word-meta">US ' + escape(card.ipa) + ' · ' + escape(card.partOfSpeech) + '</p>');
    if (card.wordForms) details.push('<p>' + escape(card.wordForms) + '</p>');
    if (typeOf(card) === 'essay') {
      details.push('<h4>Meaning</h4><p>' + escape(card.meaning) + '</p>');
      (card.paragraphs || []).forEach((p, i) => details.push('<h4>' + (i + 1) + ' · ' + roles(card)[i] + '</h4><p>' + escape(text(p)) + '</p>'));
      if (card.structure) details.push('<h4>Build your own</h4><p>' + escape(structureText(card)) + '</p>');
      if (card.notes) details.push('<h4>Usage note</h4><p>' + escape(card.notes) + '</p>');
      details.push('<h4>Your turn</h4><p>' + escape(exerciseText(card)) + '</p>');
    } else sections(card).forEach(([label, copy]) => details.push('<h4>' + label + '</h4><p>' + escape(copy) + '</p>'));
    return '<details class="jr-en-transcript"><summary>Read the complete card as text <span aria-hidden="true">＋</span></summary><div lang="en"><h3>' + escape(card.title) + '</h3>' + details.join('') + '</div></details>';
  }
  function cardHTML(card) {
    const type = typeOf(card), isEssay = type === 'essay';
    const done = !!completed[card.id];
    return `<article class="jr-en-card jr-en-${type}${done ? ' is-complete' : ''}" data-jr-card="${escape(card.id)}" aria-label="${escape(palette(card).label + ': ' + card.title)}">
      <button class="jr-en-poster-open" type="button" data-jr-do="preview" data-jr-id="${escape(card.id)}" aria-label="Open full-size ${escape(card.title)} card"><span class="jr-en-poster-loading" data-jr-loading="${escape(card.id)}">Preparing your complete ${escape(palette(card).label.toLowerCase())} card…</span><img class="jr-en-poster" id="jr-poster-${escape(card.id)}" width="${isEssay ? 1434 : 660}" height="${isEssay ? 660 : 1434}" alt="${escape(card.title)}. ${escape(palette(card).label)} card. Full accessible text follows." hidden></button>
      ${card.quoteSourceURL ? `<p class="jr-en-photo-source">Quote: <a href="${escape(card.quoteSourceURL)}" target="_blank" rel="noopener noreferrer">${escape(card.attribution||[card.quoteAuthor,card.quoteWork,'Published '+card.quoteYear].join(' · '))}</a></p>` : ''}
      ${card.photoCredit ? `<p class="jr-en-photo-source">Photo: <a href="${escape(card.photoCredit.sourceURL)}" target="_blank" rel="noopener noreferrer">${escape(card.photoCredit.credit)}</a></p>` : ''}
      <div class="jr-en-card-tools"><div class="jr-en-card-top"><span>${escape(palette(card).label)}</span><b>${String(card.number).padStart(2, '0')} / 11 · ${level}</b></div>
      <div class="jr-en-audio-actions"><button type="button" data-jr-do="speak-title" data-jr-id="${escape(card.id)}" aria-pressed="false">▷ Listen title</button>${card.conversation ? `<button type="button" data-jr-do="speak-conversation" data-jr-id="${escape(card.id)}" aria-pressed="false">▷ Listen conversation</button>` : ''}<button type="button" data-jr-do="speak-all" data-jr-id="${escape(card.id)}" aria-pressed="false">▷ Listen ${isEssay ? 'essay' : card.quoteBackground ? 'reading' : 'all'}</button></div>
      <details class="jr-en-export"><summary>Save, share or print</summary><div class="jr-en-file-actions"><button type="button" data-jr-do="share" data-jr-id="${escape(card.id)}">↗ Share PNG</button><button type="button" data-jr-do="save" data-jr-id="${escape(card.id)}">↓ Save PNG</button><button type="button" data-jr-do="print" data-jr-id="${escape(card.id)}">▤ Print</button><button type="button" data-jr-do="print-ink" data-jr-id="${escape(card.id)}">▤ Print · ink saving</button></div></details>
      <div class="jr-en-practice"><h4>Your turn</h4><p>${escape(exerciseText(card))}</p>${answerHTML(card)}</div>${guideHTML(card)}${accessibleHTML(card)}<button type="button" class="jr-en-done${done ? ' is-done' : ''}" data-jr-do="done" data-jr-id="${escape(card.id)}" aria-pressed="${done}">${done ? '✓ Completed' : '○ Mark as complete'}</button></div></article>`;
  }
  let subscriptionDraft={email:'',levels:null,consent:false};
  const SUBSCRIPTION_API='https://br-winter-pond-b5yda82s-everydayenglish.compute.c-7.us-east-2.aws.neon.tech';
  function subscriptionHTML(){
    const selected=subscriptionDraft.levels||[level];
    return `<section class="jr-en-subscribe" aria-labelledby="jr-en-sub-title"><p class="jr-en-kicker">YOUR DAILY PRACTICE</p><h2 id="jr-en-sub-title">Make room for a little English.</h2><p>Choose one or more levels. Each selected level arrives as a separate email with eleven cards, at around 7 a.m. Pacific Time.</p><form id="jr-en-subscribe-form"><label for="jr-en-sub-email">Email address</label><input id="jr-en-sub-email" name="email" type="email" autocomplete="email" maxlength="254" required value="${escape(subscriptionDraft.email)}"><fieldset><legend>Your levels</legend><div class="jr-en-sub-levels">${LEVELS.map(l=>`<label><input type="checkbox" name="levels" value="${l[0]}" ${selected.includes(l[0])?'checked':''}> ${l[0]}</label>`).join('')}</div></fieldset><div class="jr-en-honey" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div><label class="jr-en-sub-consent"><input type="checkbox" name="consent" required ${subscriptionDraft.consent?'checked':''}> I would like to receive these daily English lessons. I can change levels or unsubscribe at any time.</label><button type="submit">Subscribe to my selected levels ↗</button><p class="jr-en-sub-status" role="status" aria-live="polite"></p><small>We will send a confirmation link before activating your subscription.</small></form></section>`;
  }
  document.addEventListener('input',event=>{
    const form=event.target.closest('#jr-en-subscribe-form');if(!form)return;
    subscriptionDraft={email:form.elements.email.value,levels:[...form.querySelectorAll('[name="levels"]:checked')].map(x=>x.value),consent:form.elements.consent.checked};
  });
  document.addEventListener('submit',async event=>{
    const form=event.target;if(form.id!=='jr-en-subscribe-form')return;event.preventDefault();
    const selected=[...form.querySelectorAll('[name="levels"]:checked')].map(x=>x.value),status=form.querySelector('[role="status"]'),button=form.querySelector('button[type="submit"]');
    if(!selected.length){status.textContent='Please select at least one level.';return;}
    if(!form.reportValidity())return;
    button.disabled=true;status.textContent='Sending your confirmation…';
    try{
      const response=await fetch(SUBSCRIPTION_API+'/subscribe',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email:form.elements.email.value,levels:selected,consent:form.elements.consent.checked,website:form.elements.website.value})});
      const result=await response.json();if(!response.ok)throw new Error(result.error||'The request could not be completed.');
      status.textContent=result.message;subscriptionDraft={email:'',levels:selected,consent:false};
      form.elements.email.value='';form.elements.consent.checked=false;
    }catch(error){status.textContent=error.message==='Failed to fetch'?'The subscription service could not be reached. Please try again later.':error.message;}
    finally{button.disabled=false;}
  });
  function pageBody() {
    const edition = unit(), info = LEVELS.find(l => l[0] === level);
    if(!edition) return '<div class="page-head"><h1>Everyday English</h1><p role="status">Loading your prepared '+level+' edition for '+date+'…</p><button type="button" data-jr-do="retry">Try again</button></div>';
    const visible = edition.cards.filter(c => filter === 'all' || typeOf(c) === filter);
    return `<div class="page-head jr-en-heading"><div><p class="jr-en-kicker">EDUCATION / EVERYDAY ENGLISH</p><h1>English for<br><em>everyday life.</em></h1><p class="jr-en-intro">Choose your level. Read and listen, then answer “Your turn” before checking the model answer.<br>Finish with an essay that shows how four paragraphs build one clear argument.</p><p class="jr-en-speakers">Your speakers: ${escape(window.JR_ENGLISH_SPEAKERS?.[level]?.teacher.name||'')} &amp; ${escape(window.JR_ENGLISH_SPEAKERS?.[level]?.partner.name||'')}. ${date===SAMPLE_DATE?level+' listening pace: '+Math.round(LEVEL_PACES[level]*100)+'%. Smooth, continuous conversations.':'First playback downloads the voice data; later visits can reuse it.'}</p><p><a class="jr-en-voice-preview" href="voice-preview.html" target="_blank" rel="noopener">Meet the twelve American English voices ↗</a></p></div><aside class="jr-en-summary" aria-label="Eleven cards per edition, six levels from A1 to C2"><p class="jr-en-summary-label">YOUR DAILY EDITION</p><div class="jr-en-summary-count"><strong>11</strong><span>cards to read,<br>listen &amp; practise</span></div><div class="jr-en-summary-levels"><span>A1 — C2</span><span>Six levels</span></div></aside></div>
      <div class="jr-en-levels" role="group" aria-label="English level">${LEVELS.map(l => `<button type="button" class="jr-en-level${l[0] === level ? ' is-active' : ''}" data-jr-do="level" data-jr-level="${l[0]}" aria-pressed="${l[0] === level}"><span>${l[0]}</span><b>${l[1]}</b><small>${l[2]}</small></button>`).join('')}</div>
      <section class="jr-en-edition" aria-label="Selected English edition"><div><p class="jr-en-kicker">${level} · ${info[1].toUpperCase()} / SELECTED EDITION</p><h2>${escape(edition.theme)}</h2><p>2 vocabulary · 2 phrasal verbs · 2 idioms · 1 life phrase · 1 quote · 1 grammar · 1 small talk · 1 four-paragraph essay.</p></div><div class="jr-en-edition-tools"><label for="jr-en-date">Find an edition by date · Pacific Time</label><input id="jr-en-date" data-jr-date type="date" value="${date}" min="2026-01-01" max="2026-12-31" aria-describedby="jr-en-date-help"><small id="jr-en-date-help">Enter or choose a date in 2026.</small></div></section>
      <div class="jr-en-bulk-actions"><button type="button" data-jr-do="zip">↓ Download all 11 PNG cards · ZIP</button><button type="button" data-jr-do="print-all">▤ Print all 11 cards</button><button type="button" data-jr-do="print-all-ink">▤ Print all · ink saving</button></div>
      <div class="jr-en-progress-row"><div class="jr-en-progress-copy"><span>YOUR PROGRESS</span><b id="jr-en-progress-label">${count()} / 11 completed</b></div><progress id="jr-en-progress" value="${count()}" max="11" aria-label="Completed lessons">${count()} / 11</progress><span class="jr-en-progress-note">${storageAvailable ? 'Progress stays in this browser.' : 'Progress is available for this visit only.'}</span></div>
      <div class="jr-en-filter-row"><div class="jr-en-filters" role="group" aria-label="Card category"><button type="button" data-jr-do="filter" data-jr-filter="all" aria-pressed="${filter === 'all'}" class="${filter === 'all' ? 'is-active' : ''}">All 11 cards</button>${Object.entries(TYPES).map(([key, value]) => `<button type="button" data-jr-do="filter" data-jr-filter="${key}" aria-pressed="${filter === key}" class="${filter === key ? 'is-active' : ''}">${value.label}</button>`).join('')}</div><span class="jr-en-visible-count">${visible.length} ${visible.length===1?"card":"cards"}</span></div>
      <p id="jr-en-status" class="jr-en-status" role="status" aria-live="polite"></p><div class="jr-en-grid">${visible.map(cardHTML).join('')}</div>
      ${subscriptionHTML()}<div class="jr-en-footnote"><span class="jr-en-footnote-mark" aria-hidden="true">Aa</span><div><strong>A little English, every day.</strong><p>Explore January 1 to December 31, 2026. Every date offers six levels and eleven cards. Return to familiar themes for practice, and explore seasonal language around selected holidays. The original lesson archive remains available below.</p><p>Try one new expression in a sentence of your own. For the essay, follow the writing guide: introduction, two supporting paragraphs, and conclusion.</p></div></div>`;
  }
  window.jrEnglishPage = () => '<section id="jr-english" class="jr-english" lang="en" translate="no">' + pageBody() + '</section>';
  function renderLocal(focus) {
    stopSpeech();
    const root = document.getElementById('jr-english');
    if (!root) return;
    root.innerHTML = pageBody();
    if (focus) root.querySelector(focus)?.focus({ preventScroll: true });
    window.jrEnglishInit();
  }
  function persistSelection() {
    const url = new URL(location.href);
    url.searchParams.set('jr-level', level); url.searchParams.set('jr-date', date);
    if(filter==='all')url.searchParams.delete('jr-type');else url.searchParams.set('jr-type',filter);
    history.replaceState(null, '', url);
  }
  function loadIllustration(card) {
    const source = card.illustration || 'assets/english-illustrations/2026-10-11/' + String(card.number).padStart(2, '0') + '.png';
    if (!imageCache.has(source)) imageCache.set(source, new Promise((resolve, reject) => {
      const img = new Image(); img.crossOrigin = 'anonymous';
      img.onload = () => resolve(img); img.onerror = () => reject(new Error('Illustration could not load: ' + source)); img.src = source;
    }));
    return imageCache.get(source);
  }
  function font(ctx, size, bold) { ctx.font = (bold ? '700 ' : '400 ') + size + 'px Arial, sans-serif'; }
  function wrap(ctx, value, maxWidth) {
    const lines = [];
    String(value).split('\n').forEach(paragraph => {
      let line = '';
      for (const word of paragraph.split(/\s+/)) {
        if (!word) continue;
        const trial = line ? line + ' ' + word : word;
        if (ctx.measureText(trial).width <= maxWidth) { line = trial; continue; }
        if (line) lines.push(line);
        line = '';
        for (const char of word) {
          if (ctx.measureText(line + char).width > maxWidth && line) { lines.push(line); line = ''; }
          line += char;
        }
      }
      lines.push(line);
    });
    return lines;
  }
  function roundedRect(ctx, x, y, width, height, radius) {
    ctx.beginPath(); ctx.moveTo(x + radius, y); ctx.lineTo(x + width - radius, y); ctx.quadraticCurveTo(x + width, y, x + width, y + radius); ctx.lineTo(x + width, y + height - radius); ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height); ctx.lineTo(x + radius, y + height); ctx.quadraticCurveTo(x, y + height, x, y + height - radius); ctx.lineTo(x, y + radius); ctx.quadraticCurveTo(x, y, x + radius, y); ctx.closePath();
  }
  function baseCanvas(width, height, card, ink) {
    const canvas = document.createElement('canvas'); canvas.width = width; canvas.height = height;
    const ctx = canvas.getContext('2d'), colors = palette(card);
    ctx.textBaseline = 'alphabetic'; ctx.fillStyle = '#f7f4eb'; ctx.fillRect(0, 0, width, height);
    const essay = width > 1000, edge = essay ? 14 : 7, inset = essay ? 24 : 12;
    ctx.fillStyle = ink ? '#ffffff' : colors.bg; roundedRect(ctx, edge, edge, width - edge * 2, height - edge * 2, essay ? 10 : 5); ctx.fill();
    ctx.strokeStyle = colors.border; ctx.lineWidth = essay ? 5 : 2.5; ctx.stroke();
    ctx.strokeStyle = ink ? '#fff' : '#f7f1e5'; ctx.lineWidth = essay ? 10 : 5; roundedRect(ctx, inset, inset, width - inset * 2, height - inset * 2, essay ? 6 : 3); ctx.stroke();
    return { canvas, ctx, colors };
  }
  function drawPortrait(card, illustration, ink) {
    const { canvas, ctx, colors } = baseCanvas(660, 1434, card, ink);
    ctx.fillStyle = colors.fg; font(ctx, 16, true); ctx.fillText('Everyday English - ' + colors.label, 28, 55);
    font(ctx, 13, false); ctx.textAlign = 'right'; ctx.fillText(dateOf(card) + ' · ' + levelOf(card) + ' · PT', 632, 55); ctx.textAlign = 'left';
    drawCover(ctx, illustration, 28, 80, 604, 310);
    const rows = sections(card);
    function layout(scale) {
      const titleSize = (typeOf(card) === 'vocabulary' ? 40 : 36) * scale, titleLeading = (typeOf(card) === 'vocabulary' ? 48 : 43) * scale, size = 23.5 * scale, leading = 30.5 * scale, labelSize = 14.5 * scale, gap = 24 * scale;
      font(ctx, titleSize, true); const title = wrap(ctx, card.title, 604);
      let y = 425 + title.length * titleLeading;
      const meta = [];
      if (card.ipa) meta.push(['US ' + text(card.ipa) + '   ' + text(card.partOfSpeech), 23.5 * scale]);
      if (card.wordForms) meta.push([text(card.wordForms), 19 * scale]);
      const wordMeta = meta.map(([copy, s]) => { font(ctx, s, false); const lines = wrap(ctx, copy, 604); const block = { y, size: s, lines }; y += lines.length * s * 1.22; return block; });
      y += 34 * scale;
      const blocks = rows.map(([label, copy]) => { font(ctx, size, false); const lines = wrap(ctx, copy, 604); const block = { label, lines, y }; y += labelSize * 1.16 + lines.length * leading + gap; return block; });
      return { scale, titleSize, titleLeading, size, leading, labelSize, title, wordMeta, blocks, bottom: y - gap };
    }
    let scale = 1, plan = layout(scale);
    while (plan.bottom > 1375 && scale > 0.48) { scale -= 0.02; plan = layout(scale); }
    if (plan.bottom > 1375) throw new Error('Card contains too much text: ' + card.id);
    ctx.fillStyle = colors.fg; font(ctx, plan.titleSize, true);
    plan.title.forEach((line, i) => ctx.fillText(line, 28, 425 + plan.titleSize + i * plan.titleLeading));
    plan.wordMeta.forEach(block => { font(ctx, block.size, false); block.lines.forEach((line, i) => ctx.fillText(line, 28, block.y + block.size + i * block.size * 1.22)); });
    plan.blocks.forEach(block => {
      font(ctx, plan.labelSize, true); ctx.fillStyle = '#8b8782'; ctx.fillText(block.label.toUpperCase(), 28, block.y + plan.labelSize);
      ctx.fillStyle = colors.fg; font(ctx, plan.size, false);
      block.lines.forEach((line, i) => ctx.fillText(line, 28, block.y + plan.labelSize * 1.16 + plan.size + i * plan.leading));
    });
    font(ctx, 10, false); ctx.fillStyle = colors.border; ctx.fillText('JAMES REAL  ·  ' + levelOf(card) + '  ·  CARD ' + String(card.number).padStart(2, '0') + ' / 11', 28, 1404);
    diagnostics.push({ id: card.id, kind: 'portrait', size: plan.size, bottom: plan.bottom, limit: 1375, ink: !!ink });
    return canvas;
  }
  function highlightList(card, peers) {
    let list = (card.highlights || []).map(h => typeof h === 'string' ? { text: h, type: 'vocabulary' } : { text: h.text || h.phrase || h.word, type: ALIASES[h.type || h.category] || h.type || h.category || 'vocabulary' });
    if (!list.length) list = peers.filter(c => typeOf(c) !== 'essay').map(c => ({ text: c.title, type: typeOf(c) }));
    return list.filter(h => h.text).sort((a, b) => b.text.length - a.text.length);
  }
  function richLines(ctx, copy, width, highlights, foreground) {
    const value = String(copy), lower = value.toLowerCase(), ranges = [];
    for (const h of highlights) {
      let from = 0, index;
      while ((index = lower.indexOf(h.text.toLowerCase(), from)) !== -1) {
        const end = index + h.text.length;
        if (!/[a-z]/i.test(value[index - 1] || '') && !/[a-z]/i.test(value[end] || ''))
          ranges.push({ start: index, end, color: (TYPES[h.type] || TYPES.vocabulary).ink });
        from = end;
      }
    }
    const lines = [[]]; let x = 0, offset = 0;
    // Wrap complete words, including punctuation, even at a highlight boundary.
    for (const token of value.match(/\s+|\S+/g) || []) {
      const space = /^\s+$/.test(token), measured = ctx.measureText(token).width;
      const range = ranges.find(r => r.start < offset + token.length && r.end > offset);
      const color = range ? range.color : foreground;
      offset += token.length;
      if (x + measured > width && x > 0 && !space) { lines.push([]); x = 0; }
      if (space && x === 0) continue;
      lines[lines.length - 1].push({ text: token, color, x }); x += measured;
    }
    return lines;
  }
  // Uniform scaling and centred cropping preserve the original illustration proportions.
  function drawCover(ctx, image, x, y, w, h) {
    const scale = Math.max(w / image.width, h / image.height);
    const sw = w / scale, sh = h / scale;
    ctx.drawImage(image, (image.width - sw) / 2, (image.height - sh) / 2, sw, sh, x, y, w, h);
  }
  function drawEssay(card, illustration, ink, peers) {
    const { canvas, ctx, colors } = baseCanvas(1434, 660, card, ink);
    ctx.fillStyle = colors.fg; font(ctx, 23, true); ctx.fillText('Everyday English - Essay', 42, 42);
    font(ctx, 17, false); ctx.textAlign = 'right'; ctx.fillText(dateOf(card) + ' · ' + levelOf(card) + ' · PT', 1392, 42); ctx.textAlign = 'left';
    drawCover(ctx, illustration, 1132, 70, 260, 134);
    const highlights = highlightList(card, peers);
    function layout(scale) {
      const size = 25 * scale, leading = 30 * scale, labelSize = 17 * scale, gap = 14 * scale;
      font(ctx, 34 * scale, true); const title = wrap(ctx, card.title, 1050);
      let y = 66 + title.length * 40 * scale;
      const rows = [];
      if (card.meaning) rows.push({ label: '', text: text(card.meaning), small: true, width: 1050 });
      (card.paragraphs || []).forEach((p, i) => rows.push({ label: (i + 1) + ' · ' + text(roles(card)[i]).toUpperCase(), text: text(p), width: i === 0 ? 1050 : 1350, rich: true }));
      if (card.structure) rows.push({ label: 'BUILD YOUR OWN', text: structureText(card), small: true, width: 1350 });
      if (card.notes) rows.push({ label: 'USAGE NOTE', text: text(card.notes), small: true, width: 1350 });
      rows.push({ label: 'YOUR TURN', text: exerciseText(card), small: true, width: 1350 });
      const blocks = rows.map(row => {
        const blockSize = row.small ? 18 * scale : size, blockLeading = row.small ? 22 * scale : leading;
        font(ctx, blockSize, false);
        const availableWidth = y < 207 && row.width === 1350 ? 1050 : row.width;
        const lines = row.rich ? richLines(ctx, row.text, availableWidth, highlights, colors.fg) : wrap(ctx, row.text, availableWidth);
        const block = { ...row, y, lines, size: blockSize, leading: blockLeading };
        y += (row.label ? labelSize * 1.18 : 0) + lines.length * blockLeading + gap;
        return block;
      });
      return { scale, size, leading, labelSize, title, blocks, bottom: y - gap };
    }
    let scale = 1, plan = layout(scale);
    while (plan.bottom > 622 && scale > 0.45) { scale -= 0.02; plan = layout(scale); }
    if (plan.bottom > 622) throw new Error('Essay contains too much text: ' + card.id);
    font(ctx, 34 * scale, true); ctx.fillStyle = colors.fg;
    plan.title.forEach((line, i) => ctx.fillText(line, 42, 66 + 34 * scale + i * 40 * scale));
    plan.blocks.forEach(block => {
      let y = block.y;
      if (block.label) { font(ctx, plan.labelSize, true); ctx.fillStyle = '#8c877c'; ctx.fillText(block.label, 42, y + plan.labelSize); y += plan.labelSize * 1.18; }
      font(ctx, block.size, false); ctx.fillStyle = colors.fg;
      block.lines.forEach((line, i) => {
        const baseline = y + block.size + i * block.leading;
        if (block.rich) line.forEach(token => { ctx.fillStyle = token.color; ctx.fillText(token.text, 42 + token.x, baseline); });
        else { ctx.fillStyle = colors.fg; ctx.fillText(line, 42, baseline); }
      });
    });
    font(ctx, 10, false); ctx.fillStyle = colors.border; ctx.fillText('JAMES REAL · ' + levelOf(card) + ' · CARD 11 / 11 · COLOR LINKS CONNECT TODAY’S LESSONS', 42, 638);
    diagnostics.push({ id: card.id, kind: 'essay', size: plan.size, bottom: plan.bottom, limit: 622, ink: !!ink });
    return canvas;
  }
  async function storedSVG(card, ink, includeAnswer) {
    const source = includeAnswer ? card.downloadPoster : card.poster;
    if (!source) throw new Error('The stored card is unavailable. Please refresh.');
    const response = await fetch(source + '?format=quote-readings2026-v2');
    if (!response.ok) throw new Error('The complete card could not load.');
    let svg = await response.text();
    if (svg.includes('__JR_PHOTO__')) {
      const asset = card.photoCredit.asset;
      if (!photoDataCache.has(asset)) photoDataCache.set(asset,(async()=>{
        const r=await fetch(asset); if(!r.ok) throw new Error('The photograph could not load.');
        const blob=await r.blob();
        return new Promise((resolve,reject)=>{const reader=new FileReader();reader.onload=()=>resolve(reader.result);reader.onerror=reject;reader.readAsDataURL(blob);});
      })());
      svg=svg.replaceAll('__JR_PHOTO__',await photoDataCache.get(asset));
    }
    if (ink) svg = svg.replaceAll('fill="' + palette(card).bg + '"', 'fill="#ffffff"');
    return svg;
  }
  function previewPoster(card) {
    if(!previewCache.has(card.id)) previewCache.set(card.id,storedSVG(card,false,false).then(svg=>({url:URL.createObjectURL(new Blob([svg],{type:'image/svg+xml'}))})));
    return previewCache.get(card.id);
  }
  function poster(card, ink, includeAnswer = true) {
    const source = includeAnswer ? card.downloadPoster : card.poster;
    const key = card.id + ':' + !!ink + ':' + includeAnswer + ':' + source;
    if (posterCache.has(key)) return posterCache.get(key);
    const promise = (async () => {
      const svg = await storedSVG(card,ink,includeAnswer);
      const svgURL = URL.createObjectURL(new Blob([svg], {type:'image/svg+xml'}));
      try {
        const image = await new Promise((resolve,reject) => { const i = new Image(); i.onload=()=>resolve(i); i.onerror=reject; i.src=svgURL; });
        const canvas=document.createElement('canvas'); canvas.width=image.naturalWidth; canvas.height=image.naturalHeight;
        canvas.getContext('2d').drawImage(image,0,0);
        const blob=await new Promise((resolve,reject)=>canvas.toBlob(b=>b?resolve(b):reject(new Error('PNG export failed')),'image/png'));
        const file=new File([blob],fileName(card,ink),{type:'image/png'});
        return {file,url:URL.createObjectURL(file),width:canvas.width,height:canvas.height};
      } finally { URL.revokeObjectURL(svgURL); }
    })();
    posterCache.set(key,promise); promise.catch(()=>posterCache.delete(key)); return promise;
  }
  window.jrEnglishInit = function () {
    const root = document.getElementById('jr-english');
    if (!root) { stopSpeech(); return; }
    prepareSampleAudio();
    if(!unit()) {
      const requestedDate=date;
      if(editionLoading===requestedDate)return;
      editionLoading=requestedDate;
      fetch('data/english-levels/'+requestedDate+'.json?format=quote-readings2026-v2').then(r=>{if(!r.ok)throw Error();return r.json()}).then(data=>{
        DATA[requestedDate]=data;
        if(date===requestedDate&&document.getElementById('jr-english'))renderLocal();
      }).catch(()=>{if(date===requestedDate){root.innerHTML='<h1>Everyday English</h1><p role="status">This stored edition could not load.</p><button type="button" data-jr-do="retry">Try again</button>';}}).finally(()=>{if(editionLoading===requestedDate)editionLoading=null});
      return;
    }
    prepareQuoteAudio();
    const generation = ++paintGeneration;
    unit().cards.filter(c => filter === 'all' || typeOf(c) === filter).forEach(card => {
      previewPoster(card).then(result => {
        if (generation !== paintGeneration) return;
        const img = document.getElementById('jr-poster-' + card.id); if (!img) return;
        img.src = result.url; img.hidden = false;
        root.querySelector('[data-jr-loading="' + card.id + '"]')?.remove();
      }).catch(() => {
        if (generation !== paintGeneration) return;
        const message = root.querySelector('[data-jr-loading="' + card.id + '"]');
        if (message) message.textContent = 'The card image could not load. The complete lesson is available in the text below.';
        root.querySelector('[data-jr-card="' + card.id + '"] .jr-en-transcript')?.setAttribute('open', '');
        announce('A card illustration could not load. Please refresh; complete lesson text is still available.');
      });
    });
  };
  function download(file) { const url = URL.createObjectURL(file), link = document.createElement('a'); link.href = url; link.download = file.name; document.body.appendChild(link); link.click(); link.remove(); setTimeout(() => URL.revokeObjectURL(url), 60000); }
  async function preview(card) {
    const result = await poster(card, false, false);
    const downloadResult = await poster(card, false, true);
    document.getElementById('jr-en-preview')?.remove();
    const dialog = document.createElement('dialog'); dialog.id = 'jr-en-preview';
    dialog.innerHTML = '<div class="jr-en-preview-head"><strong>' + escape(card.title) + '</strong><button type="button" data-jr-close>Close ×</button></div><img src="' + result.url + '" alt="' + escape(card.title) + ' full card"><p><a href="' + downloadResult.url + '" download="' + escape(result.file.name) + '">↓ Download complete PNG</a></p>';
    dialog.querySelector('[data-jr-close]').onclick = () => { dialog.close(); dialog.remove(); };
    dialog.addEventListener('click', event => { if (event.target === dialog) { dialog.close(); dialog.remove(); } });
    dialog.addEventListener('cancel', () => dialog.remove()); document.body.appendChild(dialog); dialog.showModal();
  }
  function crc32(bytes) { let crc = 0xffffffff; for (const byte of bytes) { crc ^= byte; for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0); } return (crc ^ 0xffffffff) >>> 0; }
  async function zipCards(cards, editionDate, editionLevel) {
    const files = await Promise.all(cards.map(async card => (await poster(card, false)).file));
    if (files.length !== 11 || new Set(files.map(f => f.name)).size !== 11) throw new Error('A complete set of eleven cards is required.');
    const parts = [], directory = [], encoder = new TextEncoder(); let offset = 0, directorySize = 0;
    const [year, month, day] = editionDate.split('-').map(Number), stamp = ((year - 1980) << 9) | (month << 5) | day;
    for (const file of files) {
      const name = encoder.encode(file.name), bytes = new Uint8Array(await file.arrayBuffer()), checksum = crc32(bytes);
      if (bytes[0] !== 137 || bytes[1] !== 80 || bytes[2] !== 78 || bytes[3] !== 71) throw new Error('Invalid PNG.');
      const local = new Uint8Array(30), l = new DataView(local.buffer); l.setUint32(0, 0x04034b50, true); l.setUint16(4, 20, true); l.setUint16(6, 0x0800, true); l.setUint16(12, stamp, true); l.setUint32(14, checksum, true); l.setUint32(18, bytes.length, true); l.setUint32(22, bytes.length, true); l.setUint16(26, name.length, true);
      const central = new Uint8Array(46), c = new DataView(central.buffer); c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint16(8, 0x0800, true); c.setUint16(14, stamp, true); c.setUint32(16, checksum, true); c.setUint32(20, bytes.length, true); c.setUint32(24, bytes.length, true); c.setUint16(28, name.length, true); c.setUint32(42, offset, true);
      parts.push(local, name, bytes); directory.push(central, name); offset += local.length + name.length + bytes.length; directorySize += central.length + name.length;
    }
    const end = new Uint8Array(22), endView = new DataView(end.buffer); endView.setUint32(0, 0x06054b50, true); endView.setUint16(8, 11, true); endView.setUint16(10, 11, true); endView.setUint32(12, directorySize, true); endView.setUint32(16, offset, true);
    return new File([...parts, ...directory, end], 'Everyday English - ' + editionLevel + ' - ' + editionDate + '.zip', { type: 'application/zip' });
  }
  async function printCards(cards, ink) {
    // Open synchronously while the click is active, then populate once every PNG is ready.
    const popup = window.open('', '_blank'); if (!popup) { announce('Allow the print window in your browser, then try again.'); return; }
    popup.document.write('<!doctype html><html lang="en"><head><title>Everyday English · Preparing print</title></head><body style="font:16px Arial;padding:30px">Preparing ' + cards.length + ' complete cards…</body></html>'); popup.document.close();
    try {
      const results = await Promise.all(cards.map(async card => ({ card, result: await poster(card, ink) })));
      if (popup.closed) return;
      const ordinary = results.filter(r => typeOf(r.card) !== 'essay'), essays = results.filter(r => typeOf(r.card) === 'essay'), pages = [];
      const img = row => '<img src="' + row.result.url + '" alt="' + escape(row.card.title) + '">';
      for (let i = 0; i < ordinary.length; i += 2) pages.push('<section class="sheet ' + (cards.length > 1 ? 'pair' : 'single') + '">' + ordinary.slice(i, i + 2).map(img).join('') + '</section>');
      for (const row of essays) pages.push('<section class="sheet essay">' + img(row) + '</section>');
      popup.document.open();
      popup.document.write(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Everyday English · Print</title><style>@page{size:Letter portrait;margin:.35in}@page essay{size:Letter landscape;margin:.35in}*{box-sizing:border-box}body{margin:0;background:#eee;color:#292929;font:15px/1.5 Arial,sans-serif}.toolbar{position:sticky;top:0;background:#f6f2e9;padding:16px 24px;border-bottom:1px solid #bbb}.toolbar button{padding:10px 16px;margin-right:10px;border:1px solid #777;background:white;cursor:pointer}.toolbar p{margin:8px 0 0}main{padding:20px}.sheet{background:#fff;margin:0 auto 24px;padding:12px;max-width:800px;display:flex;gap:12px;align-items:center;justify-content:center}.sheet img{width:calc(50% - 6px);height:auto}.single img{width:60%}.essay{max-width:1150px}.essay img{width:100%}@media print{body,main{margin:0;padding:0;background:white}.toolbar{display:none}.sheet{margin:0;padding:0;max-width:none;height:10.28in;gap:.18in;break-inside:avoid;break-after:page}.sheet:last-child{break-after:auto}.pair img{width:3.81in;height:auto;max-height:10.28in;object-fit:contain}.single img{height:10.28in;width:auto;max-width:100%;object-fit:contain}.essay{page:essay;height:7.78in}.essay img{width:10.28in;height:auto;max-height:7.78in;object-fit:contain}}</style></head><body><div class="toolbar"><button id="print-now" disabled>Print / Save as PDF</button><button id="close-print">Close</button><p id="print-ready">Loading ${cards.length} ${ink ? 'ink-saving' : 'color'} cards…</p><p>Letter paper · ${cards.length > 1 ? 'Two portrait cards per page. Essay on its own landscape page.' : 'One complete card.'} ${ink ? 'White card interiors and thin category borders.' : 'Original pastel card colors.'} Disable browser headers and footers.</p></div><main>${pages.join('')}</main></body></html>`);
      popup.document.close();
      popup.document.getElementById('close-print').onclick = () => popup.close();
      const printButton = popup.document.getElementById('print-now'); printButton.onclick = () => { popup.focus(); popup.print(); };
      await Promise.all(Array.from(popup.document.images).map(image => image.decode()));
      if (popup.closed) return;
      printButton.disabled = false; popup.document.getElementById('print-ready').textContent = 'Ready: ' + cards.length + ' complete ' + (ink ? 'ink-saving' : 'color') + ' cards.';
      announce('The ' + (ink ? 'ink-saving' : 'color') + ' print layout is ready in the new window.'); popup.focus(); popup.print();
    } catch (_) { if (!popup.closed) popup.document.body.textContent = 'The complete print set could not load. Close this window and try again.'; announce('The print set could not load. Please try again.'); }
  }
  function stopSpeech() {
    speechGeneration++; speechId = ''; currentUtterance = null;
    window.JRVoicePlayer?.stop();
    document.querySelectorAll('#jr-english [data-jr-do^="speak-"]').forEach(button => { button.setAttribute('aria-pressed', 'false'); if (button.dataset.jrLabel) button.textContent = button.dataset.jrLabel; });
  }
  function prepareQuoteAudio(){
    for(const card of unit()?.cards||[]){
      if(!card.quoteBackground||!card.quoteAudio)continue;
      for(const file of [card.quoteAudio.title,card.quoteAudio.reading])window.JRVoicePlayer?.prepareFile(file).catch(()=>{});
    }
  }
  function playPreparedQuote(card,action,button){
    const audio=card.quoteAudio,player=window.JRVoicePlayer,pair=window.JR_ENGLISH_SPEAKERS?.[levelOf(card)];
    if(!card.quoteBackground||!audio)return false;
    if(!player||audio.voice!==pair?.teacher.voice){announce('This reading could not load. Please refresh and try again.');return true;}
    const key=card.id+':'+action;if(speechId===key){stopSpeech();announce('Audio stopped.');return true;}
    stopSpeech();speechId=key;const generation=speechGeneration;
    button.dataset.jrLabel=button.textContent;button.textContent='□ Stop audio';button.setAttribute('aria-pressed','true');
    announce('Preparing '+pair.teacher.name+'.');
    player.playFile(action==='speak-title'?audio.title:audio.reading,{
      onSpeaker:()=>{if(generation===speechGeneration)announce('Playing: '+pair.teacher.name+'. Select the same button to stop.');},
      onFinished:()=>{if(generation===speechGeneration){stopSpeech();announce('Audio finished.');}},
      onError:()=>{if(generation===speechGeneration){stopSpeech();announce('This reading could not load. Check your connection and try again.');}}
    },[{name:pair.teacher.name,start:0}]);return true;
  }
  async function speak(card, action, button) {
    if(playPreparedQuote(card,action,button))return;
    const pairs=window.JR_ENGLISH_SPEAKERS, player=window.JRVoicePlayer, pair=pairs?.[levelOf(card)];
    if(!pair||!player){announce('The selected voices are unavailable. Please refresh and try again.');return;}
    const key=card.id+':'+action;
    if(speechId===key){stopSpeech();announce('Audio stopped.');return;}
    stopSpeech();speechId=key;const generation=speechGeneration,segments=[];
    function add(copy,speaker=pair.teacher){
      if(dateOf(card)===SAMPLE_DATE)speaker={...speaker,pace:LEVEL_PACES[levelOf(card)]};
      const words=text(copy).split(/\s+/).filter(Boolean);let chunk='';
      for(const word of words){if(chunk.length+word.length>220){segments.push({...speaker,text:chunk});chunk='';}chunk+=(chunk?' ':'')+word;}
      if(chunk)segments.push({...speaker,text:chunk});
    }
    function conversation(copy){
      text(copy).replace(/\\n/g,'\n').split('\n').filter(Boolean).forEach(line=>{
        const colon=line.indexOf(':'),name=colon>=0?line.slice(0,colon).trim():'';
        const speaker=name===pair.partner.name||name==='B'?pair.partner:pair.teacher;
        add(colon>=0&&[pair.teacher.name,pair.partner.name,'A','B'].includes(name)?line.slice(colon+1).trim():line,speaker);
      });
    }
    if(action==='speak-title')add(card.title);
    else if(action==='speak-conversation')conversation(card.conversation);
    else if(typeOf(card)==='essay'){
      [card.title,...(card.paragraphs||[]).map(text),card.structure,exerciseText(card)].filter(Boolean).forEach(copy=>add(copy));
    }else{
      add(card.title);
      if(card.quoteBackground)add(card.attribution);
      sections(card).forEach(([label,copy])=>{add(label+'.');if(label==='Conversation')conversation(copy);else add(copy);});
    }
    if(!segments.length){stopSpeech();return;}
    button.dataset.jrLabel=button.textContent;button.textContent='□ Stop audio';button.setAttribute('aria-pressed','true');
    announce('Preparing '+pair.teacher.name+' and '+pair.partner.name+'.');
    let lastSpeaker='';
    const callbacks={
      onLoading:()=>{if(generation===speechGeneration)announce('Preparing your voices. First use downloads voice data to this device.');},
      onSpeaker:name=>{if(generation===speechGeneration&&name!==lastSpeaker){lastSpeaker=name;announce('Playing: '+name+'. Select the same button to stop.');}},
      onFinished:()=>{if(generation===speechGeneration){stopSpeech();announce('Audio finished.');}},
      onError:()=>{if(generation===speechGeneration){stopSpeech();announce('The selected voices could not load. Check your connection and try again.');}}
    };
    if(dateOf(card)===SAMPLE_DATE&&(action==='speak-title'||action==='speak-conversation'||(action==='speak-all'&&card.quoteBackground))){
      await samplePreparations.get(levelOf(card));
      if(generation!==speechGeneration)return;
    }
    const recording=sampleAudioByLevel.get(levelOf(card))?.cards[card.id],file=action==='speak-title'?recording?.title:action==='speak-conversation'?recording?.conversation:action==='speak-all'&&card.quoteBackground?recording?.reading:null;
    if(file)player.playFile(file,callbacks,action==='speak-conversation'?recording.turns:[{name:pair.teacher.name,start:0}]);
    else if(dateOf(card)===SAMPLE_DATE&&(action==='speak-title'||action==='speak-conversation'||(action==='speak-all'&&card.quoteBackground)))callbacks.onError();
    else player.play(segments,callbacks);
  }
  function toggleDone(card, button) {
    if (completed[card.id]) delete completed[card.id]; else completed[card.id] = true;
    saveProgress(); const done = !!completed[card.id]; button.textContent = done ? '✓ Completed' : '○ Mark as complete'; button.setAttribute('aria-pressed', String(done)); button.classList.toggle('is-done', done); button.closest('.jr-en-card')?.classList.toggle('is-complete', done);
    const label = document.getElementById('jr-en-progress-label'), progress = document.getElementById('jr-en-progress'); if (label) label.textContent = count() + ' / 11 completed'; if (progress) progress.value = count();
    announce(count() === 11 ? 'All eleven cards complete. A little progress, well made.' : (done ? 'Card marked complete. ' : 'Completion removed. ') + (storageAvailable ? 'Progress saved in this browser.' : 'Progress is available for this visit only.'));
  }
  document.addEventListener('click', async event => {
    const button = event.target.closest('#jr-english button[data-jr-do]'); if (!button) return;
    const action = button.dataset.jrDo;
    if(action==='retry'){editionLoading=null;window.jrEnglishInit();return;}
    if (action === 'level') { if (LEVELS.some(l => l[0] === button.dataset.jrLevel)) { level = button.dataset.jrLevel; persistSelection(); renderLocal('[data-jr-level="' + level + '"]'); announce('Showing all eleven ' + level + ' cards for ' + date + '.'); } return; }
    if (action === 'filter') { if (button.dataset.jrFilter === 'all' || TYPES[button.dataset.jrFilter]) { filter = button.dataset.jrFilter; persistSelection(); renderLocal('[data-jr-filter="' + filter + '"]'); } return; }
    const card = cardById(button.dataset.jrId);
    if (action.startsWith('speak-')) { if (card) speak(card, action, button); return; }
    if (action === 'done') { if (card) toggleDone(card, button); return; }
    if (action.startsWith('print')) { const all = action.startsWith('print-all'); await printCards(all ? unit().cards.slice() : card ? [card] : [], action.endsWith('ink')); return; }
    const originalLabel = button.textContent; button.disabled = true;
    try {
      if (action === 'zip') { button.textContent = 'Preparing eleven PNG cards…'; const archive = await zipCards(unit().cards.slice(), date, level); download(archive); announce('Your ZIP is ready: eleven complete PNG cards. Open the ZIP to extract the images.'); }
      else if (card && action === 'preview') await preview(card);
      else if (card && ['save', 'share'].includes(action)) {
        button.textContent = 'Preparing PNG…'; const result = await poster(card, false);
        if (action === 'share' && navigator.share && navigator.canShare?.({ files: [result.file] })) { await navigator.share({ files: [result.file], title: card.title, text: 'A little English, every day' }); announce('Sharing completed.'); }
        else { download(result.file); announce(action === 'share' ? 'Image sharing is unavailable here. Your complete PNG has been downloaded; attach it in your preferred app.' : 'Complete PNG downloaded.'); }
      }
    } catch (error) { if (error.name === 'AbortError') announce('Sharing cancelled.'); else announce('The complete card could not be prepared. Please refresh and try again.'); }
    finally { button.disabled = false; if (action !== 'preview') button.textContent = originalLabel; }
  });
  document.addEventListener('change', event => { if(event.target.matches('#jr-english [data-jr-date]')&&!DATES.includes(event.target.value)){event.target.setCustomValidity('Choose a date from January 1 to December 31, 2026.');event.target.reportValidity();return;} if (event.target.matches('#jr-english [data-jr-date]') && DATES.includes(event.target.value)) { event.target.setCustomValidity(''); date = event.target.value; persistSelection(); renderLocal('#jr-en-date'); announce('Showing ' + date + ' · ' + level + '.'); } });
  window.addEventListener('hashchange', () => { if (location.hash !== '#english') stopSpeech(); });
  window.jrEnglishDiagnostics = diagnostics;
})();
