document.addEventListener('DOMContentLoaded', () => {
  // 既存: ローディング
  const loadingScreen = document.getElementById('loading-screen');
  const heroSection = document.querySelector('.hero');
  if (loadingScreen && heroSection) {
    const isLoaded = sessionStorage.getItem('edgehub_loaded');
    if (!isLoaded) {
      heroSection.style.opacity = '0';
      setTimeout(() => {
        loadingScreen.classList.add('fade-out');
        setTimeout(() => {
          loadingScreen.style.display = 'none';
          heroSection.style.opacity = '1';
        }, 800);
      }, 3500);
      sessionStorage.setItem('edgehub_loaded', '1');
    } else {
      loadingScreen.style.display = 'none';
      heroSection.style.opacity = '1';
    }
  }

  // Hero scroll interaction
  const heroSticky = document.querySelector('.hero-sticky');
  const heroOverlay = document.querySelector('.hero-overlay');
  const heroLogo = document.querySelector('.hero-center-logo');
  const heroTexts = document.querySelector('.hero-texts');

  if (heroSection && heroSticky && heroOverlay && heroLogo && heroTexts) {
    const viewportH = () => window.innerHeight || document.documentElement.clientHeight;

    let ticking = false;
    const onScrollOrResize = () => {
      if (!ticking) {
        window.requestAnimationFrame(update);
        ticking = true;
      }
    };

    const update = () => {
      ticking = false;
      const vh = viewportH();
      const startY = heroSection.offsetTop; // セクション開始位置
      const total = vh * 2.2; // 進行距離（2.2画面）固定時間延長
      const y = window.scrollY || window.pageYOffset || 0;
      const delta = Math.max(0, Math.min(total, y - startY));
      const progressed = delta / total; // 0..1

      // 背景黒化 0 -> 0.85
      const alpha = progressed * 0.85;
      heroOverlay.style.backgroundColor = `rgba(0,0,0,${alpha.toFixed(3)})`;

      // ロゴ: 1 -> 0, scale 1 -> .8
      heroLogo.style.opacity = String(1 - progressed);
      const scale = 1 - progressed * 0.2;
      heroLogo.style.transform = `translate(-50%, -50%) scale(${scale.toFixed(3)})`;

      // テキスト: 0.4からフェードイン開始、1.0で完全表示
      const textStart = 0.4;
      let textOpacity = 0;
      if (progressed > textStart) {
        textOpacity = (progressed - textStart) / (1 - textStart);
      }
      heroTexts.style.opacity = String(Math.min(Math.max(textOpacity, 0), 1));
    };

    update();
    window.addEventListener('scroll', onScrollOrResize, { passive: true });
    window.addEventListener('resize', onScrollOrResize);
  }

  // SERVICE: intersection-based reveal
  const serviceItems = document.querySelectorAll('.service-item');
  if (serviceItems.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
          entry.target.classList.add('in-view');
          io.unobserve(entry.target); // 一度のみ
        }
      });
    }, { threshold: [0, 0.3, 1] });
    serviceItems.forEach(el => io.observe(el));
  }

  // SERVICE vertical cards background apply
  const vcards = document.querySelectorAll('.service-vcard');
  if (vcards.length) {
    vcards.forEach(card => {
      const bg = card.getAttribute('data-bg');
      if (bg) {
        card.style.backgroundImage = `url(${bg})`;
      }
    });

    const io2 = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && entry.intersectionRatio >= 0.3) {
          entry.target.classList.add('in-view');
          io2.unobserve(entry.target);
        }
      });
    }, { threshold: [0, 0.3, 1] });
    vcards.forEach(el => io2.observe(el));
  }

  // business2: curve headline animation (disabled; always visible)
});