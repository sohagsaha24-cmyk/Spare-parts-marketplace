// AutoParts BD - Main JavaScript

document.addEventListener('DOMContentLoaded', () => {
  // Auto-dismiss flash messages
  const flashes = document.querySelectorAll('.flash-container, .admin-flash-container');
  flashes.forEach(el => {
    setTimeout(() => {
      el.style.opacity = '0';
      el.style.transition = 'opacity 0.5s';
      setTimeout(() => el.remove(), 500);
    }, 3500);
  });

  // --- Single Page Marketplace (SPA) ---
  if (window.__AUTOPARTS_SPA__) {
    const state = {
      category: '',
      search: '',
      categories: [],
      products: [],
    };

    const el = {
      categories: document.getElementById('spa-categories'),
      searchInfo: document.getElementById('spa-search-info'),
      title: document.getElementById('spa-title'),
      count: document.getElementById('spa-count'),
      grid: document.getElementById('spa-products'),
      empty: document.getElementById('spa-empty'),
    };

    const qs = (obj) => {
      const u = new URLSearchParams();
      Object.entries(obj).forEach(([k, v]) => {
        if (v !== undefined && v !== null && String(v).trim() !== '') u.set(k, v);
      });
      return u.toString();
    };

    const fmtPrice = (p) => {
      const n = Number(p || 0);
      if (Number.isNaN(n)) return String(p ?? '');
      return n.toLocaleString(undefined, { maximumFractionDigits: 2 });
    };

    const setActiveCategoryBtn = () => {
      const btns = el.categories?.querySelectorAll('.cat-btn') || [];
      btns.forEach(b => b.classList.toggle('active', (b.dataset.category || '') === state.category));
    };

    const renderCategories = () => {
      if (!el.categories) return;
      el.categories.innerHTML = '';
      const addBtn = (label, category) => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'cat-btn';
        b.dataset.category = category;
        b.textContent = label;
        b.addEventListener('click', () => {
          state.category = category;
          setActiveCategoryBtn();
          loadProducts();
        });
        el.categories.appendChild(b);
      };
      addBtn('All Parts', '');
      state.categories.forEach(c => addBtn(c, c));
      setActiveCategoryBtn();
    };

    const productCard = (p) => {
      const img = p.image_url || 'https://via.placeholder.com/400x280?text=No+Image';
      const out = Number(p.stock) <= 0;
      const low = !out && Number(p.stock) <= 5;
      const stockText = out ? 'Unavailable' : low ? `${p.stock} left` : 'In Stock';
      const stockClass = out ? 'stock-out' : low ? 'stock-low' : 'stock-ok';
      const desc = (p.description || '').trim();
      const short = desc.length > 80 ? `${desc.slice(0, 80)}...` : desc;
      const detailHref = `/products/${p.id}`;
      const buyHref = `/orders/checkout/${p.id}`;

      const wrap = document.createElement('div');
      wrap.className = 'product-card';
      wrap.innerHTML = `
        <a href="${detailHref}" class="card-link">
          <div class="card-image">
            <img src="${img}" alt="${(p.name || '').replaceAll('"', '&quot;')}" loading="lazy"
                 onerror="this.src='https://via.placeholder.com/400x280?text=No+Image'">
            <div class="card-category-badge">${p.category || ''}</div>
            ${out ? `<div class="out-of-stock-badge">Out of Stock</div>` : low ? `<div class="low-stock-badge">Low Stock</div>` : ``}
          </div>
          <div class="card-body">
            <div class="card-brand">${p.brand || ''}</div>
            <h3 class="card-title">${p.name || ''}</h3>
            <p class="card-desc">${short}</p>
            <div class="card-footer">
              <div class="card-price">৳${fmtPrice(p.price)}</div>
              <div class="card-stock ${stockClass}">${stockText}</div>
            </div>
          </div>
        </a>
        ${
          out
            ? `<button class="btn-buy disabled" disabled>Out of Stock</button>`
            : `<a href="${buyHref}" class="btn-buy">Buy Now →</a>`
        }
      `;
      return wrap;
    };

    const renderProducts = () => {
      if (!el.grid) return;
      el.grid.innerHTML = '';
      const items = state.products || [];
      if (el.count) el.count.textContent = `${items.length} items`;

      const title = state.category ? `${state.category} Parts` : state.search ? `Search Results` : 'All Spare Parts';
      if (el.title) el.title.textContent = title;

      if (el.searchInfo) {
        if (state.search) {
          el.searchInfo.style.display = 'block';
          el.searchInfo.innerHTML = `Showing results for "<strong>${state.search.replaceAll('<', '&lt;')}</strong>" <button type="button" class="clear-search" id="spa-clear-search">✕ Clear</button>`;
          const clearBtn = document.getElementById('spa-clear-search');
          clearBtn?.addEventListener('click', () => {
            state.search = '';
            const searchInput = document.querySelector('.search-input');
            if (searchInput) searchInput.value = '';
            loadProducts();
          });
        } else {
          el.searchInfo.style.display = 'none';
          el.searchInfo.innerHTML = '';
        }
      }

      if (items.length === 0) {
        if (el.empty) el.empty.style.display = 'block';
        return;
      }
      if (el.empty) el.empty.style.display = 'none';

      items.forEach(p => el.grid.appendChild(productCard(p)));
    };

    const loadCategories = async () => {
      const res = await fetch('/api/categories');
      const body = await res.json();
      state.categories = Array.isArray(body.categories) ? body.categories : [];
      renderCategories();
    };

    const loadProducts = async () => {
      const res = await fetch(`/api/products?${qs({ category: state.category, search: state.search })}`);
      const body = await res.json();
      state.products = Array.isArray(body.products) ? body.products : [];
      renderProducts();
    };

    // Hook navbar search form to SPA fetch
    const searchForm = document.querySelector('.search-form');
    searchForm?.addEventListener('submit', (e) => {
      e.preventDefault();
      const searchInput = document.querySelector('.search-input');
      state.search = (searchInput?.value || '').trim();
      loadProducts();
    });

    loadCategories().then(loadProducts).catch(() => loadProducts());
    return;
  }

  // Product card entrance animation
  if (typeof IntersectionObserver !== 'undefined') {
    const cards = document.querySelectorAll('.product-card');
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          setTimeout(() => {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }, i * 60);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    cards.forEach(card => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(16px)';
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      observer.observe(card);
    });
  }

  // Mobile nav search toggle
  const searchInput = document.querySelector('.search-input');
  if (searchInput) {
    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') searchInput.blur();
    });
  }
});
