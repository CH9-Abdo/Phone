// ============================================================
// DJELLAL BOUTIQUE — Main Application Logic
// Depends on: js/phones_data.js (must be loaded before this)
// ============================================================

// --- State ---
let currentData = [];
let currentPage = 1;
const ITEMS_PER_PAGE = 12;
let compareList = [];

// --- DOM Ready ---
document.addEventListener('DOMContentLoaded', () => {
    if (typeof products === 'undefined' || typeof brands === 'undefined') {
        console.error('Error: Phone data not loaded!');
        return;
    }
    currentData = [...products];
    initTheme();
    setupEventListeners();
    renderPage();
    initPriceSlider();
});

// ============================================================
// THEME
// ============================================================
function initTheme() {
    const saved = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const isDark = saved === 'dark' || (!saved && prefersDark);
    setTheme(isDark);
}

function toggleTheme() {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    setTheme(!isDark);
    localStorage.setItem('theme', !isDark ? 'dark' : 'light');
}

function setTheme(isDark) {
    if (isDark) {
        document.body.setAttribute('data-theme', 'dark');
    } else {
        document.body.removeAttribute('data-theme');
    }
    updateThemeIcon(isDark);
}

function updateThemeIcon(isDark) {
    const btn = document.getElementById('themeToggle');
    if (btn) btn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

// ============================================================
// SETUP
// ============================================================
function setupEventListeners() {
    renderBrands();
    populateCalculator();

    document.getElementById('mainSearch')?.addEventListener('input', debounce(handleSearch, 280));
    document.getElementById('priceRange')?.addEventListener('input', handleFilters);
    document.getElementById('sortSelect')?.addEventListener('change', handleSort);

    document.querySelectorAll('.screen-filter, .refresh-filter, .ram-filter').forEach(el => {
        el.addEventListener('change', handleFilters);
    });

    document.getElementById('calcPhone')?.addEventListener('change', calculateInstallment);
    document.getElementById('calcPlan')?.addEventListener('change', calculateInstallment);

    // Sidebar overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.onclick = toggleSidebar;
    document.body.appendChild(overlay);

    // Sidebar close button
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        const closeBtn = document.createElement('div');
        closeBtn.className = 'sidebar-close';
        closeBtn.innerHTML = '<i class="fas fa-times"></i>';
        closeBtn.onclick = toggleSidebar;
        sidebar.prepend(closeBtn);
    }

    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeModal();
            closeCompareModal();
        }
    });
}

// ============================================================
// RENDER PAGE
// ============================================================
function renderPage() {
    renderGrid(currentData);
    renderPagination(currentData);
}

// ============================================================
// PRICE SLIDER
// ============================================================
function initPriceSlider() {
    const slider = document.getElementById('priceRange');
    if (!slider) return;
    updateSliderTrack(slider);
    slider.addEventListener('input', () => updateSliderTrack(slider));
}

function updateSliderTrack(slider) {
    const min = parseInt(slider.min);
    const max = parseInt(slider.max);
    const val = parseInt(slider.value);
    const pct = ((val - min) / (max - min)) * 100;
    slider.style.background = `linear-gradient(to left, var(--green) ${pct}%, var(--border) ${pct}%)`;
    const priceMaxEl = document.getElementById('priceMax');
    if (priceMaxEl) {
        priceMaxEl.textContent = val >= parseInt(slider.max)
            ? parseInt(slider.max).toLocaleString() + '+'
            : val.toLocaleString();
    }
}

// ============================================================
// FILTERING & SORTING
// ============================================================
function handleFilters() {
    const searchQuery = document.getElementById('mainSearch').value.toLowerCase().trim();
    const maxPrice = parseInt(document.getElementById('priceRange').value);

    updateSliderTrack(document.getElementById('priceRange'));

    const selectedBrands  = getChecked('.brand-filter');
    const selectedScreens = getChecked('.screen-filter');
    const selectedRefresh = getChecked('.refresh-filter');
    const selectedRam     = getChecked('.ram-filter');

    let filtered = products.filter(p => {
        const matchesSearch =
            !searchQuery ||
            p.name.toLowerCase().includes(searchQuery) ||
            p.brand.toLowerCase().includes(searchQuery) ||
            Object.values(p.specs).some(v => v && v.toLowerCase().includes(searchQuery));

        const matchesPrice   = p.price <= maxPrice;
        const matchesBrand   = selectedBrands.length === 0   || selectedBrands.includes(p.brand);
        const matchesScreen  = selectedScreens.length === 0  || (p.specs.screen  && selectedScreens.some(s => p.specs.screen.includes(s)));
        const matchesRefresh = selectedRefresh.length === 0  || (p.specs.refresh && selectedRefresh.some(r => p.specs.refresh.includes(r)));
        const matchesRam     = selectedRam.length === 0      || (p.specs.ram     && selectedRam.some(r => p.specs.ram.includes(r)));

        return matchesSearch && matchesPrice && matchesBrand && matchesScreen && matchesRefresh && matchesRam;
    });

    currentData = filtered;
    currentPage = 1;
    applySortAndRender();
}

function handleSearch() {
    handleFilters();
    if (document.getElementById('mainSearch').value.length > 0) {
        scrollToElement('products-area');
    }
}

function handleSort(shouldRender = true) {
    applySortAndRender();
}

function applySortAndRender() {
    const sortType = document.getElementById('sortSelect').value;
    let sorted = [...currentData];

    switch (sortType) {
        case 'priceLow':  sorted.sort((a, b) => a.price - b.price); break;
        case 'priceHigh': sorted.sort((a, b) => b.price - a.price); break;
        case 'refresh':   sorted.sort((a, b) => (parseInt(b.specs.refresh) || 0) - (parseInt(a.specs.refresh) || 0)); break;
        case 'rating':    sorted.sort((a, b) => (b.rating || 0) - (a.rating || 0)); break;
        default:          sorted.sort((a, b) => b.id - a.id);
    }

    currentData = sorted;
    renderPage();
}

function resetFilters() {
    // Uncheck all checkboxes
    document.querySelectorAll('.brand-filter, .screen-filter, .refresh-filter, .ram-filter').forEach(el => {
        el.checked = false;
    });
    // Reset price slider
    const slider = document.getElementById('priceRange');
    if (slider) {
        slider.value = slider.max;
        updateSliderTrack(slider);
    }
    // Reset search
    const searchInput = document.getElementById('mainSearch');
    if (searchInput) searchInput.value = '';

    currentData = [...products];
    currentPage = 1;
    applySortAndRender();
}

// ============================================================
// RENDER GRID
// ============================================================
function renderGrid(data) {
    const grid  = document.getElementById('productsGrid');
    const count = document.getElementById('resultsCountNum');
    if (!grid) return;

    const start = (currentPage - 1) * ITEMS_PER_PAGE;
    const end   = start + ITEMS_PER_PAGE;
    const page  = data.slice(start, end);

    grid.innerHTML = '';
    if (count) count.textContent = data.length;

    if (data.length === 0) {
        grid.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-search"></i>
                <h3>لا توجد نتائج</h3>
                <p>حاول تعديل الفلاتر أو البحث بكلمات أخرى</p>
                <button class="btn btn-outline" style="margin-top: 16px;" onclick="resetFilters()">إعادة ضبط الفلاتر</button>
            </div>`;
        return;
    }

    page.forEach((p, idx) => {
        const card = document.createElement('div');
        card.className = 'product-card animate-fade';
        card.style.animationDelay = `${idx * 0.04}s`;

        const installment12 = Math.round((p.price * 1.45) / 12);
        const badgeHtml     = p.tags && p.tags.length > 0
            ? `<span class="product-badge">${p.tags[0]}</span>` : '';
        const batteryShort  = p.specs.battery ? p.specs.battery.split(' / ')[0] : 'N/A';
        const isCompared    = compareList.includes(p.id);

        card.innerHTML = `
            ${badgeHtml}
            <div class="product-img-wrap" onclick="openModal(${p.id})">
                <img src="${p.image}"
                     alt="${p.name}"
                     class="product-image"
                     loading="lazy"
                     onerror="this.src='https://via.placeholder.com/200x200?text=${encodeURIComponent(p.brand)}'">
                <div class="product-img-overlay">
                    <span><i class="fas fa-eye"></i> عرض التفاصيل</span>
                </div>
            </div>

            <div class="product-info">
                <div class="product-brand">${p.brand}</div>
                <h3 class="product-name" onclick="openModal(${p.id})">${p.name}</h3>
                <div class="star-rating">${renderStars(p.rating)}</div>
                <div class="product-price">
                    ${p.price.toLocaleString()} <small>DZD</small>
                </div>
                <div class="payment-pill">
                    <i class="fas fa-credit-card" style="margin-left: 4px; font-size: 10px;"></i>
                    تقسيط يبدأ من ${installment12.toLocaleString()} DZD/شهر
                </div>
                <div class="product-specs">
                    <span><i class="fas fa-microchip"></i> ${p.specs.ram}</span>
                    <span><i class="fas fa-hdd"></i> ${p.specs.storage}</span>
                    <span><i class="fas fa-mobile"></i> ${p.specs.refresh}</span>
                    <span><i class="fas fa-battery-full"></i> ${batteryShort}</span>
                </div>
                <label class="checkbox-container">
                    <input type="checkbox" onchange="toggleCompare(${p.id}, this)" ${isCompared ? 'checked' : ''}>
                    <span>مقارنة</span>
                </label>
            </div>

            <div class="product-actions">
                <button class="btn btn-outline" onclick="openModal(${p.id})">
                    <i class="fas fa-info-circle"></i> التفاصيل
                </button>
                <button class="btn btn-primary" onclick="openModal(${p.id})">
                    <i class="fas fa-shopping-bag"></i> اطلب الآن
                </button>
            </div>`;

        grid.appendChild(card);
    });
}

// ============================================================
// PAGINATION
// ============================================================
function renderPagination(data) {
    const container  = document.getElementById('pagination-controls');
    if (!container) return;

    const totalPages = Math.ceil(data.length / ITEMS_PER_PAGE);
    container.innerHTML = '';
    if (totalPages <= 1) return;

    const mkBtn = (label, page, disabled = false, active = false) => {
        const btn = document.createElement('button');
        btn.className = 'page-btn' + (active ? ' active' : '');
        btn.innerHTML = label;
        btn.disabled = disabled;
        if (!disabled) {
            btn.onclick = () => {
                currentPage = page;
                renderPage();
                scrollToElement('products-area');
            };
        }
        return btn;
    };

    container.appendChild(mkBtn('&laquo;', currentPage - 1, currentPage === 1));

    // Show limited page range
    const range = 2;
    for (let i = 1; i <= totalPages; i++) {
        if (i === 1 || i === totalPages || (i >= currentPage - range && i <= currentPage + range)) {
            container.appendChild(mkBtn(i, i, false, i === currentPage));
        } else if (
            (i === currentPage - range - 1 || i === currentPage + range + 1) &&
            totalPages > 7
        ) {
            const dots = document.createElement('span');
            dots.textContent = '…';
            dots.style.cssText = 'padding: 0 6px; color: var(--text-4); line-height: 40px;';
            container.appendChild(dots);
        }
    }

    container.appendChild(mkBtn('&raquo;', currentPage + 1, currentPage === totalPages));
}

// ============================================================
// BRANDS
// ============================================================
function renderBrands() {
    const container = document.getElementById('brandFilters');
    if (!container) return;
    container.innerHTML = '';
    brands.forEach(brand => {
        const label = document.createElement('label');
        label.innerHTML = `<input type="checkbox" class="brand-filter" value="${brand}"> ${brand}`;
        label.querySelector('input').addEventListener('change', handleFilters);
        container.appendChild(label);
    });
}

// ============================================================
// STARS
// ============================================================
function renderStars(rating) {
    let html = '';
    for (let i = 1; i <= 5; i++) {
        if (i <= Math.floor(rating)) {
            html += '<i class="fas fa-star"></i>';
        } else if (i - rating < 1) {
            html += '<i class="fas fa-star-half-alt"></i>';
        } else {
            html += '<i class="far fa-star"></i>';
        }
    }
    return html;
}

// ============================================================
// MODAL
// ============================================================
function openModal(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;

    const installment12 = Math.round((p.price * 1.45) / 12);

    document.getElementById('modalGallery').innerHTML = `
        <img src="${p.image}" alt="${p.name}"
             onerror="this.src='https://via.placeholder.com/400x400?text=${encodeURIComponent(p.brand)}'">`;

    document.getElementById('modalBrand').textContent   = p.brand;
    document.getElementById('modalName').textContent    = p.name;
    document.getElementById('modalRating').innerHTML    = renderStars(p.rating);
    document.getElementById('modalPrice').textContent   = `${p.price.toLocaleString()} DZD`;
    document.getElementById('modalInstallmentBadge').textContent = `أو ${installment12.toLocaleString()} DZD/شهر`;

    const plans = [
        { label: 'دفع كاش',           total: p.price,        monthly: p.price,              months: 1  },
        { label: 'تقسيط 6 أشهر (+25%)', total: p.price * 1.25, monthly: (p.price * 1.25) / 6,  months: 6  },
        { label: 'تقسيط 8 أشهر (+35%)', total: p.price * 1.35, monthly: (p.price * 1.35) / 8,  months: 8  },
        { label: 'تقسيط 12 شهر (+45%)', total: p.price * 1.45, monthly: (p.price * 1.45) / 12, months: 12 },
    ];

    document.getElementById('modalPaymentPlans').innerHTML = plans.map(plan => `
        <div class="plan-row">
            <span>${plan.label}</span>
            <span>${Math.round(plan.monthly).toLocaleString()} DZD / شهر</span>
        </div>`).join('');

    // Specs table
    const specsTable = document.getElementById('modalSpecs');
    specsTable.innerHTML = '';
    const icons = {
        screen: 'fa-mobile', refresh: 'fa-tachometer-alt', ram: 'fa-memory',
        storage: 'fa-hdd', camera: 'fa-camera', battery: 'fa-battery-full',
        processor: 'fa-microchip', network: 'fa-wifi'
    };
    for (const [key, value] of Object.entries(p.specs)) {
        const row = specsTable.insertRow();
        const iconClass = icons[key] || 'fa-circle';
        row.insertCell(0).innerHTML = `<i class="fas ${iconClass}" style="color:var(--green); margin-left: 6px;"></i> ${translateKey(key)}`;
        row.insertCell(1).textContent = value;
    }

    // WhatsApp link
    const message = encodeURIComponent(`مرحباً Djellal Boutique، أريد الاستفسار عن ${p.name} وخطط التقسيط المتاحة.`);
    document.getElementById('whatsappBtn').href = `https://wa.me/213540203685?text=${message}`;

    document.getElementById('productModal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('productModal').style.display = 'none';
    document.body.style.overflow = '';
}

function translateKey(key) {
    const map = {
        screen: 'الشاشة', refresh: 'معدل التحديث', ram: 'RAM',
        storage: 'التخزين', camera: 'الكاميرا', battery: 'البطارية / الشحن',
        processor: 'المعالج', network: 'الشبكة'
    };
    return map[key] || key;
}

// ============================================================
// CALCULATOR
// ============================================================
function populateCalculator() {
    const select = document.getElementById('calcPhone');
    if (!select) return;
    select.innerHTML = '';
    [...products].sort((a, b) => a.name.localeCompare(b.name)).forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.price;
        opt.textContent = `${p.name} — ${p.price.toLocaleString()} DZD`;
        select.appendChild(opt);
    });
    calculateInstallment();
}

function calculateInstallment() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect  = document.getElementById('calcPlan');
    const resultEl    = document.getElementById('calcResult');
    if (!phoneSelect || !planSelect || !resultEl) return;

    const price = parseFloat(phoneSelect.value);
    const [multiplierStr, monthsStr] = planSelect.value.split('|');
    const multiplier = parseFloat(multiplierStr);
    const months     = parseInt(monthsStr);
    const monthly    = Math.round((price * multiplier) / months);

    resultEl.textContent = `${monthly.toLocaleString()} DZD / شهر`;
}

function requestOnWhatsapp() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect  = document.getElementById('calcPlan');
    const resultEl    = document.getElementById('calcResult');
    if (!phoneSelect || !planSelect || !resultEl) return;

    const phoneName = phoneSelect.options[phoneSelect.selectedIndex].text;
    const planName  = planSelect.options[planSelect.selectedIndex].text;
    const result    = resultEl.textContent;
    const msg = encodeURIComponent(`مرحباً Djellal Boutique،\nأود طلب تقسيط لـ: ${phoneName}\nخطة الدفع: ${planName}\nالقسط الشهري المقدر: ${result}`);
    window.open(`https://wa.me/213540203685?text=${msg}`, '_blank');
}

// ============================================================
// COMPARISON
// ============================================================
function toggleCompare(id, checkbox) {
    if (checkbox.checked) {
        if (compareList.length >= 3) {
            showToast('يمكنك مقارنة 3 هواتف كحد أقصى', 'warning');
            checkbox.checked = false;
            return;
        }
        if (!compareList.includes(id)) compareList.push(id);
    } else {
        compareList = compareList.filter(item => item !== id);
    }
    updateCompareBar();
}

function updateCompareBar() {
    const bar    = document.getElementById('compareBar');
    const thumbs = document.getElementById('compareThumbs');
    const count  = document.getElementById('compareCount');

    bar.classList.toggle('active', compareList.length > 0);
    count.textContent = compareList.length;
    thumbs.innerHTML = '';

    compareList.forEach(id => {
        const p = products.find(x => x.id === id);
        if (p) {
            const img = document.createElement('img');
            img.src = p.image;
            img.className = 'compare-thumb';
            img.alt = p.name;
            thumbs.appendChild(img);
        }
    });
}

function clearComparison() {
    compareList = [];
    updateCompareBar();
    renderGrid(currentData);
}

function openCompareModal() {
    if (compareList.length < 2) {
        showToast('الرجاء اختيار هاتفين على الأقل للمقارنة', 'info');
        return;
    }

    const table  = document.getElementById('compareTable');
    const phones = compareList.map(id => products.find(p => p.id === id));

    let html = '<tr><th>المواصفات</th>';
    phones.forEach(p => {
        html += `<td>
            <img src="${p.image}" class="compare-header-img" alt="${p.name}">
            <div style="font-weight: 800; margin-bottom: 4px;">${p.name}</div>
            <div style="color: var(--green); font-weight: 700;">${p.price.toLocaleString()} DZD</div>
            <span class="compare-remove" onclick="removeFromCompare(${p.id})">
                <i class="fas fa-times"></i> إزالة
            </span>
        </td>`;
    });
    html += '</tr>';

    const specsKeys = ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network'];
    specsKeys.forEach(key => {
        html += `<tr><td>${translateKey(key)}</td>`;
        phones.forEach(p => { html += `<td>${p.specs[key] || '—'}</td>`; });
        html += '</tr>';
    });

    table.innerHTML = html;
    document.getElementById('compareModal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function removeFromCompare(id) {
    compareList = compareList.filter(item => item !== id);
    updateCompareBar();
    if (compareList.length < 1) {
        closeCompareModal();
    } else {
        openCompareModal();
    }
}

function closeCompareModal() {
    document.getElementById('compareModal').style.display = 'none';
    document.body.style.overflow = '';
}

// ============================================================
// SIDEBAR
// ============================================================
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    const isOpen  = sidebar?.classList.contains('active');

    sidebar?.classList.toggle('active');
    overlay?.classList.toggle('active');
    document.body.style.overflow = !isOpen ? 'hidden' : '';
}

// ============================================================
// UTILS
// ============================================================
function scrollToElement(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function focusSearch() {
    const input = document.getElementById('mainSearch');
    if (input) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => input.focus(), 350);
    }
}

function getChecked(selector) {
    return Array.from(document.querySelectorAll(`${selector}:checked`)).map(el => el.value);
}

function debounce(fn, delay) {
    let timer;
    return (...args) => {
        clearTimeout(timer);
        timer = setTimeout(() => fn(...args), delay);
    };
}

// Simple toast notification
function showToast(message, type = 'info') {
    const existing = document.querySelector('.dj-toast');
    if (existing) existing.remove();

    const toast = document.createElement('div');
    toast.className = 'dj-toast';
    const colors = { info: '#3b82f6', warning: '#f59e0b', success: '#00a86b', error: '#e8183a' };
    toast.style.cssText = `
        position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%);
        background: ${colors[type] || colors.info}; color: white;
        padding: 12px 24px; border-radius: 50px; font-size: 14px; font-weight: 600;
        font-family: 'Tajawal', sans-serif; z-index: 9999; box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        animation: fadeInUp 0.3s ease; white-space: nowrap;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity 0.3s'; setTimeout(() => toast.remove(), 350); }, 2800);
}

// Close modals on backdrop click
window.onclick = function(event) {
    if (event.target === document.getElementById('productModal')) closeModal();
    if (event.target === document.getElementById('compareModal')) closeCompareModal();
};
