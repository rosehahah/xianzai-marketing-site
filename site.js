const menuButton = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');
if (menuButton && mainNav) {
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? '关闭导航菜单' : '打开导航菜单');
    mainNav.classList.toggle('is-open', open);
  });
  mainNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      mainNav.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', '打开导航菜单');
    }
  });
}

const grid = document.querySelector('#frame-grid');
if (grid) {
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const moreButton = document.querySelector('#show-all');
  const countLabel = document.querySelector('#gallery-count');
  let allFrames = [];
  let currentFilter = '全部';
  let showAll = false;
  const initialCount = 8;

  const drawCards = () => {
    const filtered = currentFilter === '全部' ? allFrames : allFrames.filter((item) => item.category === currentFilter);
    const visible = showAll || currentFilter !== '全部' ? filtered : filtered.slice(0, initialCount);
    grid.innerHTML = visible.map((item, index) => `
      <article class="frame-card" data-category="${item.category}" style="animation-delay:${Math.min(index * 35, 280)}ms">
        <a href="https://apps.apple.com/app/id6814311061" target="_blank" rel="noreferrer" aria-label="在苋在中查看${item.name}片方">
          <div class="frame-card-image"><img src="${item.image}" alt="${item.name}片方视觉示例，${item.description}" loading="lazy" decoding="async"><span class="card-category">${item.category}</span></div>
          <div class="frame-meta"><div><h3>${item.name}</h3><p>${item.description}</p></div><span class="card-arrow" aria-hidden="true">↗</span></div>
        </a>
      </article>`).join('');
    countLabel.textContent = currentFilter === '全部' ? `展示 ${visible.length} / ${allFrames.length} 款` : `${currentFilter} · ${filtered.length} 款`;
    moreButton.hidden = currentFilter !== '全部' || filtered.length <= initialCount;
    moreButton.setAttribute('aria-expanded', String(showAll));
    moreButton.innerHTML = showAll ? '收起片方 <span aria-hidden="true">−</span>' : `展开全部 ${allFrames.length} 款片方 <span aria-hidden="true">＋</span>`;
    grid.setAttribute('aria-busy', 'false');
  };

  fetch('/assets/templates.json')
    .then((response) => { if (!response.ok) throw new Error('gallery'); return response.json(); })
    .then((items) => { allFrames = items; drawCards(); })
    .catch(() => {
      grid.setAttribute('aria-busy', 'false');
      grid.innerHTML = '<p class="gallery-error">片方图鉴暂时无法载入，请稍后重试。</p>';
      countLabel.textContent = '片方图鉴暂时不可用';
    });

  filterButtons.forEach((button) => button.addEventListener('click', () => {
    currentFilter = button.dataset.filter;
    showAll = false;
    filterButtons.forEach((item) => {
      const active = item === button;
      item.classList.toggle('is-active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    if (allFrames.length) drawCards();
  }));
  moreButton.addEventListener('click', () => { showAll = !showAll; drawCards(); });
}

document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (event) => {
    const target = document.querySelector(link.getAttribute('href'));
    if (!target) return;
    event.preventDefault();
    target.scrollIntoView({ behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
  });
});
