// File: main.js
// HOW TO EDIT:
// - TODO: Replace NAME, EMAIL, and social URLs in index.html
// - To add projects: edit /project.json. The inline #projects-data script is a fallback for local file usage.
// Notes: app.js enhances the static HTML (progressive enhancement). Works with file:// because of inline fallback.

const $ = sel => document.querySelector(sel);
const $$ = sel => Array.from(document.querySelectorAll(sel));

/* Cached DOM nodes */
const themeToggle = $('#theme-toggle');
const yearEl = $('#year');
const projectsGrid = $('#projects-grid');
const projectsDataScript = $('#projects-data');
const searchInput = $('#search-input');
const tagFilters = $('#tag-filters');
const sortSelect = $('#sort-select');
const modal = $('#project-modal');
const modalClose = $('#modal-close');
const modalContent = $('#modal-content');
const viewButtons = () => $$('.view-btn');
const header = $('#header');

/* State */
let projects = []; // loaded dataset
let selectedTags = new Set();
let currentFilterText = '';
let currentSort = 'featured';
let lastFocusedEl = null;

/* Theme */
function setTheme(t){
  document.documentElement.setAttribute('data-theme', t);
  try{ localStorage.setItem('theme', t); }catch(e){}
}
function toggleTheme(){
  const t = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  setTheme(t);
}
themeToggle?.addEventListener('click', toggleTheme);

/* Header shrink on scroll */
let lastScroll = 0;
window.addEventListener('scroll', () => {
  const s = window.scrollY;
  if (s > 40) header.classList.add('shrink'); else header.classList.remove('shrink');
  lastScroll = s;
});

/* IntersectionObserver for reveals and skill bars */
const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if(entry.isIntersecting){
      entry.target.classList.add('inview');
      // animate skill bars
      entry.target.querySelectorAll?.('.bar-fill')?.forEach(el => {
        const level = el.getAttribute('data-level') || 0;
        el.style.width = level + '%';
      });
    }
  });
},{threshold:0.12});

document.querySelectorAll('.reveal').forEach(el => observer.observe(el));

/* Try to load external projects.json, else fallback to inline script */
async function loadProjects(){
  try{
    const res = await fetch('./project.json', {cache: "no-store"});
    if(!res.ok) throw new Error('fetch failed');
    projects = await res.json();
  }catch(e){
    // fallback to inline
    try{
      const txt = projectsDataScript?.textContent?.trim();
      projects = txt ? JSON.parse(txt) : [];
    }catch(err){
      projects = [];
    }
  }
  // after load, render tags & projects
  renderTagFilters();
  renderProjects();
  attachViewHandlers();
}

/* Utility: create tag list from dataset */
function getAllTags(){
  const set = new Set();
  projects.forEach(p => (p.tags || []).forEach(t => set.add(t)));
  return Array.from(set).sort();
}

/* Render tag filter buttons */
function renderTagFilters(){
  const tags = getAllTags();
  tagFilters.innerHTML = '';
  tags.forEach(tag => {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'tag-btn';
    btn.textContent = tag;
    btn.dataset.tag = tag;
    btn.addEventListener('click', () => {
      if(selectedTags.has(tag)) selectedTags.delete(tag); else selectedTags.add(tag);
      btn.classList.toggle('active');
      filterAndRender();
    });
    tagFilters.appendChild(btn);
  });
}

/* Render projects (grid) */
function renderProjects(){
  // If JS disabled, static project cards exist. We prefer to replace only when dataset loaded.
  // Generate DOM
  projectsGrid.innerHTML = '';
  const list = sortProjects(projects.slice());
  list.forEach(p => {
    const article = document.createElement('article');
    article.className = 'project-card reveal';
    article.setAttribute('role','listitem');
    article.dataset.id = p.id;

    const media = document.createElement('div'); media.className='card-media';
    const img = document.createElement('img');
    img.alt = p.title + ' screenshot';
    img.loading = 'lazy';
    img.decoding = 'async';
    // srcset example for image performance
    const imgUrl = p.images[0] || '';
    img.src = imgUrl + '&w=800';
    img.srcset = `${imgUrl}&w=480 480w, ${imgUrl}&w=800 800w, ${imgUrl}&w=1200 1200w`;
    img.sizes = "(max-width:700px) 100vw, 50vw";
    img.width = 800;
    img.height = 450;
    img.className = 'project-img img-skeleton';
    // remove skeleton on load
    img.addEventListener('load', () => img.classList.remove('img-skeleton'));
    media.appendChild(img);

    const body = document.createElement('div'); body.className='card-body';
    const title = document.createElement('h3'); title.className='card-title'; title.innerHTML = highlight(p.title);
    const desc = document.createElement('p'); desc.className='card-desc'; desc.innerHTML = highlight(p.shortDescription);
    const meta = document.createElement('div'); meta.className='card-meta';
    const tagsWrap = document.createElement('div'); tagsWrap.className='tags';
    (p.tags || []).slice(0,4).forEach(t => {
      const sp = document.createElement('span'); sp.textContent = `#${t}`; tagsWrap.appendChild(sp);
    });
    const actions = document.createElement('div'); actions.className='card-actions';
    const viewBtn = document.createElement('button'); viewBtn.className='btn small view-btn'; viewBtn.textContent='View'; viewBtn.dataset.id = p.id;
    const codeLink = document.createElement('a'); codeLink.className='link'; codeLink.textContent='Code'; codeLink.href = p.githubUrl || '#';
    codeLink.target = '_blank'; codeLink.rel='noopener';
    actions.appendChild(viewBtn); actions.appendChild(codeLink);

    meta.appendChild(tagsWrap); meta.appendChild(actions);
    body.appendChild(title); body.appendChild(desc); body.appendChild(meta);
    article.appendChild(media); article.appendChild(body);
    projectsGrid.appendChild(article);
    observer.observe(article);
  });
}

/* Sorting */
function sortProjects(list){
  if(currentSort === 'newest') return list.sort((a,b)=> (b.year||0)-(a.year||0));
  if(currentSort === 'year-desc') return list.sort((a,b)=> (b.year||0)-(a.year||0));
  // featured first
  return list.sort((a,b)=> (b.featured?1:0)-(a.featured?1:0));
}

/* Search & filter logic */
function filterAndRender(){
  currentFilterText = (searchInput?.value || '').trim().toLowerCase();
  currentSort = sortSelect.value;
  const filtered = projects.filter(p => {
    // tag filter
    if(selectedTags.size){
      const matchTag = (p.tags || []).some(t => selectedTags.has(t));
      if(!matchTag) return false;
    }
    // text filter
    if(currentFilterText){
      const hay = [p.title, p.shortDescription, (p.longDescription||'')].join(' ').toLowerCase();
      return hay.includes(currentFilterText);
    }
    return true;
  });
  // Render filtered list
  projectsGrid.innerHTML = '';
  const list = sortProjects(filtered);
  list.forEach(p => {
    const article = document.createElement('article');
    article.className = 'project-card reveal';
    article.dataset.id = p.id;
    // create inner (simplified, similar to renderProjects)
    article.innerHTML = `
      <div class="card-media"><img alt="${p.title} screenshot" class="img-skeleton" loading="lazy" src="${p.images[0]}&w=800" srcset="${p.images[0]}&w=480 480w, ${p.images[0]}&w=800 800w, ${p.images[0]}&w=1200 1200w" sizes="(max-width:700px) 100vw, 50vw"></div>
      <div class="card-body">
        <h3 class="card-title">${highlight(p.title)}</h3>
        <p class="card-desc">${highlight(p.shortDescription)}</p>
        <div class="card-meta">
          <div class="tags">${(p.tags||[]).map(t=>`<span>#${t}</span>`).join('')}</div>
          <div class="card-actions"><button class="btn small view-btn" data-id="${p.id}">View</button><a class="link" href="${p.githubUrl}" target="_blank" rel="noopener">Code</a></div>
        </div>
      </div>`;
    projectsGrid.appendChild(article);
    observer.observe(article);
  });
  attachViewHandlers();
}

/* Highlight matched terms */
function escapeRegExp(s){ return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
function highlight(text){
  if(!currentFilterText) return text;
  const pattern = new RegExp(`(${escapeRegExp(currentFilterText)})`, 'ig');
  return text.replace(pattern, match => `<mark class="mark">${match}</mark>`);
}

/* Attach view buttons to open modal */
function attachViewHandlers(){
  $$('.view-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const id = btn.dataset.id;
      openModal(id);
    });
  });
}

/* Modal content generation */
function openModal(id){
  const p = projects.find(x => x.id === id);
  if(!p) return;
  lastFocusedEl = document.activeElement;
  modal.setAttribute('aria-hidden','false');
  modal.style.display = 'flex';
  modalClose.focus();
  // build content
  modalContent.innerHTML = `
    <article class="project-detail" aria-labelledby="proj-title-${p.id}">
      <h2 id="proj-title-${p.id}">${p.title} <span class="muted">(${p.year})</span></h2>
      <p class="muted">${p.shortDescription}</p>
      <div class="project-media">
        ${p.images.map(src=>`<img alt="${p.title}" loading="lazy" src="${src}&w=1200" style="max-width:100%;margin-top:0.5rem;border-radius:10px">`).join('')}
      </div>
      <h3>Problem</h3>
      <p>${p.longDescription}</p>
      <h3>Tech Stack</h3>
      <p>${(p.techStack || []).join(', ')}</p>
      <h3>Links</h3>
      <p><a href="${p.githubUrl}" target="_blank" rel="noopener">Repository</a> ${p.liveDemoUrl?`• <a href="${p.liveDemoUrl}" target="_blank" rel="noopener">Live Demo</a>`:''}</p>
    </article>
  `;
  // trap focus minimally
  modal.addEventListener('keydown', onModalKeydown);
}

/* Close modal */
function closeModal(){
  modal.setAttribute('aria-hidden','true');
  modal.style.display = 'none';
  modalContent.innerHTML = '';
  modal.removeEventListener('keydown', onModalKeydown);
  try{ lastFocusedEl?.focus(); }catch(e){}
}
modalClose?.addEventListener('click', closeModal);
modal.querySelector('.modal-backdrop')?.addEventListener('click', closeModal);
function onModalKeydown(e){
  if(e.key === 'Escape') closeModal();
}

/* Attach other event listeners */
searchInput?.addEventListener('input', () => filterAndRender());
sortSelect?.addEventListener('change', () => { currentSort = sortSelect.value; filterAndRender(); });

/* Contact form basic client-side validation & Netlify fallback */
const contactForm = $('#contact-form');
if(contactForm){
  contactForm.addEventListener('submit', (e) => {
    // Let Netlify handle POST when hosted. For local fallback, show mailto fallback.
    const formStatus = $('#form-status');
    if(location.protocol === 'file:'){
      e.preventDefault();
      formStatus.textContent = 'Local file detected — please use the mail link or deploy to enable server form capture.';
      return;
    }
    // otherwise allow submission (Netlify or Formspree)
    formStatus.textContent = 'Sending...';
    setTimeout(()=> formStatus.textContent = 'Sent — thanks! (This is a demo message response.)', 1000);
  });
}

/* Attach keyboard support for tag buttons */
tagFilters.addEventListener('keyup', (e) => {
  if(e.key === 'Enter' || e.key === ' ') e.target.click();
});

/* Initial load */
document.addEventListener('DOMContentLoaded', async () => {
  yearEl.textContent = new Date().getFullYear();
  await loadProjects();
  // attach view handlers for static fallback cards
  $$('.view-btn').forEach(b => b.addEventListener('click', e => openModal(e.target.dataset.id)));
  // site accessibility: focus outlines for keyboard only
  document.body.addEventListener('keydown', e => {
    if(e.key === 'Tab') document.documentElement.classList.add('show-focus');
  }, {once:true});
});
