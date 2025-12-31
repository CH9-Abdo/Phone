// Main Application Logic
// Depends on: js/phones_data.js (which must be loaded before this script)

// Initialize Page
document.addEventListener('DOMContentLoaded', () => {
    // Ensure data is loaded
    if (typeof products === 'undefined' || typeof brands === 'undefined') {
        console.error("Error: Phone data not loaded! Check if phones_data.js is included.");
        return;
    }

    renderBrands();
    renderProducts(products);
    populateCalculator();
    
    // Event Listeners
    const searchInput = document.getElementById('mainSearch');
    if (searchInput) {
        searchInput.addEventListener('input', handleSearch);
    }
    
    const priceRange = document.getElementById('priceRange');
    if (priceRange) {
        priceRange.addEventListener('input', handleFilters);
    }
    
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', handleSort);
    }

    document.querySelectorAll('.screen-filter, .refresh-filter, .ram-filter').forEach(el => {
        el.addEventListener('change', handleFilters);
    });

    // Calculator Listeners
    const calcPhone = document.getElementById('calcPhone');
    if (calcPhone) {
        calcPhone.addEventListener('change', calculateInstallment);
    }
    
    const calcPlan = document.getElementById('calcPlan');
    if (calcPlan) {
        calcPlan.addEventListener('change', calculateInstallment);
    }

    // Create Sidebar Overlay
    const overlay = document.createElement('div');
    overlay.className = 'sidebar-overlay';
    overlay.onclick = toggleSidebar;
    document.body.appendChild(overlay);
    
    // Add close button to sidebar
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        const closeBtn = document.createElement('div');
        closeBtn.className = 'sidebar-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = toggleSidebar;
        sidebar.prepend(closeBtn);
    }
});

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    if (sidebar && overlay) {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
        // Prevent body scroll when sidebar is open
        document.body.style.overflow = sidebar.classList.contains('active') ? 'hidden' : 'auto';
    }
}

function renderBrands() {
    const container = document.getElementById('brandFilters');
    if (!container) return;
    
    // Clear existing content to avoid duplicates if re-rendered
    container.innerHTML = '';
    
    brands.forEach(brand => {
        const label = document.createElement('label');
        label.innerHTML = `<input type="checkbox" class="brand-filter" value="${brand}"> ${brand}`;
        label.querySelector('input').addEventListener('change', handleFilters);
        container.appendChild(label);
    });
}

function renderProducts(data) {
    const grid = document.getElementById('productsGrid');
    const count = document.getElementById('resultsCount');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    if (count) {
        count.innerText = `عرض ${data.length} هاتف`;
    }

    if (data.length === 0) {
        grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 40px; color: #666;">لا توجد نتائج تطابق بحثك</div>';
        return;
    }

    data.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card animate-fade';
        
        const installment12 = Math.round((p.price * 1.45) / 12);
        
        // Handle potentially missing tags
        const tagsHtml = p.tags && p.tags.length > 0 
            ? `<span class="product-badge">${p.tags[0]}</span>` 
            : '';

        // Safe battery display
        const batteryDisplay = p.specs.battery ? p.specs.battery.split(' / ')[0] : 'N/A';

        card.innerHTML = `
            ${tagsHtml}
            <div style="height: 200px; display: flex; align-items: center; justify-content: center; overflow: hidden; background: #fff;">
                <img src="${p.image}" alt="${p.name}" class="product-image" onerror="this.src='https://via.placeholder.com/200x250?text=No+Image'">
            </div>
            <div class="product-info">
                <div class="product-brand">${p.brand}</div>
                <h3 class="product-name">${p.name}</h3>
                <div class="star-rating">${renderStars(p.rating)}</div>
                <div class="product-price">${p.price.toLocaleString()} DZD</div>
                <div class="payment-pill">أو تقسيط يبدأ من ${installment12.toLocaleString()} DZD/شهر</div>
                <div class="product-specs">
                    <span><i class="fas fa-microchip"></i> ${p.specs.ram}</span>
                    <span><i class="fas fa-hdd"></i> ${p.specs.storage}</span>
                    <span><i class="fas fa-mobile"></i> ${p.specs.refresh}</span>
                    <span><i class="fas fa-battery-full"></i> ${batteryDisplay}</span>
                </div>
            </div>
            <div class="product-actions">
                <button class="btn btn-outline" style="border-color: #ddd; color: var(--text-main);" onclick="openModal(${p.id})">التفاصيل</button>
                <button class="btn btn-primary" onclick="buyNow(${p.id})">اطلب الآن</button>
            </div>
        `;
        grid.appendChild(card);
    });
}

function renderStars(rating) {
    let stars = '';
    for (let i = 1; i <= 5; i++) {
        stars += `<i class="${i <= rating ? 'fas' : 'far'} fa-star"></i>`;
    }
    return stars;
}

function handleFilters() {
    const searchQuery = document.getElementById('mainSearch').value.toLowerCase();
    const maxPrice = document.getElementById('priceRange').value;
    
    const priceMaxDisplay = document.getElementById('priceMax');
    if (priceMaxDisplay) {
        priceMaxDisplay.innerText = parseInt(maxPrice).toLocaleString();
    }

    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(el => el.value);
    const selectedScreens = Array.from(document.querySelectorAll('.screen-filter:checked')).map(el => el.value);
    const selectedRefresh = Array.from(document.querySelectorAll('.refresh-filter:checked')).map(el => el.value);
    const selectedRam = Array.from(document.querySelectorAll('.ram-filter:checked')).map(el => el.value);

    const filtered = products.filter(p => {
        // Search Logic
        const matchesSearch = p.name.toLowerCase().includes(searchQuery) || 
                              p.brand.toLowerCase().includes(searchQuery) ||
                              (p.specs.screen && p.specs.screen.toLowerCase().includes(searchQuery)) ||
                              (p.specs.refresh && p.specs.refresh.toLowerCase().includes(searchQuery));
                              
        const matchesPrice = p.price <= maxPrice;
        
        const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(p.brand);
        
        const matchesScreen = selectedScreens.length === 0 || 
                              (p.specs.screen && selectedScreens.some(s => p.specs.screen.includes(s)));
                              
        const matchesRefresh = selectedRefresh.length === 0 || 
                               (p.specs.refresh && selectedRefresh.some(r => p.specs.refresh.includes(r)));
                               
        const matchesRam = selectedRam.length === 0 || 
                           (p.specs.ram && selectedRam.some(ram => p.specs.ram.includes(ram)));

        return matchesSearch && matchesPrice && matchesBrand && matchesScreen && matchesRefresh && matchesRam;
    });

    renderProducts(filtered);
}

function handleSearch() {
    handleFilters();
    if (window.scrollY < 400) {
        scrollToElement('products-area');
    }
}

function handleSort() {
    const sortSelect = document.getElementById('sortSelect');
    if (!sortSelect) return;
    
    const sortType = sortSelect.value;
    let sorted = [...products]; // Create a copy to sort

    switch(sortType) {
        case 'priceLow': sorted.sort((a,b) => a.price - b.price); break;
        case 'priceHigh': sorted.sort((a,b) => b.price - a.price); break;
        case 'refresh': sorted.sort((a,b) => {
            const rA = parseInt(a.specs.refresh) || 0;
            const rB = parseInt(b.specs.refresh) || 0;
            return rB - rA;
        }); break;
        // Default: Newest (by ID desc)
        default: sorted.sort((a,b) => b.id - a.id);
    }
    renderProducts(sorted);
}

function openModal(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;

    const modalGallery = document.getElementById('modalGallery');
    if (modalGallery) {
        modalGallery.innerHTML = `<img src="${p.image}" alt="${p.name}" onerror="this.src='https://via.placeholder.com/400x400?text=No+Image'">`;
    }
    
    const modalBrand = document.getElementById('modalBrand');
    if (modalBrand) modalBrand.innerText = p.brand;
    
    const modalName = document.getElementById('modalName');
    if (modalName) modalName.innerText = p.name;
    
    const modalRating = document.getElementById('modalRating');
    if (modalRating) modalRating.innerHTML = renderStars(p.rating);
    
    const modalPrice = document.getElementById('modalPrice');
    if (modalPrice) modalPrice.innerText = `${p.price.toLocaleString()} DZD`;

    const plans = [
        { label: "دفع كاش", total: p.price, monthly: p.price, months: 1 },
        { label: "تقسيط 6 أشهر (+25%)", total: p.price * 1.25, monthly: (p.price * 1.25) / 6, months: 6 },
        { label: "تقسيط 8 أشهر (+35%)", total: p.price * 1.35, monthly: (p.price * 1.35) / 8, months: 8 },
        { label: "تقسيط 12 شهر (+45%)", total: p.price * 1.45, monthly: (p.price * 1.45) / 12, months: 12 }
    ];

    const plansContainer = document.getElementById('modalPaymentPlans');
    if (plansContainer) {
        plansContainer.innerHTML = plans.map(plan => `
            <div class="plan-row">
                <span><strong>${plan.label}</strong></span>
                <span>${Math.round(plan.monthly).toLocaleString()} DZD / شهر</span>
            </div>
        `).join('');
    }

    const specsTable = document.getElementById('modalSpecs');
    if (specsTable) {
        specsTable.innerHTML = '';
        for (const [key, value] of Object.entries(p.specs)) {
            const row = specsTable.insertRow();
            row.insertCell(0).innerText = translateKey(key);
            row.insertCell(1).innerText = value;
        }
    }

    const message = encodeURIComponent(`مرحباً Djellal Boutique، أريد الاستفسار عن ${p.name} وخطط التقسيط المتاحة.`);
    const whatsappBtn = document.getElementById('whatsappBtn');
    if (whatsappBtn) {
        whatsappBtn.href = `https://wa.me/213540203685?text=${message}`;
    }

    const modal = document.getElementById('productModal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modal = document.getElementById('productModal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

function translateKey(key) {
    const keys = {
        screen: "الشاشة",
        refresh: "معدل التحديث",
        ram: "الرام (RAM)",
        storage: "التخزين",
        camera: "الكاميرات",
        battery: "البطارية / الشحن",
        processor: "المعالج",
        network: "الشبكة"
    };
    return keys[key] || key;
}

function populateCalculator() {
    const select = document.getElementById('calcPhone');
    if (!select) return;
    
    // Clear first just in case
    select.innerHTML = '';
    
    products.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.price;
        opt.innerText = `${p.name} (${p.price.toLocaleString()} DZD)`;
        select.appendChild(opt);
    });
    
    // Calculate initial value
    calculateInstallment();
}

function calculateInstallment() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect = document.getElementById('calcPlan');
    const resultDiv = document.getElementById('calcResult');
    
    if (!phoneSelect || !planSelect || !resultDiv) return;

    const price = parseFloat(phoneSelect.value);
    const multiplier = parseFloat(planSelect.value);
    
    // Default months for calculation
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
    if (event.target == modal) {
        closeModal();
    }
}