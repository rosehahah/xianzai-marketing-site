const isEnglish = document.documentElement.lang.toLowerCase().startsWith('en');

const messages = isEnglish ? {
  menuOpen: 'Open navigation menu',
  menuClose: 'Close navigation menu',
  categories: {
    daily: 'Playful days',
    mood: 'People & moods',
    profile: 'Character cards',
    story: 'Cinematic stories',
  },
  cardLabel: (name) => `View the ${name} frame in XianNow`,
  cardAlt: (name, description) => `${name} frame example. ${description}`,
  countAll: (visible, total) => `Showing ${visible} of ${total} frames`,
  countCategory: (category, count) => `${category} · ${count} frames`,
  collapse: 'Show fewer frames <span aria-hidden="true">−</span>',
  expand: (count) => `Show all ${count} frames <span aria-hidden="true">＋</span>`,
  galleryError: 'The frame library could not be loaded. Please try again later.',
  galleryUnavailable: 'Frame library temporarily unavailable',
} : {
  menuOpen: '打开导航菜单',
  menuClose: '关闭导航菜单',
  categories: {
    daily: '奇趣日常',
    mood: '心情关系',
    profile: '角色档案',
    story: '电影叙事',
  },
  cardLabel: (name) => `在苋在中查看${name}片方`,
  cardAlt: (name, description) => `${name}片方视觉示例，${description}`,
  countAll: (visible, total) => `展示 ${visible} / ${total} 款`,
  countCategory: (category, count) => `${category} · ${count} 款`,
  collapse: '收起片方 <span aria-hidden="true">−</span>',
  expand: (count) => `展开全部 ${count} 款片方 <span aria-hidden="true">＋</span>`,
  galleryError: '片方图鉴暂时无法载入，请稍后重试。',
  galleryUnavailable: '片方图鉴暂时不可用',
};

document.querySelectorAll('.language-link').forEach((link) => {
  link.addEventListener('click', () => {
    try {
      window.localStorage.setItem('xiannow-language', link.hreflang.startsWith('zh') ? 'zh' : 'en');
    } catch (_) {
      // Language selection still works when storage is unavailable.
    }
  });
});

const menuButton = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav');
if (menuButton && mainNav) {
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    menuButton.setAttribute('aria-label', open ? messages.menuClose : messages.menuOpen);
    mainNav.classList.toggle('is-open', open);
  });
  mainNav.addEventListener('click', (event) => {
    if (event.target.closest('a')) {
      mainNav.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', messages.menuOpen);
    }
  });
}

// Browser-native lazy loading can fetch megabytes several screens ahead of the
// viewport. Keep those image URLs inert until they are close to being visible.
const loadDeferredImage = (image) => {
  if (!image.dataset.src) return;
  image.src = image.dataset.src;
  delete image.dataset.src;
};
const lazyImageObserver = typeof IntersectionObserver === 'function'
  ? new IntersectionObserver((entries, observer) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      observer.unobserve(entry.target);
      if (entry.target.isConnected) loadDeferredImage(entry.target);
    });
  }, { rootMargin: '250px 0px', threshold: 0 })
  : null;
const observeDeferredImages = (root = document) => {
  root.querySelectorAll('img[data-src]').forEach((image) => {
    if (lazyImageObserver) lazyImageObserver.observe(image);
    else loadDeferredImage(image);
  });
};
observeDeferredImages();

const grid = document.querySelector('#frame-grid');
if (grid) {
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const moreButton = document.querySelector('#show-all');
  const countLabel = document.querySelector('#gallery-count');
  const chineseCategoryKeys = { '日常': 'daily', '心情': 'mood', '档案': 'profile', '故事': 'story' };
  let allFrames = [];
  let currentFilter = 'all';
  let showAll = false;
  const initialCount = 8;

  const categoryKey = (item) => isEnglish ? item.category : chineseCategoryKeys[item.category];

  const drawCards = () => {
    const filtered = currentFilter === 'all' ? allFrames : allFrames.filter((item) => categoryKey(item) === currentFilter);
    const visible = showAll || currentFilter !== 'all' ? filtered : filtered.slice(0, initialCount);
    grid.querySelectorAll('img[data-src]').forEach((image) => lazyImageObserver?.unobserve(image));
    grid.innerHTML = visible.map((item, index) => {
      const category = messages.categories[categoryKey(item)];
      return `
      <article class="frame-card" data-category="${categoryKey(item)}" style="animation-delay:${Math.min(index * 35, 280)}ms">
        <a href="https://apps.apple.com/cn/app/%E8%8B%8B%E5%9C%A8/id6814311061" target="_blank" rel="noreferrer" aria-label="${messages.cardLabel(item.name)}">
          <div class="frame-card-image"><img data-src="${item.image}" alt="${messages.cardAlt(item.name, item.description)}" loading="lazy" decoding="async"><span class="card-category">${category}</span></div>
          <div class="frame-meta"><div><h3>${item.name}</h3><p>${item.description}</p></div><span class="card-arrow" aria-hidden="true">↗</span></div>
        </a>
      </article>`;
    }).join('');
    observeDeferredImages(grid);
    const selectedCategory = messages.categories[currentFilter];
    countLabel.textContent = currentFilter === 'all'
      ? messages.countAll(visible.length, allFrames.length)
      : messages.countCategory(selectedCategory, filtered.length);
    moreButton.hidden = currentFilter !== 'all' || filtered.length <= initialCount;
    moreButton.setAttribute('aria-expanded', String(showAll));
    moreButton.innerHTML = showAll ? messages.collapse : messages.expand(allFrames.length);
    grid.setAttribute('aria-busy', 'false');
  };

  fetch(isEnglish ? '/assets/templates.en.json' : '/assets/templates.json')
    .then((response) => { if (!response.ok) throw new Error('gallery'); return response.json(); })
    .then((items) => { allFrames = items; drawCards(); })
    .catch(() => {
      grid.setAttribute('aria-busy', 'false');
      grid.innerHTML = `<p class="gallery-error">${messages.galleryError}</p>`;
      countLabel.textContent = messages.galleryUnavailable;
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

// Attach only this page's web film, when visible or explicitly requested.
const heroVideo = document.querySelector('#hero-video');
if (heroVideo) {
  const stage = heroVideo.closest('.hero-film-stage');
  const source = heroVideo.querySelector('source');
  const controls = stage.querySelector('.hero-video-controls');
  const playButton = stage.querySelector('[data-video-play]');
  const startButton = stage.querySelector('[data-video-start]');
  const soundButton = stage.querySelector('[data-video-sound]');
  const expandButton = stage.querySelector('[data-video-expand]');
  const dialog = document.querySelector('.hero-video-dialog');
  const expandedVideo = dialog.querySelector('video');
  const expandedStage = expandedVideo.parentElement;
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const portraitPreference = window.matchMedia('(max-aspect-ratio: 4/5)');
  const selectedSource = (highQuality = false) => portraitPreference.matches
    ? highQuality ? source.dataset.hdPortraitSrc : source.dataset.portraitSrc
    : highQuality ? source.dataset.hdSrc : source.dataset.src;
  const labels = isEnglish
    ? { play: 'Play', pause: 'Pause', soundOn: 'Sound on', soundOff: 'Sound off', error: 'Video unavailable. Please try again later.' }
    : { play: '播放', pause: '暂停', soundOn: '开启声音', soundOff: '关闭声音', error: '视频暂时无法播放，请稍后重试。' };
  let inView = false;
  let manuallyPaused = false;
  let explicitlyStarted = false;
  let playbackFailed = false;
  let autoplayBlocked = false;
  let dialogWasPlaying = false;
  let expandedWasPlayingBeforeHide = false;
  let playAttempt = 0;
  let expandedLoad = 0;
  let pendingExpandedSeek;
  const automaticPlaybackAllowed = () => !motionPreference.matches && !connection?.saveData;
  const wantsPlayback = () => inView && !document.hidden && !dialog.open && !manuallyPaused
    && !playbackFailed && (explicitlyStarted || automaticPlaybackAllowed());

  // A play promise is not evidence of a painted frame. Keep the cover until the
  // browser presents a frame; older browsers use decoded data and two paint ticks.
  const frameCover = (video, container) => {
    let generation = 0;
    let frameRequest = null;
    let fallbackQueued = false;
    const reveal = (token) => {
      if (token === generation && video.readyState >= 2 && video.videoWidth > 0) {
        container.classList.add('has-frame');
      }
    };
    const watch = () => {
      if (container.classList.contains('has-frame')) return;
      const token = generation;
      if (video.requestVideoFrameCallback) {
        if (frameRequest === null) {
          frameRequest = video.requestVideoFrameCallback(() => {
            if (token !== generation) return;
            frameRequest = null;
            reveal(token);
            // Metadata seeking can temporarily invalidate the presented frame.
            if (!container.classList.contains('has-frame')) watch();
          });
        }
      } else if (video.readyState >= 2 && !fallbackQueued) {
        fallbackQueued = true;
        requestAnimationFrame(() => requestAnimationFrame(() => {
          if (token === generation) fallbackQueued = false;
          reveal(token);
        }));
      }
    };
    video.addEventListener('loadeddata', watch);
    video.addEventListener('playing', watch);
    video.addEventListener('seeked', watch);
    return {
      watch,
      reset: () => {
        generation += 1;
        if (frameRequest !== null) video.cancelVideoFrameCallback?.(frameRequest);
        frameRequest = null;
        fallbackQueued = false;
        container.classList.remove('has-frame');
      },
    };
  };
  const heroCover = frameCover(heroVideo, stage);
  const expandedCover = frameCover(expandedVideo, expandedStage);
  const attachSource = () => {
    if (!source.hasAttribute('src')) {
      source.src = selectedSource();
      heroVideo.load();
      heroCover.watch();
    }
  };
  const unloadHeroSource = () => {
    playAttempt += 1;
    heroCover.reset();
    heroVideo.pause();
    if (source.hasAttribute('src')) {
      source.removeAttribute('src');
      heroVideo.load();
    }
  };
  const updateControls = () => {
    const playing = !heroVideo.paused && !heroVideo.ended;
    playButton.textContent = playing ? labels.pause : labels.play;
    startButton.hidden = playing || !(autoplayBlocked || playbackFailed || (!explicitlyStarted && !automaticPlaybackAllowed()));
    soundButton.textContent = heroVideo.muted ? labels.soundOn : labels.soundOff;
    soundButton.setAttribute('aria-pressed', String(!heroVideo.muted));
    stage.classList.toggle('is-playing', playing);
  };
  const reconcilePlayback = async () => {
    const attempt = ++playAttempt;
    if (!wantsPlayback()) {
      heroVideo.pause();
      updateControls();
      return;
    }
    attachSource();
    try {
      await heroVideo.play();
      if (!wantsPlayback()) heroVideo.pause();
    } catch (error) {
      // Muted playback can also be blocked. Leave a real-click entry available.
      if (attempt === playAttempt && wantsPlayback() && error.name !== 'AbortError') {
        autoplayBlocked = error.name === 'NotAllowedError';
        playbackFailed = true;
      }
      updateControls();
    }
  };
  const startPlayback = () => {
    manuallyPaused = false;
    explicitlyStarted = true;
    playbackFailed = false;
    autoplayBlocked = false;
    playButton.removeAttribute('title');
    if (heroVideo.error) {
      heroCover.reset();
      heroVideo.load();
    }
    reconcilePlayback();
  };

  heroVideo.muted = true;
  heroVideo.defaultMuted = true;
  heroVideo.volume = 1;
  heroVideo.controls = false;
  controls.hidden = false;
  heroVideo.addEventListener('playing', () => {
    if (!wantsPlayback()) { heroVideo.pause(); return; }
    autoplayBlocked = false;
    updateControls();
  });
  heroVideo.addEventListener('pause', updateControls);
  heroVideo.addEventListener('volumechange', updateControls);
  heroVideo.addEventListener('error', () => {
    playbackFailed = true;
    playButton.title = labels.error;
    updateControls();
  });
  playButton.addEventListener('click', () => {
    if (!heroVideo.paused) {
      manuallyPaused = true;
      reconcilePlayback();
    } else {
      startPlayback();
    }
  });
  startButton.addEventListener('click', startPlayback);
  soundButton.addEventListener('click', () => {
    heroVideo.muted = !heroVideo.muted;
    if (heroVideo.paused) startPlayback();
    updateControls();
  });

  if (typeof IntersectionObserver === 'function') {
    const observer = new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      reconcilePlayback();
    }, { threshold: 0.2 });
    observer.observe(stage);
  } else {
    inView = true;
    reconcilePlayback();
  }

  const loadExpandedSource = (startTime) => {
    const load = ++expandedLoad;
    const nextSource = selectedSource(true);
    if (pendingExpandedSeek) expandedVideo.removeEventListener('loadedmetadata', pendingExpandedSeek);
    if (expandedVideo.getAttribute('src') !== nextSource) {
      expandedCover.reset();
      expandedVideo.width = portraitPreference.matches ? 1620 : 3840;
      expandedVideo.height = portraitPreference.matches ? 2880 : 1646;
      expandedVideo.src = nextSource;
      expandedVideo.load();
    }
    pendingExpandedSeek = () => {
      if (load !== expandedLoad || !dialog.open) return;
      if (Number.isFinite(startTime)) {
        const end = Number.isFinite(expandedVideo.duration) ? Math.max(0, expandedVideo.duration - 0.05) : startTime;
        expandedVideo.currentTime = Math.min(startTime, end);
      }
      pendingExpandedSeek = undefined;
    };
    if (expandedVideo.readyState >= 1) pendingExpandedSeek();
    else expandedVideo.addEventListener('loadedmetadata', pendingExpandedSeek, { once: true });
    expandedCover.watch();
    expandedVideo.play().catch(() => {}); // Native controls remain usable when policy blocks playback.
  };
  portraitPreference.addEventListener('change', () => {
    unloadHeroSource();
    playbackFailed = false;
    autoplayBlocked = false;
    if (dialog.open) loadExpandedSource(expandedVideo.currentTime);
    reconcilePlayback();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      expandedWasPlayingBeforeHide = dialog.open && !expandedVideo.paused;
      expandedVideo.pause();
    } else if (dialog.open && expandedWasPlayingBeforeHide) {
      expandedWasPlayingBeforeHide = false;
      expandedVideo.play().catch(() => {});
    }
    reconcilePlayback();
  });
  const preferenceChanged = () => {
    explicitlyStarted = false;
    playbackFailed = false;
    autoplayBlocked = false;
    if (!automaticPlaybackAllowed()) unloadHeroSource();
    reconcilePlayback();
  };
  motionPreference.addEventListener('change', preferenceChanged);
  let previousSaveData = Boolean(connection?.saveData);
  connection?.addEventListener('change', () => {
    const saveData = Boolean(connection.saveData);
    if (saveData === previousSaveData) return;
    previousSaveData = saveData;
    preferenceChanged();
  });

  expandButton.addEventListener('click', () => {
    dialogWasPlaying = !heroVideo.paused;
    const startTime = heroVideo.currentTime;
    heroVideo.pause();
    // Reuse the selected responsive cover only after opening; do not preload HD.
    if (!expandedStage.querySelector('picture')) {
      expandedStage.appendChild(stage.querySelector('picture').cloneNode(true));
    }
    expandedVideo.muted = heroVideo.muted;
    expandedVideo.volume = heroVideo.volume;
    dialog.showModal();
    loadExpandedSource(startTime);
  });
  dialog.querySelector('[data-video-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target !== dialog) return;
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    expandedLoad += 1;
    expandedWasPlayingBeforeHide = false;
    if (pendingExpandedSeek) expandedVideo.removeEventListener('loadedmetadata', pendingExpandedSeek);
    pendingExpandedSeek = undefined;
    expandedVideo.pause();
    heroVideo.muted = expandedVideo.muted;
    heroVideo.volume = expandedVideo.volume;
    if (heroVideo.readyState >= 1) heroVideo.currentTime = expandedVideo.currentTime;
    updateControls();
    expandButton.focus({ preventScroll: true });
    if (dialogWasPlaying) reconcilePlayback();
  });
  updateControls();
}
