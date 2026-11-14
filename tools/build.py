"""Build the four static GitHub Pages entry points from catalogue.json."""
from html import escape
import json
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'catalogue.json').read_text(encoding='utf-8'))
CONFIG = DATA['business']
PRODUCTS = DATA['products']
HOME = 'https://rehanreo.github.io/HamzaOceanSeafood/'
BRAND = 'Hamza Ocean Seafood'
WHATSAPP = 'https://wa.me/' + CONFIG['whatsapp']
SECONDARY_WHATSAPP = 'https://wa.me/' + CONFIG['secondaryWhatsapp']
BULK_MINIMUM = CONFIG['bulkMinimumKg']
TEMPLATES = ROOT / 'tools' / 'templates'
CUTS = {
    'ask': ['Confirm with us'],
    'whole': ['Whole cleaned', 'Confirm with us'],
    'large': ['Whole cleaned', 'Bone-in steaks', 'Boneless fillets', 'Curry cut', 'Confirm with us'],
    'prawns': ['Whole', 'Peeled & deveined', 'Confirm with us'],
}
CUT_GUIDE = [
    ('whole', 'Whole cleaned', 'Scaled and gutted, with the fish left whole. Ask about keeping the head or tail.', 'Whole roast, grill or fry'),
    ('steaks', 'Bone-in steaks', 'Crosswise slices with the centre bone in. Request a thickness for consistent portions.', 'Pan-fry or grill'),
    ('fillet', 'Boneless fillets', 'Flesh cut away from the backbone and trimmed. Ask about skin-on or skin-off.', 'Pan-sear or portion for service'),
    ('curry', 'Curry cut', 'Smaller pieces cut for cooking in sauce. Confirm bone-in or boneless when ordering.', 'Curry or stew'),
    ('prawns', 'Peeled & deveined', 'Shell and vein removed. Ask about keeping the tail on.', 'Biryani, stir-fry or pasta'),
]


def display_number(number):
    return f'+{number[:2]} {number[2:5]} {number[5:]}'


def safe_json(data):
    return json.dumps(data, ensure_ascii=False).replace('<', '\\u003c')


def icon(which):
    paths = {
        'bag': '<path d="M5 8h14l1 13H4L5 8Z"/><path d="M9 10V6a3 3 0 0 1 6 0v4"/>',
        'arrow': '<path d="M4 12h15m-6-6 6 6-6 6"/>',
        'fish': '<path d="M3 12c4-5 9-8 15-3l3-2v10l-3-2C12 20 7 17 3 12Z"/><path d="M8 12h.01"/>',
        'menu': '<path d="M3 6h18M3 12h18M3 18h18"/>',
        'pin': '<path d="M20 10c0 5-8 11-8 11S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    }
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths[which]}</svg>'


def button(url, label, classes='btn btn-primary'):
    return f'<a class="{classes}" href="{escape(url, quote=True)}">{escape(label)} {icon("arrow")}</a>'


def message_link(message):
    return f'{WHATSAPP}?text={quote(message)}'


def layout(path, title, description, body, *, schema=None):
    prefix = '../' if path else './'
    url = HOME + path
    ga = escape(CONFIG['analyticsId'])
    homepage_url = urlsplit(HOME)
    live_origin = f'{homepage_url.scheme}://{homepage_url.netloc}'
    org = {
        '@context': 'https://schema.org', '@type': 'OnlineStore', 'name': BRAND,
        'url': HOME, 'logo': HOME + 'assets/images/Logo.png',
        'image': HOME + 'assets/catalogue/social-preview.jpg',
        'email': CONFIG['email'], 'telephone': '+' + CONFIG['whatsapp'],
        'areaServed': {'@type':'Country', 'name':'Pakistan'},
        'sameAs': ['https://www.instagram.com/hamzaoceanseafood', 'https://www.tiktok.com/@hamzaoceanseafood',
                   'https://www.linkedin.com/company/hamza-ocean-seafood/'],
    }
    data = {'whatsapp': CONFIG['whatsapp'], 'metaPixelId': CONFIG['metaPixelId'], 'bulkMinimumKg': BULK_MINIMUM, 'liveOrigin': live_origin, 'products': [
        {'id': p['id'], 'label': p['name'] + (f' ({p["local"]})' if p['local'] else ''), 'cuts': CUTS[p['cuts']]} for p in PRODUCTS
    ]}
    def localize(markup):
        values = {
            '@root/': prefix,
            '@HOME_PREFIX@': prefix if path else '',
            '@PRIMARY@': WHATSAPP,
            '@SECONDARY@': SECONDARY_WHATSAPP,
            '@PRIMARY_DISPLAY@': display_number(CONFIG['whatsapp']),
            '@SECONDARY_DISPLAY@': display_number(CONFIG['secondaryWhatsapp']),
            '@PRIMARY_TEL@': '+' + CONFIG['whatsapp'],
            '@EMAIL@': CONFIG['email'],
        }
        for token, value in values.items():
            markup = markup.replace(token, escape(value, quote=True))
        if path == 'products/':
            markup = markup.replace('href="../#products"', 'href="#catalogue"')
        return markup

    header = localize((TEMPLATES / 'header.html').read_text(encoding='utf-8'))
    footer = localize((TEMPLATES / 'footer.html').read_text(encoding='utf-8'))
    localized_body = localize(body)
    hero_preload = '<link rel="preload" as="image" href="assets/images/Hero-bg-1.jpg">' if not path else ''

    return f'''<!doctype html>
<html lang="en-PK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0B2942">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title, quote=True)}">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_PK">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{HOME}assets/catalogue/social-preview.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Hamza Ocean Seafood catalogue preview">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}assets/images/favicon.ico">
<link rel="apple-touch-icon" href="{prefix}assets/images/apple-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,500;0,9..144,600;0,9..144,700;1,9..144,400;1,9..144,500&amp;family=Manrope:wght@300;400;500;600;700;800&amp;display=swap">
{hero_preload}
<link rel="stylesheet" href="{prefix}style.css">
<script type="application/ld+json">{safe_json(schema or org)}</script>
<script>
  if (location.origin === {safe_json(live_origin)}) {{
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {{ window.dataLayer.push(arguments); }};
    window.gtag('js', new Date());
    window.gtag('config', '{ga}');
    const tag = document.createElement('script');
    tag.src = 'https://www.googletagmanager.com/gtag/js?id={ga}';
    tag.async = true;
    document.head.append(tag);
  }}
</script>
<script id="site-data" type="application/json">{safe_json(data)}</script>
<script src="{prefix}script.js" defer></script>
</head>
<body class="{"home-page" if not path else "inner-page"}">
<a class="skip-link" href="#main-content">Skip to content</a>
{header}
<main id="main-content">
{localized_body}
</main>
{footer}
<dialog class="dialog item-dialog" id="item-dialog" aria-labelledby="item-title">
  <div class="dialog-heading"><h2 id="item-title">Add seafood</h2><button type="button" class="close-button" data-close aria-label="Close">×</button></div>
  <form id="item-form">
    <p id="item-description" class="muted"></p>
    <label for="item-qty">Quantity (kg)</label>
    <input id="item-qty" name="quantity" type="number" min="0.5" max="1000" step="0.5" inputmode="decimal" required>
    <label for="item-cut">Preferred cut</label><select name="cut" id="item-cut" required></select>
    <label for="item-note">Item notes <span>(optional)</span></label><textarea name="note" id="item-note" rows="2" maxlength="120"></textarea>
    <p class="help">Cut and availability are confirmed on WhatsApp. <a href="{prefix}products/#cutting-guide">See cut options</a>.</p>
    <button type="submit" class="btn btn-primary" id="item-submit">Add to cart</button>
  </form>
</dialog>
<dialog class="dialog cart-dialog" id="cart-dialog" aria-labelledby="cart-title">
  <div class="dialog-heading"><h2 id="cart-title">Your cart</h2><button type="button" class="close-button" data-close aria-label="Close">×</button></div>
  <div id="cart-items"></div>
  <form id="checkout-form" hidden>
    <p class="cart-total">Requested weight <strong id="cart-weight"></strong></p>
    <p id="bulk-note" class="bulk-note" hidden>Your order qualifies for bulk pricing at {BULK_MINIMUM} kg or more. Ask for the discounted rate on WhatsApp.</p>
    <label for="delivery-city">Delivery city</label><input id="delivery-city" name="city" autocomplete="address-level2" maxlength="60" required placeholder="e.g. Karachi or Lahore">
    <p class="help">We’ll confirm today’s rates, availability, cuts and delivery in chat. Send the prefilled message in WhatsApp to request your order.</p>
    <button type="submit" class="btn btn-whatsapp">Continue to WhatsApp {icon('arrow')}</button>
    <div id="whatsapp-parts" class="whatsapp-parts"></div>
  </form>
</dialog>
<div class="toast" role="status" id="toast"></div>
<noscript><p class="noscript">Order or request a quote directly on <a href="{WHATSAPP}">WhatsApp</a>.</p></noscript>
</body>
</html>
'''


def card(product):
    photo = product['image']
    category = escape(product['category'])
    name = escape(product['name'])
    local = f'<p class="local-name">{escape(product["local"])}</p>' if product['local'] else ''
    label = product['name'] + (f' ({product["local"]})' if product['local'] else '')
    cut_label = {'ask': 'Ask about available cuts', 'whole': 'Whole cleaned on request', 'large': 'Whole, steaks or fillets on request', 'prawns': 'Whole or peeled on request'}[product['cuts']]

    credit = ''
    if product.get('photoSource'):
        credit = (f'<p class="photo-credit">{escape(product["photoContext"])} '
                  f'<a href="{escape(product["photoSource"], quote=True)}">{escape(product["photoCredit"])}</a> · '
                  f'<a href="{escape(product["photoLicense"], quote=True)}">CC BY 4.0</a>. '
                  f'{escape(product["photoChanges"])}</p>')
    position = product.get('imagePosition')
    crop = f' style="object-position:{escape(position, quote=True)}"' if position else ''
    alt = escape(product.get('photoContext', product['name']), quote=True)
    img = (f'<img src="@root/assets/catalogue/{escape(photo, quote=True)}" alt="{alt}" width="{product.get("imageWidth", 800)}" height="{product.get("imageHeight", 530)}" loading="lazy" decoding="async"{crop}>'
           if photo else f'<div class="photo-pending">{icon("fish")}<span>Photo on request</span></div>')
    facts = ''
    if product.get('fact'):
        facts = f'<p class="product-fact">{escape(product["fact"])} <a href="{escape(product["source"], quote=True)}" aria-label="Nutrition source for {escape(product["local"] or product["name"], quote=True)}">Source</a></p>'
    return f'''<article class="product-card catalogue-card" data-category="{category}" data-search="{escape(' '.join([product['name'], product['local'], product['category']]).casefold(), quote=True)}">
      <div class="product-image-wrap">{img}</div>
      <div class="product-body"><div><h3 class="product-name">{name}</h3>{local}</div>
        <p class="product-desc">{escape(product['description'])}</p><p class="product-cut">{cut_label}</p>{facts}{credit}
        <button class="btn btn-primary add-button" type="button" data-add="{escape(product['id'])}" aria-label="Add {escape(label, quote=True)} to cart"><span>Add to cart</span><span aria-hidden="true">+</span></button>
      </div>
    </article>'''


def product_cards(ids):
    index = {p['id']: p for p in PRODUCTS}
    return '\n'.join(card(index[ident]) for ident in ids)


def heading(title, subtitle):
    return f'<div class="section-header"><h2 class="section-title">{escape(title)}</h2><p class="section-subtitle">{escape(subtitle)}</p></div>'


featured = f'''
<section class="products" id="products">
  <div class="container">
    <div class="featured-head">
      {heading('Explore the seafood catalogue', 'Choose your seafood, weight and preferred cut. We confirm today’s prices and availability on WhatsApp.')}
      {button('@root/products/', f'View all {len(PRODUCTS)} products')}
    </div>
    <div class="catalogue-grid">{product_cards(['red-snapper', 'indian-salmon', 'white-pomfret', 'tiger-prawns'])}</div>
  </div>
</section>
'''
wholesale_band = f'''
<section class="wholesale-band" id="wholesale">
  <div class="container">
    {heading('Seafood for restaurants, hotels and caterers', f'Ask for a quote for your preferred species, size, cut and delivery city. Bulk discounts apply from {BULK_MINIMUM} kg.')}
    {button('@root/wholesale/', 'Get a wholesale quote')}
  </div>
</section>
'''
homepage = (TEMPLATES/'home.html').read_text(encoding='utf-8').replace('@FEATURED@', featured).replace('@WHOLESALE_BAND@', wholesale_band)

products_page = f'''
<section class="page-intro"><div class="container">
  <h1>Seafood catalogue</h1><p>Choose your seafood, weight and preferred cut. We’ll confirm today’s prices and availability on WhatsApp.</p>
  <div class="actions">{button('#catalogue', 'Browse products')}{button('#cutting-guide', 'See the cutting guide', 'btn btn-outline')}</div>
</div></section>
<section class="container catalogue-section" id="catalogue">
  <div class="catalogue-tools">
    <div class="filter-tabs" aria-label="Filter products">
      <button type="button" data-filter="All" aria-pressed="true">All seafood</button>
      <button type="button" data-filter="Fish" aria-pressed="false">Fish</button>
      <button type="button" data-filter="Small fish" aria-pressed="false">Small fish</button>
      <button type="button" data-filter="Prawns" aria-pressed="false">Prawns</button>
    </div>
    <label class="form-field">Search seafood<input id="catalogue-search" type="search" placeholder="e.g. Pomfret or Paplet" autocomplete="off" maxlength="60"></label>
  </div>
  <p class="result-count" id="results-count" role="status">{len(PRODUCTS)} products</p>
  <div class="catalogue-grid" id="catalogue-grid">{''.join(card(p) for p in PRODUCTS)}</div>
  <div id="empty-results" class="empty-state" hidden><p>No seafood matches your search.</p><button class="btn btn-outline" id="reset-filters" type="button">Clear filters</button></div>
  <div class="catalogue-footer"><div><h2 class="section-title">Looking for another catch?</h2><p>Send us the name and we’ll check what’s available.</p></div>{button(message_link('Hi Hamza Ocean Seafood! Can you check availability for a specific seafood item?'), 'Ask on WhatsApp', 'btn btn-outline')}</div>
</section>
'''

wholesale_page = f'''
<section class="page-intro wholesale-intro"><div class="container">
  <p class="eyebrow">Restaurants, hotels and caterers</p>
  <h1>Wholesale seafood<br>for Punjab kitchens.</h1>
  <p>Share the seafood, grades and cuts you need. We’ll confirm availability, current rates and delivery to your city.</p>
  <p class="offer">Bulk discounts on seafood orders of {BULK_MINIMUM} kg or more.</p>
  <div class="actions">{button('#quote', 'Request a bulk quote', 'btn btn-primary')}{button('@root/products/', 'Browse seafood', 'btn btn-outline')}</div>
</div></section>
<section class="container wholesale-section wholesale-grid" id="quote">
  <div>{heading('Get a wholesale quote', 'Send your requirements directly to our team on WhatsApp.')}
    <div class="wholesale-details"><h3>Seafood quotes for major Punjab cities</h3>
    <p>Request a quote for Lahore, Faisalabad, Rawalpindi, Multan, Gujranwala, Sialkot or another city. We’ll confirm service, timing and delivery charges for your location.</p>
    <h3>One-off orders and recurring supply</h3><p>Tell us your portion sizes, preferred cuts, order frequency and delivery date so we can quote for your kitchen.</p>
    <h3>How the discount works</h3><p>Orders of {BULK_MINIMUM} kg or more qualify for bulk discounts. We confirm the applicable rate with your quote.</p></div>
  </div>
  <form id="wholesale-form" class="quote-form">
    <label for="business">Business name</label><input id="business" name="business" autocomplete="organization" maxlength="80" required>
    <label for="wholesale-city">Delivery city</label><input id="wholesale-city" name="city" autocomplete="address-level2" maxlength="60" required>
    <label for="seafood">Seafood, cut or size grade</label><textarea id="seafood" name="seafood" rows="3" maxlength="400" placeholder="e.g. 15 kg snapper fillets and 10 kg medium prawns" required></textarea>
    <div class="form-row"><div><label for="wholesale-weight">Estimated total (kg)</label><input id="wholesale-weight" name="weight" type="number" min="0.5" max="10000" step="0.5" inputmode="decimal" required></div>
    <div><label for="date">Required by <span>(optional)</span></label><input id="date" name="date" type="date"></div></div>
    <label for="frequency">Order frequency</label><select id="frequency" name="frequency"><option>One-time order</option><option>Weekly supply</option><option>Other recurring supply</option></select>
    <p id="quote-bulk-note" class="bulk-note" hidden>Your order qualifies for a bulk discount.</p>
    <p class="help">WhatsApp opens with your details. Send the prefilled message to request your quote.</p>
    <button class="btn btn-whatsapp" type="submit">Continue to WhatsApp {icon('arrow')}</button>
  </form>
</section>
'''

guide_section = f'''
<section class="guide-section" id="cutting-guide">
  <div class="container">
    {heading('Seafood cutting guide', 'Compare common preparations and choose your preferred cut when adding seafood to your cart.')}
    <div class="guide-grid">
      {''.join(f'<article class="guide-card"><img src="@root/assets/cuts/{key}.svg" alt="Illustration of {escape(name.lower())}" width="560" height="340" loading="lazy"><div><h3>{escape(name)}</h3><p>{escape(desc)}</p><p class="guide-use">{escape(use)}</p></div></article>' for key, name, desc, use in CUT_GUIDE)}
    </div>
    <div class="catalogue-footer">{button('#catalogue', 'Back to products', 'btn btn-outline')}</div>
  </div>
</section>
'''


def main():
    pages = [
        ('', f'Fresh Seafood for Homes & Restaurants | {BRAND}', 'Shop fresh fish and prawns sourced through Karachi Fish Harbour. Choose your cuts, order on WhatsApp or request a bulk quote for your restaurant.', homepage),
        ('products/', f'Fresh Fish & Prawns Catalogue | {BRAND}', 'Browse fresh fish, small fish and prawns. Choose weight and cuts, build your seafood cart and ask for today’s prices on WhatsApp.', products_page + guide_section),
        ('wholesale/', f'Wholesale Seafood Supplier for Punjab Restaurants | {BRAND}', f'Request a wholesale quote for fish and prawns in Lahore and other major Punjab cities. Bulk discounts on orders of {BULK_MINIMUM} kg or more. Ask about cuts, grades and delivery.', wholesale_page),
    ]
    for path, title, description, body in pages:
        folder = ROOT / path
        folder.mkdir(exist_ok=True)
        (folder / 'index.html').write_text(layout(path, title, description, body), encoding='utf-8')
    # Keep links to the old standalone guide working after the sections merge.
    legacy_guide = ROOT / 'cutting-guide'
    legacy_guide.mkdir(exist_ok=True)
    (legacy_guide / 'index.html').write_text(
        f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Seafood cutting guide</title>
<meta http-equiv="refresh" content="0; url=../products/#cutting-guide">
<link rel="canonical" href="{HOME}products/#cutting-guide">
</head><body><a href="../products/#cutting-guide">Open the seafood cutting guide</a></body></html>
''', encoding='utf-8')
    urls = '\n'.join(f'  <url><loc>{HOME}{path}</loc></url>' for path, *_ in pages)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {HOME}sitemap.xml\n', encoding='utf-8')


if __name__ == '__main__':
    main()
