// Main Application Logic
// Depends on: js/phones_data.js (which must be loaded before this script)

// --- State Management ---
let currentData = [];
let currentPage = 1;
const itemsPerPage = 12;
let compareList = []; // IDs of phones to compare

// --- DOM Ready ---
document.addEventListener('DOMContentLoaded', () => {
    if (typeof products === 'undefined' || typeof brands === 'undefined') {
        console.error("Error: Phone data not loaded! Check if phones_data.js is included.");
        return;
    }

    currentData = [...products]; // Initialize with all products
    
    initTheme(); // Initialize Dark Mode
    setupEventListeners();
    renderPage();
});

// --- Theme Management ---
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        document.body.setAttribute('data-theme', 'dark');
        updateThemeIcon(true);
    } else {
        document.body.removeAttribute('data-theme');
        updateThemeIcon(false);
    }
}

function toggleTheme() {
    const isDark = document.body.getAttribute('data-theme') === 'dark';
    if (isDark) {
        document.body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        updateThemeIcon(false);
    } else {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        updateThemeIcon(true);
    }
}

function updateThemeIcon(isDark) {
    const btn = document.getElementById('themeToggle');
    if(btn) btn.innerHTML = isDark ? '<i class="fas fa-sun"></i>' : '<i class="fas fa-moon"></i>';
}

// --- Setup ---
function setupEventListeners() {
    renderBrands();
    populateCalculator();
    
    document.getElementById('mainSearch')?.addEventListener('input', handleSearch);
    document.getElementById('priceRange')?.addEventListener('input', handleFilters);
    document.getElementById('sortSelect')?.addEventListener('change', handleSort);
    document.querySelectorAll('.screen-filter, .refresh-filter, .ram-filter').forEach(el => {
        el.addEventListener('change', handleFilters);
    });
    document.getElementById('calcPhone')?.addEventListener('change', calculateInstallment);
    document.getElementById('calcPlan')?.addEventListener('change', calculateInstallment);

    // Sidebar overlay and close button
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.onclick = toggleSidebar;
    document.body.appendChild(overlay);
    
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        const closeBtn = document.createElement('div');
        closeBtn.className = 'sidebar-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = toggleSidebar;
        sidebar.prepend(closeBtn);
    }
}

// --- Main Rendering Function ---
function renderPage() {
    renderGrid(currentData);
    renderPagination(currentData);
}

// --- Data Filtering and Sorting ---
function handleFilters() {
    const searchQuery = document.getElementById('mainSearch').value.toLowerCase();
    const maxPrice = document.getElementById('priceRange').value;
    
    document.getElementById('priceMax').innerText = parseInt(maxPrice).toLocaleString();

    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(el => el.value);
    const selectedScreens = Array.from(document.querySelectorAll('.screen-filter:checked')).map(el => el.value);
    const selectedRefresh = Array.from(document.querySelectorAll('.refresh-filter:checked')).map(el => el.value);
    const selectedRam = Array.from(document.querySelectorAll('.ram-filter:checked')).map(el => el.value);

    let filtered = products.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery) || 
                              p.brand.toLowerCase().includes(searchQuery) ||
                              (p.specs.screen && p.specs.screen.toLowerCase().includes(searchQuery)) ||
                              (p.specs.refresh && p.specs.refresh.toLowerCase().includes(searchQuery));
                              
        const matchesPrice = p.price <= maxPrice;
        const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(p.brand);
        const matchesScreen = selectedScreens.length === 0 || (p.specs.screen && selectedScreens.some(s => p.specs.screen.includes(s)));
        const matchesRefresh = selectedRefresh.length === 0 || (p.specs.refresh && selectedRefresh.some(r => p.specs.refresh.includes(r)));
        const matchesRam = selectedRam.length === 0 || (p.specs.ram && selectedRam.some(ram => p.specs.ram.includes(ram)));

        return matchesSearch && matchesPrice && matchesBrand && matchesScreen && matchesRefresh && matchesRam;
    });

    currentData = filtered;
    currentPage = 1; // Reset to first page
    handleSort(false); // Apply current sort to the new filtered data
}

function handleSearch() {
    handleFilters();
    // Auto scroll to products if user types and is at the top
    const searchInput = document.getElementById('mainSearch');
    if (searchInput.value.length > 0) {
         scrollToElement('products-area');
    }
}

function handleSort(shouldRender = true) {
    const sortType = document.getElementById('sortSelect').value;
    let sorted = [...currentData];

    switch(sortType) {
        case 'priceLow': sorted.sort((a,b) => a.price - b.price); break;
        case 'priceHigh': sorted.sort((a,b) => b.price - a.price); break;
        case 'refresh': sorted.sort((a,b) => (parseInt(b.specs.refresh) || 0) - (parseInt(a.specs.refresh) || 0)); break;
        default: sorted.sort((a,b) => b.id - a.id);
    }
    
    currentData = sorted;
    if (shouldRender) {
        currentPage = 1; // Reset to first page
        renderPage();
    } else {
        // This is called from handleFilters, so renderPage() will be called there
        renderPage();
    }
}


// --- UI Rendering ---
function renderGrid(data) {
    const grid = document.getElementById('productsGrid');
    const count = document.getElementById('resultsCount');
    if (!grid) return;

    // Pagination logic
    const start = (currentPage - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    const paginatedItems = data.slice(start, end);

    grid.innerHTML = '';
    count.innerText = `عرض ${data.length} هاتف`;
    
    if (data.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">لا توجد نتائج تطابق بحثك</div>';
        return;
    }

    paginatedItems.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card animate-fade';
        const installment12 = Math.round((p.price * 1.45) / 12);
        const tagsHtml = p.tags && p.tags.length > 0 ? `<span class="product-badge">${p.tags[0]}</span>` : '';
        const batteryDisplay = p.specs.battery ? p.specs.battery.split(' / ')[0] : 'N/A';
        const isCompared = compareList.includes(p.id);

        card.innerHTML = `
            ${tagsHtml}
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; overflow: hidden; background: #fff; cursor: pointer;" onclick="openModal(${p.id})">
                <img src="${p.image}" alt="${p.name}" class="product-image" onerror="this.src='https://via.placeholder.com/200x250?text=No+Image'">
            </div>
            <div class="product-info">
                <div class="product-brand">${p.brand}</div>
                <h3 class="product-name" style="cursor: pointer;" onclick="openModal(${p.id})">${p.name}</h3>
                <div class="star-rating">${renderStars(p.rating)}</div>
                <div class="product-price">${p.price.toLocaleString()} DZD</div>
                <div class="payment-pill">أو تقسيط يبدأ من ${installment12.toLocaleString()} DZD/شهر</div>
                <div class="product-specs">
                    <span><i class="fas fa-microchip"></i> ${p.specs.ram}</span>
                    <span><i class="fas fa-hdd"></i> ${p.specs.storage}</span>
                    <span><i class="fas fa-mobile"></i> ${p.specs.refresh}</span>
                    <span><i class="fas fa-battery-full"></i> ${batteryDisplay}</span>
                </div>
                
                <label class="checkbox-container">
                    <input type="checkbox" onchange="toggleCompare(${p.id}, this)" ${isCompared ? 'checked' : ''}>
                    <span>مقارنة</span>
                </label>
            </div>
            <div class="product-actions">
                <button class="btn btn-outline detail-btn" onclick="openModal(${p.id})">التفاصيل</button>
                <button class="btn btn-primary" onclick="buyNow(${p.id})">اطلب الآن</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

// --- Comparison Logic ---
function toggleCompare(id, checkbox) {
    if (checkbox.checked) {
        if (compareList.length >= 3) {
            alert("يمكنك مقارنة 3 هواتف كحد أقصى");
            checkbox.checked = false;
            return;
        }
        if (!compareList.includes(id)) {
            compareList.push(id);
        }
    } else {
        compareList = compareList.filter(item => item !== id);
    }
    updateCompareBar();
}

function updateCompareBar() {
    const bar = document.getElementById('compareBar');
    const thumbs = document.getElementById('compareThumbs');
    const count = document.getElementById('compareCount');
    
    if (compareList.length > 0) {
        bar.classList.add('active');
    } else {
        bar.classList.remove('active');
    }
    
    count.innerText = compareList.length;
    thumbs.innerHTML = '';
    
    compareList.forEach(id => {
        const p = products.find(x => x.id === id);
        if (p) {
            const img = document.createElement('img');
            img.src = p.image;
            img.className = 'compare-thumb';
            thumbs.appendChild(img);
        }
    });
}

function clearComparison() {
    compareList = [];
    updateCompareBar();
    renderGrid(currentData); // Re-render to uncheck boxes
}

function openCompareModal() {
    if (compareList.length < 2) {
        alert("الرجاء اختيار هاتفين على الأقل للمقارنة");
        return;
    }
    
    const table = document.getElementById('compareTable');
    table.innerHTML = '';
    
    const phones = compareList.map(id => products.find(p => p.id === id));
    
    // Header Row (Images & Names)
    let headerRow = '<tr><th>المواصفات</th>';
    phones.forEach(p => {
        headerRow += `
            <td>
                <img src="${p.image}" class="compare-header-img">
                <div style="font-weight:bold;">${p.name}</div>
                <div style="color:var(--primary-color);">${p.price.toLocaleString()} DZD</div>
            </td>
        `;
    });
    headerRow += '</tr>';
    table.innerHTML += headerRow;
    
    // Specs Rows
    const specsKeys = ['screen', 'refresh', 'ram', 'storage', 'camera', 'battery', 'processor', 'network'];
    
    specsKeys.forEach(key => {
        let row = `<tr><td>${translateKey(key)}</td>`;
        phones.forEach(p => {
            row += `<td>${p.specs[key] || '-'}</td>`;
        });
        row += '</tr>';
        table.innerHTML += row;
    });

    document.getElementById('compareModal').style.display = 'flex';
}

function closeCompareModal() {
    document.getElementById('compareModal').style.display = 'none';
}

function renderPagination(data) {
    const paginationContainer = document.getElementById('pagination-controls');
    if (!paginationContainer) return;
    
    const totalItems = data.length;
    const totalPages = Math.ceil(totalItems / itemsPerPage);

    paginationContainer.innerHTML = '';
    
    if (totalPages <= 1) return;

    // Previous Button
    const prevButton = document.createElement('button');
    prevButton.className = 'page-btn';
    prevButton.innerHTML = '&laquo; السابق';
    prevButton.disabled = currentPage === 1;
    prevButton.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage();
            scrollToElement('products-area');
        }
    };
    paginationContainer.appendChild(prevButton);

    // Page Numbers
    for (let i = 1; i <= totalPages; i++) {
        const pageButton = document.createElement('button');
        pageButton.className = 'page-btn';
        pageButton.innerText = i;
        if (i === currentPage) {
            pageButton.classList.add('active');
        }
        pageButton.onclick = () => {
            currentPage = i;
            renderPage();
            scrollToElement('products-area');
        };
        paginationContainer.appendChild(pageButton);
    }

    // Next Button
    const nextButton = document.createElement('button');
    nextButton.className = 'page-btn';
    nextButton.innerHTML = 'التالي &raquo;';
    nextButton.disabled = currentPage === totalPages;
    nextButton.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage();
            scrollToElement('products-area');
        }
    };
    paginationContainer.appendChild(nextButton);
}

// --- Other UI Components ---

function toggleSidebar() {
    document.querySelector('.sidebar')?.classList.toggle('active');
    document.querySelector('.sidebar-overlay')?.classList.toggle('active');
    document.body.style.overflow = document.querySelector('.sidebar.active') ? 'hidden' : 'auto';
}

function focusSearch() {
    const searchInput = document.getElementById('mainSearch');
    if (searchInput) {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        setTimeout(() => searchInput.focus(), 300);
    }
}

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

function renderStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += `<i class="${i <= rating ? 'fas' : 'far'} fa-star"></i>`;
    }
    return stars;
}

// --- Modal ---
function openModal(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;

    document.getElementById('modalGallery').innerHTML = `<img src="${p.image}" alt="${p.name}" onerror="this.src='https://via.placeholder.com/400x400?text=No+Image'">`;
    document.getElementById('modalBrand').innerText = p.brand;
    document.getElementById('modalName').innerText = p.name;
    document.getElementById('modalRating').innerHTML = renderStars(p.rating);
    document.getElementById('modalPrice').innerText = `${p.price.toLocaleString()} DZD`;

    const plans = [
        { label: "دفع كاش", total: p.price, monthly: p.price, months: 1 },
        { label: "تقسيط 6 أشهر (+25%)", total: p.price * 1.25, monthly: (p.price * 1.25) / 6, months: 6 },
        { label: "تقسيط 8 أشهر (+35%)", total: p.price * 1.35, monthly: (p.price * 1.35) / 8, months: 8 },
        { label: "تقسيط 12 شهر (+45%)", total: p.price * 1.45, monthly: (p.price * 1.45) / 12, months: 12 }
    ];

    document.getElementById('modalPaymentPlans').innerHTML = plans.map(plan => `
        <div class="plan-row">
            <span><strong>${plan.label}</strong></span>
            <span>${Math.round(plan.monthly).toLocaleString()} DZD / شهر</span>
        </div>
    `).join('');

    const specsTable = document.getElementById('modalSpecs');
    specsTable.innerHTML = '';
    for (const [key, value] of Object.entries(p.specs)) {
        const row = specsTable.insertRow();
        row.insertCell(0).innerText = translateKey(key);
        row.insertCell(1).innerText = value;
    }

    const message = encodeURIComponent(`مرحباً Djellal Boutique، أريد الاستفسار عن ${p.name} وخطط التقسيط المتاحة.`);
    document.getElementById('whatsappBtn').href = `https://wa.me/213540203685?text=${message}`;

    document.getElementById('productModal').style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    document.getElementById('productModal').style.display = 'none';
    document.body.style.overflow = 'auto';
}

function translateKey(key) {
    const keys = { screen: "الشاشة", refresh: "معدل التحديث", ram: "الرام (RAM)", storage: "التخزين", camera: "الكاميرات", battery: "البطارية / الشحن", processor: "المعالج", network: "الشبكة" };
    return keys[key] || key;
}

function populateCalculator() {
    const select = document.getElementById('calcPhone');
    if (!select) return;
    select.innerHTML = '';
    products.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.price;
        opt.innerText = `${p.name} (${p.price.toLocaleString()} DZD)`;
        select.appendChild(opt);
    });
    calculateInstallment();
}

function calculateInstallment() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect = document.getElementById('calcPlan');
    const resultDiv = document.getElementById('calcResult');
    if (!phoneSelect || !planSelect || !resultDiv) return;
    const price = parseFloat(phoneSelect.value);
    const multiplier = parseFloat(planSelect.value);
    let months = 1;
    if (multiplier === 1.25) months = 6;
    else if (multiplier === 1.35) months = 8;
    else if (multiplier === 1.45) months = 12;
    const monthly = Math.round((price * multiplier) / months);
    resultDiv.innerText = `${monthly.toLocaleString()} DZD / شهر`;
}

function buyNow(id) {
    openModal(id);
}

function requestOnWhatsapp() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect = document.getElementById('calcPlan');
    const resultDiv = document.getElementById('calcResult');
    if (!phoneSelect || !planSelect || !resultDiv) return;
    const phoneName = phoneSelect.options[phoneSelect.selectedIndex].text;
    const planName = planSelect.options[planSelect.selectedIndex].text;
    const result = resultDiv.innerText;
    const msg = encodeURIComponent(`مرحباً، أود طلب تقسيط ${phoneName} باستخدام خطة ${planName}. القسط المقدر: ${result}`);
    window.open(`https://wa.me/213540203685?text=${msg}`, '_blank');
}

function scrollToElement(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
}

window.onclick = function(event) {
    const modal = document.getElementById('productModal');
    const compareModal = document.getElementById('compareModal');
    if (event.target == modal) {
        closeModal();
    }
    if (event.target == compareModal) {
        closeCompareModal();
    }
}
