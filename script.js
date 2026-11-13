'use strict';

const site = JSON.parse(document.getElementById('site-data').textContent);
const products = new Map(site.products.map(product => [product.id, product]));
const bulkMinimumKg = site.bulkMinimumKg;
const storageKey = 'hamza-ocean-cart-v1';
const itemDialog = document.getElementById('item-dialog');
const itemForm = document.getElementById('item-form');
const cartDialog = document.getElementById('cart-dialog');
const checkout = document.getElementById('checkout-form');
const cartItems = document.getElementById('cart-items');
const whatsappParts = document.getElementById('whatsapp-parts');
const toast = document.getElementById('toast');

let cart = readCart();
let activeProduct = null;
let editingIndex = null;
let toastTimer;
let returnFocusTo;

function validQuantity(value) {
  return Number.isFinite(value) && value >= 0.5 && value <= 1000 && Number.isInteger(value * 2);
}

function readCart() {
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
    if (!Array.isArray(saved)) return [];
    return saved.filter(item => {
      const product = item && products.get(item.id);
      return product && validQuantity(item.quantity) && product.cuts.includes(item.cut) && typeof item.note === 'string';
    }).map(item => ({ ...item, note: item.note.slice(0, 120) }));
  } catch {
    return [];
  }
}

function saveCart() {
  try {
    localStorage.setItem(storageKey, JSON.stringify(cart));
  } catch {
    // The cart remains available on this page if storage is disabled.
  }
  renderCart();
}

function measure(eventName, params, metaEvent, metaParams = {}) {
  if (typeof window.gtag === 'function') window.gtag('event', eventName, params);
  if (metaEvent && typeof window.fbq === 'function') window.fbq('track', metaEvent, metaParams);
}

function initMetaPixel() {
  if (location.origin !== site.liveOrigin || !/^\d{8,25}$/.test(site.metaPixelId) || window.fbq) return;
  function pixel() {
    if (pixel.callMethod) pixel.callMethod.apply(pixel, arguments);
    else pixel.queue.push(arguments);
  }
  pixel.push = pixel;
  pixel.loaded = true;
  pixel.version = '2.0';
  pixel.queue = [];
  window.fbq = pixel;
  window._fbq = pixel;
  const script = document.createElement('script');
  script.src = 'https://connect.facebook.net/en_US/fbevents.js';
  script.async = true;
  document.head.append(script);
  pixel('init', site.metaPixelId);
  pixel('track', 'PageView');
}

function whatsappUrl(lines) {
  return 'https://wa.me/' + site.whatsapp + '?text=' + encodeURIComponent(lines.join('\n'));
}

function compact(value) {
  return String(value || '').trim().replace(/\s+/g, ' ');
}

function openWhatsApp(lines) {
  window.open(whatsappUrl(lines), '_blank', 'noopener,noreferrer');
}

function requiredText(input) {
  input.setCustomValidity(compact(input.value) ? '' : 'Please fill in this field.');
  return input.reportValidity();
}

function tell(message) {
  clearTimeout(toastTimer);
  toast.textContent = message;
  toastTimer = setTimeout(() => { toast.textContent = ''; }, 3500);
}

function showItem(product, index = null) {
  const item = index === null ? null : cart[index];
  activeProduct = product;
  editingIndex = index;
  document.getElementById('item-title').textContent = product.label;
  document.getElementById('item-description').textContent = 'Choose a quantity and your preferred cut.';
  const select = itemForm.elements.cut;
  select.replaceChildren(...product.cuts.map(cut => new Option(cut, cut)));
  select.value = item?.cut ?? product.cuts[0];
  itemForm.elements.quantity.value = item?.quantity ?? 1;
  itemForm.elements.note.value = item?.note ?? '';
  document.getElementById('item-submit').textContent = item ? 'Save changes' : 'Add to cart';
  itemDialog.showModal();
}

function makeLineAction(label, attribute, index, productLabel) {
  const button = document.createElement('button');
  button.type = 'button';
  button.textContent = label;
  button.setAttribute(attribute, index);
  button.setAttribute('aria-label', label + ' ' + productLabel);
  return button;
}

function renderCart() {
  const total = cart.reduce((weight, item) => weight + item.quantity, 0);
  document.querySelectorAll('[data-cart-count]').forEach(counter => { counter.textContent = cart.length; });
  document.getElementById('cart-weight').textContent = total + ' kg';
  document.getElementById('bulk-note').hidden = total < bulkMinimumKg;
  whatsappParts.replaceChildren();
  checkout.hidden = cart.length === 0;
  cartItems.replaceChildren();
  if (!cart.length) {
    const empty = document.createElement('p');
    empty.className = 'help';
    empty.textContent = 'Your cart is empty. Add seafood from the catalogue to get started.';
    cartItems.append(empty);
  }
  cart.forEach((item, index) => {
    const product = products.get(item.id);
    const row = document.createElement('div');
    row.className = 'cart-line';
    const details = document.createElement('div');
    const name = document.createElement('strong');
    name.textContent = product.label;
    const description = document.createElement('p');
    description.textContent = item.quantity + ' kg · ' + item.cut + (item.note ? '\n' + item.note : '');
    details.append(name, description);
    const actions = document.createElement('div');
    actions.className = 'line-actions';
    actions.append(makeLineAction('Edit', 'data-edit', index, product.label), makeLineAction('Remove', 'data-remove', index, product.label));
    row.append(details, actions);
    cartItems.append(row);
  });
}

itemForm.addEventListener('submit', event => {
  event.preventDefault();
  const quantity = itemForm.elements.quantity.valueAsNumber;
  if (!activeProduct || !validQuantity(quantity)) return;
  const line = {
    id: activeProduct.id,
    quantity,
    cut: itemForm.elements.cut.value,
    note: compact(itemForm.elements.note.value),
  };
  const isEdit = editingIndex !== null;
  if (isEdit) {
    cart[editingIndex] = line;
  } else {
    const matching = cart.find(item => item.id === line.id && item.cut === line.cut && item.note === line.note);
    if (matching && validQuantity(matching.quantity + line.quantity)) matching.quantity += line.quantity;
    else cart.push(line);
    measure('add_to_cart', { items: [{ item_id: line.id, item_name: activeProduct.label, quantity }] }, 'AddToCart', {
      content_ids: [line.id], content_type: 'product', contents: [{ id: line.id, quantity }],
    });
  }
  saveCart();
  itemDialog.close();
  if (!isEdit) tell(activeProduct.label + ' added to your cart.');
});

itemDialog.addEventListener('close', () => {
  if (editingIndex === null) {
    returnFocusTo?.focus();
    return;
  }
  if (!cartDialog.open) cartDialog.showModal();
  cartItems.querySelector('[data-edit="' + editingIndex + '"]')?.focus();
  editingIndex = null;
});

cartDialog.addEventListener('close', () => {
  if (!itemDialog.open) returnFocusTo?.focus();
});

checkout.elements.city.addEventListener('input', () => whatsappParts.replaceChildren());
checkout.addEventListener('submit', event => {
  event.preventDefault();
  const city = checkout.elements.city;
  if (!cart.length || !requiredText(city)) return;
  const total = cart.reduce((sum, line) => sum + line.quantity, 0);
  const lines = ['Hi Hamza Ocean Seafood! I’d like to request this order:', '', 'Delivery city: ' + compact(city.value)];
  const itemLines = cart.map(line => {
    const product = products.get(line.id);
    return '• ' + product.label + ' — ' + line.quantity + ' kg, ' + line.cut + (line.note ? ' (' + line.note + ')' : '');
  });
  const tail = ['', 'Requested weight: ' + total + ' kg'];
  if (total >= bulkMinimumKg) tail.push('Please include the bulk discount in the quote.');
  tail.push('Please confirm availability, preparation, price and delivery. Thank you!');
  const batches = [];
  let current = [];
  for (const line of itemLines) {
    if (current.length && whatsappUrl([...lines, '', ...current, line, ...tail]).length > 3500) {
      batches.push(current);
      current = [];
    }
    current.push(line);
  }
  batches.push(current);
  const eventParams = {
    item_count: cart.length,
    quantity: total + ' kg',
    product_name: cart.length === 1 ? products.get(cart[0].id).label : 'Mixed seafood cart',
    bulk_eligible: total >= bulkMinimumKg,
  };
  whatsappParts.replaceChildren();
  if (batches.length === 1) {
    openWhatsApp([...lines, '', ...batches[0], ...tail]);
    measure('whatsapp_order_click', eventParams, 'Contact', { source: 'retail_cart' });
  } else {
    const description = document.createElement('p');
    description.textContent = 'Your cart needs ' + batches.length + ' WhatsApp messages. Open and send each part.';
    whatsappParts.append(description);
    batches.forEach((batch, index) => {
      const link = document.createElement('a');
      link.className = 'button button-secondary';
      link.href = whatsappUrl([...lines, 'Order part ' + (index + 1) + ' of ' + batches.length, '', ...batch, ...tail]);
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.textContent = 'Open part ' + (index + 1);
      link.dataset.contact = 'retail_cart_part';
      link.addEventListener('click', () => {
        if (index === 0) measure('whatsapp_order_click', eventParams, 'Contact', { source: 'retail_cart' });
      });
      whatsappParts.append(link);
    });
    whatsappParts.querySelector('a').focus();
  }
});

const wholesale = document.getElementById('wholesale-form');
wholesale?.elements.weight.addEventListener('input', () => {
  const weight = wholesale.elements.weight;
  document.getElementById('quote-bulk-note').hidden = !weight.validity.valid || weight.valueAsNumber < bulkMinimumKg;
});
wholesale?.addEventListener('submit', event => {
  event.preventDefault();
  const fields = wholesale.elements;
  if (![fields.business, fields.city, fields.seafood].every(requiredText)) return;
  const weight = fields.weight.valueAsNumber;
  const lines = [
    'Hi Hamza Ocean Seafood! I’d like a wholesale quote.',
    '',
    'Business: ' + compact(fields.business.value),
    'Delivery city: ' + compact(fields.city.value),
    'Seafood, cuts and grades: ' + compact(fields.seafood.value),
    'Estimated total: ' + weight + ' kg',
    'Frequency: ' + fields.frequency.value,
  ];
  if (fields.date.value) lines.push('Required by: ' + fields.date.value);
  if (weight >= bulkMinimumKg) lines.push('Please include your bulk discount for this order.');
  lines.push('', 'Please confirm availability, rates and delivery. Thank you!');
  openWhatsApp(lines);
  measure('wholesale_whatsapp_click', { quantity_kg: weight, bulk_eligible: weight >= bulkMinimumKg }, 'Contact', { source: 'wholesale_quote' });
});

document.querySelectorAll('form input, form textarea').forEach(input => {
  input.addEventListener('input', () => input.setCustomValidity(''));
});

document.addEventListener('click', event => {
  const closeButton = event.target.closest('[data-close]');
  if (closeButton) closeButton.closest('dialog').close();

  const add = event.target.closest('[data-add]');
  if (add) {
    returnFocusTo = add;
    const product = products.get(add.dataset.add);
    if (product) showItem(product);
  }

  const cartButton = event.target.closest('[data-show-cart]');
  if (cartButton) {
    returnFocusTo = cartButton;
    cartDialog.showModal();
  }

  const edit = event.target.closest('[data-edit]');
  if (edit) {
    const index = Number(edit.dataset.edit);
    const line = cart[index];
    if (line) {
      cartDialog.close();
      showItem(products.get(line.id), index);
    }
  }

  const remove = event.target.closest('[data-remove]');
  if (remove) {
    const index = Number(remove.dataset.remove);
    const line = cart[index];
    if (line) {
      cart.splice(index, 1);
      saveCart();
      cartItems.querySelector('[data-remove="' + Math.min(index, cart.length - 1) + '"]')?.focus();
      if (!cart.length) cartDialog.querySelector('[data-close]').focus();
    }
  }

  const contact = event.target.closest('a[href^="https://wa.me/"]');
  if (contact && contact.dataset.contact !== 'retail_cart_part') {
    const source = contact.dataset.contact || 'general';
    measure('whatsapp_contact_click', { source }, 'Contact', { source });
  }
});

const menu = document.querySelector('.menu-toggle');
const nav = document.getElementById('main-nav');
function setMenu(open) {
  menu.setAttribute('aria-expanded', String(open));
  nav.classList.toggle('is-open', open);
}
menu.addEventListener('click', () => setMenu(menu.getAttribute('aria-expanded') !== 'true'));
nav.addEventListener('click', event => {
  if (event.target.closest('a')) setMenu(false);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
    setMenu(false);
    menu.focus();
  }
});

const search = document.getElementById('catalogue-search');
if (search) {
  const filters = [...document.querySelectorAll('[data-filter]')];
  const cards = [...document.querySelectorAll('#catalogue-grid .product-card')];
  const results = document.getElementById('results-count');
  const empty = document.getElementById('empty-results');
  let category = 'All';
  function applyFilters() {
    const query = compact(search.value).toLowerCase();
    let count = 0;
    for (const card of cards) {
      const matches = (category === 'All' || category === card.dataset.category) &&
        query.split(' ').every(term => card.dataset.search.includes(term));
      card.hidden = !matches;
      if (matches) count++;
    }
    results.textContent = count + (count === 1 ? ' product' : ' products');
    empty.hidden = count > 0;
    for (const button of filters) button.setAttribute('aria-pressed', String(button.dataset.filter === category));
  }
  for (const button of filters) {
    button.addEventListener('click', () => {
      category = button.dataset.filter;
      applyFilters();
    });
  }
  search.addEventListener('input', applyFilters);
  document.getElementById('reset-filters').addEventListener('click', () => {
    category = 'All';
    search.value = '';
    applyFilters();
    search.focus();
  });
}

window.addEventListener('storage', event => {
  if (event.key === storageKey || event.key === null) {
    if (itemDialog.open) itemDialog.close();
    cart = readCart();
    renderCart();
  }
});

document.querySelector('[data-year]').textContent = new Date().getFullYear();
renderCart();
initMetaPixel();
