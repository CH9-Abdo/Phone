// Data: Smartphones
const products = [
    {
        id: 1,
        name: "iPhone 15 Pro Max",
        brand: "Apple",
        price: 280000,
        image: "Photos/Iphone 15 pro max.jpg",
        rating: 5.0,
        specs: {
            screen: "6.7\" Super Retina XDR OLED",
            refresh: "120Hz",
            ram: "8GB",
            storage: "256GB",
            camera: "48MP Main + 12MP Front",
            battery: "4422mAh / 27W",
            processor: "A17 Pro Bionic",
            network: "5G Support",
        },
        tags: ["New"],
    },
    {
        id: 2,
        name: "Samsung Galaxy S24 Ultra",
        brand: "Samsung",
        price: 320000,
        image: "https://v-center.dz/5519-large_default/samsung-galaxy-s24-ultra-5g.jpg",
        rating: 5.0,
        specs: {
            screen: "6.8\" Dynamic AMOLED 2X",
            refresh: "120Hz",
            ram: "12GB",
            storage: "512GB",
            camera: "200MP Quad + 12MP Front",
            battery: "5000mAh / 45W",
            processor: "Snapdragon 8 Gen 3",
            network: "5G Support",
        },
        tags: ["AI Features", "Best Screen"],
    },
    {
        id: 3,
        name: "Xiaomi 14 Ultra",
        brand: "Xiaomi",
        price: 245000,
        image: "https://v-center.dz/5722-large_default/xiaomi-14-ultra-16gb-512gb.jpg",
        rating: 4.8,
        specs: {
            screen: "6.73\" LTPO AMOLED",
            refresh: "120Hz",
            ram: "16GB",
            storage: "512GB",
            camera: "50MP Quad Leica + 32MP Front",
            battery: "5000mAh / 90W",
            processor: "Snapdragon 8 Gen 3",
            network: "5G Support",
        },
        tags: ["Leica Camera"],
    },
    {
        id: 4,
        name: "Oppo Reno 11 Pro",
        brand: "Oppo",
        price: 115000,
        image: "https://v-center.dz/5450-large_default/oppo-reno-11-pro-5g-12gb-256gb.jpg",
        rating: 4.5,
        specs: {
            screen: "6.7\" AMOLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "256GB",
            camera: "50MP Triple + 32MP Front",
            battery: "4600mAh / 80W",
            processor: "Dimensity 8200",
            network: "5G Support",
        },
    },
    {
        id: 5,
        name: "Google Pixel 8 Pro",
        brand: "Google Pixel",
        price: 195000,
        image: "https://v-center.dz/5100-large_default/google-pixel-8-pro-12gb-128gb.jpg",
        rating: 4.7,
        specs: {
            screen: "6.7\" LTPO OLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "128GB",
            camera: "50MP Triple + 10.5MP Front",
            battery: "5050mAh / 30W",
            processor: "Google Tensor G3",
            network: "5G Support",
        },
    },
    {
        id: 6,
        name: "Realme 12 Pro+",
        brand: "Realme",
        price: 98000,
        image: "https://v-center.dz/5600-large_default/realme-12-pro-plus-5g.jpg",
        rating: 4.4,
        specs: {
            screen: "6.7\" AMOLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "512GB",
            camera: "50MP + 64MP Periscope",
            battery: "5000mAh / 67W",
            processor: "Snapdragon 7s Gen 2",
            network: "5G Support",
        },
    },
    {
        id: 7,
        name: "Samsung Galaxy A55",
        brand: "Samsung",
        price: 82000,
        image: "https://v-center.dz/5650-large_default/samsung-galaxy-a55-5g-8gb-256gb.jpg",
        rating: 4.6,
        specs: {
            screen: "6.6\" Super AMOLED",
            refresh: "120Hz",
            ram: "8GB",
            storage: "256GB",
            camera: "50MP Triple + 32MP Front",
            battery: "5000mAh / 25W",
            processor: "Exynos 1480",
            network: "5G Support",
        },
    },
    {
        id: 8,
        name: "Nothing Phone (2)",
        brand: "Nothing",
        price: 135000,
        image: "https://v-center.dz/4800-large_default/nothing-phone-2-12gb-256gb.jpg",
        rating: 4.8,
        specs: {
            screen: "6.7\" LTPO OLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "256GB",
            camera: "50MP Dual + 32MP Front",
            battery: "4700mAh / 45W",
            processor: "Snapdragon 8+ Gen 1",
            network: "5G Support",
        },
        tags: ["Unique Design"],
    },
    {
        id: 9,
        name: "Huawei P60 Pro",
        brand: "Huawei",
        price: 210000,
        image: "https://v-center.dz/4500-large_default/huawei-p60-pro-8gb-256gb.jpg",
        rating: 4.7,
        specs: {
            screen: "6.67\" LTPO OLED",
            refresh: "120Hz",
            ram: "8GB",
            storage: "256GB",
            camera: "48MP Triple XMAGE",
            battery: "4815mAh / 88W",
            processor: "Snapdragon 8+ Gen 1",
            network: "4G Support",
        },
    },
    {
        id: 10,
        name: "Redmi Note 13 Pro+",
        brand: "Xiaomi",
        price: 88000,
        image: "https://v-center.dz/5300-large_default/xiaomi-redmi-note-13-pro-plus-5g.jpg",
        rating: 4.5,
        specs: {
            screen: "6.67\" AMOLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "512GB",
            camera: "200MP Triple + 16MP Front",
            battery: "5000mAh / 120W",
            processor: "Dimensity 7200 Ultra",
            network: "5G Support",
        },
    },
    {
        id: 11,
        name: "OnePlus 12",
        brand: "OnePlus",
        price: 225000,
        image: "https://v-center.dz/5400-large_default/oneplus-12-5g-16gb-512gb.jpg",
        rating: 4.9,
        specs: {
            screen: "6.82\" LTPO4 AMOLED",
            refresh: "120Hz",
            ram: "16GB",
            storage: "512GB",
            camera: "50MP Hasselblad + 32MP Front",
            battery: "5400mAh / 100W",
            processor: "Snapdragon 8 Gen 3",
            network: "5G Support",
        },
    },
    {
        id: 12,
        name: "Vivo V30 Pro",
        brand: "Vivo",
        price: 145000,
        image: "https://v-center.dz/5800-large_default/vivo-v30-pro-5g.jpg",
        rating: 4.6,
        specs: {
            screen: "6.78\" AMOLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "512GB",
            camera: "50MP Triple ZEISS + 50MP Front",
            battery: "5000mAh / 80W",
            processor: "Dimensity 8200",
            network: "5G Support",
        },
    },
    {
        id: 13,
        name: "Oppo Reno 12 Pro",
        brand: "Oppo",
        price: 125000,
        image: "https://v-center.dz/5900-large_default/oppo-reno-12-pro-5g.jpg",
        rating: 4.7,
        specs: {
            screen: "6.7\" AMOLED",
            refresh: "120Hz",
            ram: "12GB",
            storage: "512GB",
            camera: "50MP Triple + 50MP Front",
            battery: "5000mAh / 80W",
            processor: "Dimensity 7300-Energy",
            network: "5G Support",
        },
    },
    {
        id: 14,
        name: "Samsung Galaxy A35",
        brand: "Samsung",
        price: 68000,
        image: "https://v-center.dz/5680-large_default/samsung-galaxy-a35-5g-8gb-128gb.jpg",
        rating: 4.3,
        specs: {
            screen: "6.6\" Super AMOLED",
            refresh: "120Hz",
            ram: "8GB",
            storage: "128GB",
            camera: "50MP Triple + 13MP Front",
            battery: "5000mAh / 25W",
            processor: "Exynos 1380",
            network: "5G Support",
        },
    },
    {
        id: 15,
        name: "Redmi Note 13",
        brand: "Xiaomi",
        price: 45000,
        image: "https://v-center.dz/5250-large_default/xiaomi-redmi-note-13-8gb-256gb.jpg",
        rating: 4.2,
        specs: {
            screen: "6.67\" AMOLED",
            refresh: "120Hz",
            ram: "8GB",
            storage: "256GB",
            camera: "108MP Triple + 16MP Front",
            battery: "5000mAh / 33W",
            processor: "Snapdragon 685",
            network: "4G Support",
        },
    },
];

const brands = ["Apple", "Samsung", "Xiaomi", "Oppo", "Vivo", "OnePlus", "Google Pixel", "Realme", "Nothing", "Huawei"];

// Initialize Page
document.addEventListener('DOMContentLoaded', () => {
    renderBrands();
    renderProducts(products);
    populateCalculator();
    
    // Event Listeners
    document.getElementById('mainSearch').addEventListener('input', handleSearch);
    document.getElementById('priceRange').addEventListener('input', handleFilters);
    document.getElementById('sortSelect').addEventListener('change', handleSort);
    document.querySelectorAll('.screen-filter, .refresh-filter, .ram-filter').forEach(el => {
        el.addEventListener('change', handleFilters);
    });

    // Calculator Listeners
    document.getElementById('calcPhone').addEventListener('change', calculateInstallment);
    document.getElementById('calcPlan').addEventListener('change', calculateInstallment);
});

function renderBrands() {
    const container = document.getElementById('brandFilters');
    if (!container) return;
    brands.forEach(brand => {
        const label = document.createElement('label');
        label.innerHTML = `<input type=\"checkbox\" class=\"brand-filter\" value=\"${brand}\"> ${brand}`;
        label.querySelector('input').addEventListener('change', handleFilters);
        container.appendChild(label);
    });
}

function renderProducts(data) {
    const grid = document.getElementById('productsGrid');
    const count = document.getElementById('resultsCount');
    if (!grid) return;
    grid.innerHTML = '';
    count.innerText = `عرض ${data.length} هاتف`;

    data.forEach(p => {
        const card = document.createElement('div');
        card.className = 'product-card animate-fade';
        
        const installment12 = Math.round((p.price * 1.45) / 12);

        card.innerHTML = `
            ${p.tags ? `<span class=\"product-badge\">${p.tags[0]}</span>` : ''}
            <img src="${p.image}" alt="${p.name}" class="product-image">
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
                    <span><i class="fas fa-battery-full"></i> ${p.specs.battery.split(' / ')[0]}</span>
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
    document.getElementById('priceMax').innerText = parseInt(maxPrice).toLocaleString();

    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked')).map(el => el.value);
    const selectedScreens = Array.from(document.querySelectorAll('.screen-filter:checked')).map(el => el.value);
    const selectedRefresh = Array.from(document.querySelectorAll('.refresh-filter:checked')).map(el => el.value);
    const selectedRam = Array.from(document.querySelectorAll('.ram-filter:checked')).map(el => el.value);

    const filtered = products.filter(p => {
        const matchesSearch = p.name.toLowerCase().includes(searchQuery) || 
                              p.brand.toLowerCase().includes(searchQuery) ||
                              p.specs.screen.toLowerCase().includes(searchQuery) ||
                              p.specs.refresh.toLowerCase().includes(searchQuery);
        const matchesPrice = p.price <= maxPrice;
        const matchesBrand = selectedBrands.length === 0 || selectedBrands.includes(p.brand);
        const matchesScreen = selectedScreens.length === 0 || selectedScreens.some(s => p.specs.screen.includes(s));
        const matchesRefresh = selectedRefresh.length === 0 || selectedRefresh.some(r => p.specs.refresh.includes(r));
        const matchesRam = selectedRam.length === 0 || selectedRam.some(ram => p.specs.ram.includes(ram));

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
    const sortType = document.getElementById('sortSelect').value;
    let sorted = [...products];

    switch(sortType) {
        case 'priceLow': sorted.sort((a,b) => a.price - b.price); break;
        case 'priceHigh': sorted.sort((a,b) => b.price - a.price); break;
        case 'refresh': sorted.sort((a,b) => parseInt(b.specs.refresh) - parseInt(a.specs.refresh)); break;
        default: sorted.sort((a,b) => b.id - a.id);
    }
    renderProducts(sorted);
}

function openModal(id) {
    const p = products.find(prod => prod.id === id);
    if (!p) return;

    document.getElementById('modalGallery').innerHTML = `<img src="${p.image}" alt="${p.name}">`;
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
    if (!phoneSelect || !planSelect) return;

    const price = parseFloat(phoneSelect.value);
    const multiplier = parseFloat(planSelect.value);
    let months = 1;
    
    if (multiplier === 1.25) months = 6;
    else if (multiplier === 1.35) months = 8;
    else if (multiplier === 1.45) months = 12;

    const monthly = Math.round((price * multiplier) / months);
    document.getElementById('calcResult').innerText = `${monthly.toLocaleString()} DZD / شهر`;
}

function buyNow(id) {
    openModal(id);
}

function requestOnWhatsapp() {
    const phoneSelect = document.getElementById('calcPhone');
    const planSelect = document.getElementById('calcPlan');
    const phoneName = phoneSelect.options[phoneSelect.selectedIndex].text;
    const planName = planSelect.options[planSelect.selectedIndex].text;
    const result = document.getElementById('calcResult').innerText;
    
    const msg = encodeURIComponent(`مرحباً، أود طلب تقسيط ${phoneName} باستخدام خطة ${planName}. القسط المقدر: ${result}`);
    window.open(`https://wa.me/213540203685?text=${msg}`, '_blank');
}

function scrollToElement(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
}

window.onclick = function(event) {
    if (event.target == document.getElementById('productModal')) {
        closeModal();
    }
}
