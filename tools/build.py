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
REVIEW = 'https://g.page/r/Cd3XOubzZOcIECE/review'
NAV = [('products/', 'Seafood'), ('wholesale/', 'Wholesale'), ('cutting-guide/', 'Cutting guide')]
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


def button(url, label, classes='button'):
    return f'<a class="{classes}" href="{escape(url, quote=True)}">{escape(label)} {icon("arrow")}</a>'


def message_link(message):
    return f'{WHATSAPP}?text={quote(message)}'


def layout(path, title, description, body, *, schema=None):
    prefix = '../' if path else './'
    url = HOME + path
    nav = ''.join(f'<a href="{prefix}{href}"{" aria-current=\x22page\x22" if href == path else ""}>{label}</a>' for href, label in NAV)
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
    localized_body = body.replace('@root/', prefix)
    return f'''<!doctype html>
<html lang="en-PK">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0B1B3A">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&amp;family=Instrument+Serif:ital@0;1&amp;display=swap">
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
<body>
<a class="skip" href="#main-content">Skip to content</a>
<header class="site-header">
  <div class="shell header-inner">
    <a class="brand" href="{prefix}" aria-label="{BRAND} home">
      <img src="{prefix}assets/images/apple-icon.png" width="44" height="44" alt="">
      <span>Hamza Ocean<small>SEAFOOD</small></span>
    </a>
    <nav class="main-nav" aria-label="Main navigation" id="main-nav">{nav}<a href="{prefix}#about">About</a><a href="#contact">Contact</a></nav>
    <div class="header-actions">
      <button class="cart-button" type="button" data-show-cart>{icon("bag")} <span>Cart</span> <span class="cart-count" data-cart-count>0</span></button>
      <button class="menu-toggle" type="button" aria-label="Menu" aria-controls="main-nav" aria-expanded="false">{icon("menu")}</button>
    </div>
  </div>
</header>
<main id="main-content">
{localized_body}
</main>
<footer class="site-footer" id="contact" aria-label="Contact and site information">
  <div class="shell footer-grid">
    <div><a class="brand" href="{prefix}"><img src="{prefix}assets/images/apple-icon.png" width="44" height="44" alt=""><span>Hamza Ocean<small>SEAFOOD</small></span></a>
      <p>Karachi-sourced seafood for homes, restaurants and catering teams.</p></div>
    <div><h2>Explore</h2>{nav}<a href="{prefix}#faq">FAQs</a></div>
    <div><h2>Contact</h2><a href="{WHATSAPP}" data-contact="footer_primary">{display_number(CONFIG["whatsapp"])} · WhatsApp</a><a href="{SECONDARY_WHATSAPP}" data-contact="footer_secondary">{display_number(CONFIG["secondaryWhatsapp"])} · WhatsApp</a><a href="mailto:{escape(CONFIG['email'])}">{escape(CONFIG['email'])}</a><a href="{REVIEW}">Leave a Google review</a></div>
    <div><h2>Follow</h2><a href="https://www.facebook.com/hamzaoceanseafood">Facebook</a><a href="https://www.instagram.com/hamzaoceanseafood">Instagram</a><a href="https://www.linkedin.com/company/hamza-ocean-seafood/">LinkedIn</a><a href="https://www.tiktok.com/@hamzaoceanseafood">TikTok</a></div>
  </div>
  <div class="shell footer-bottom"><span>© <span data-year>2026</span> {BRAND}</span><span>Karachi, Pakistan · Website by <a href="https://www.facebook.com/share/1GYQCWmWqY/">Reo Digital Studio</a></span></div>
</footer>
<dialog class="dialog item-dialog" id="item-dialog" aria-labelledby="item-title">
  <div class="dialog-heading"><h2 id="item-title">Add seafood</h2><button type="button" class="close-button" data-close aria-label="Close">×</button></div>
  <form id="item-form">
    <p id="item-description" class="muted"></p>
    <label for="item-qty">Quantity (kg)</label>
    <input id="item-qty" name="quantity" type="number" min="0.5" max="1000" step="0.5" inputmode="decimal" required>
    <label for="item-cut">Preferred cut</label><select name="cut" id="item-cut" required></select>
    <label for="item-note">Item notes <span>(optional)</span></label><textarea name="note" id="item-note" rows="2" maxlength="120"></textarea>
    <p class="help">Cut and availability are confirmed on WhatsApp.</p>
    <button type="submit" class="button button-primary" id="item-submit">Add to cart</button>
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
    <button type="submit" class="button button-whatsapp">Continue to WhatsApp {icon('arrow')}</button>
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
    identity = ''
    if product.get('identitySource'):
        identity = f'<p class="photo-credit"><a href="{escape(product["identitySource"], quote=True)}">Fish name reference</a></p>'
    credit = ''
    if product.get('photoSource'):
        credit = (f'<p class="photo-credit">{escape(product["photoContext"])} '
                  f'<a href="{escape(product["photoSource"], quote=True)}">{escape(product["photoCredit"])}</a> · '
                  f'<a href="{escape(product["photoLicense"], quote=True)}">CC BY 4.0</a>. '
                  f'{escape(product["photoChanges"])}</p>')
    img = (f'<img src="@root/assets/catalogue/{escape(photo)}" alt="{name}" width="800" height="530" loading="lazy" decoding="async">'
           if photo else f'<div class="photo-pending">{icon("fish")}<span>Photo on request</span></div>')
    facts = ''
    if product.get('fact'):
        facts = f'<p class="product-fact">{escape(product["fact"])} <a href="{escape(product["source"], quote=True)}" aria-label="Nutrition source for {escape(product["local"] or product["name"], quote=True)}">Source</a></p>'
    return f'''<article class="product-card" data-category="{category}" data-search="{escape(' '.join([product['name'], product['local'], product['category']]).casefold(), quote=True)}">
      <div class="product-photo">{img}</div>
      <div class="product-body"><div><h3>{name}</h3>{local}</div>
        <p class="product-description">{escape(product['description'])}</p><p class="product-cut">{cut_label}</p>{facts}{identity}{credit}
        <button class="add-button" type="button" data-add="{escape(product['id'])}" aria-label="Add {escape(label, quote=True)} to cart"><span>Add to cart</span><span aria-hidden="true">+</span></button>
      </div>
    </article>'''


def product_cards(ids):
    index = {p['id']: p for p in PRODUCTS}
    return '\n'.join(card(index[ident]) for ident in ids)


def heading(title, subtitle, kicker=None):
    label = f'<p class="eyebrow">{escape(kicker)}</p>' if kicker else ''
    return f'<div class="section-head">{label}<h2>{escape(title)}</h2><p>{escape(subtitle)}</p></div>'


def faq(question, answer):
    return f'<details><summary>{escape(question)} <span aria-hidden="true">+</span></summary><p>{escape(answer)}</p></details>'


homepage = f'''
<section class="hero" id="home">
  <div class="shell hero-grid">
    <div class="hero-copy">
      <p class="eyebrow">Sourced through Karachi Fish Harbour</p>
      <h1>Fresh seafood<br>for homes<br><em>and restaurants.</em></h1>
      <p class="hero-intro">Browse fish and prawns, choose your cuts, and send your order on WhatsApp. For restaurant supply and bulk requests, get a tailored quote.</p>
      <div class="actions">{button('@root/products/', 'Shop seafood', 'button button-gold')}{button('@root/wholesale/', 'Get a wholesale quote','button button-outline')}</div>
    </div>
    <div class="hero-photo"><img src="@root/assets/catalogue/hero.webp" alt="Fresh red snapper arranged on a white tray" width="1000" height="850" fetchpriority="high"></div>
  </div>
</section>
<div class="benefit-bar"><div class="shell benefit-inner"><span>{icon('pin')} Karachi Fish Harbour sourcing</span><span>{icon('fish')} Cleaning and custom cuts</span><span>{icon('bag')} WhatsApp orders and quotes</span></div></div>
<section class="section shell" id="products">
  <div class="section-split">{heading('Explore the seafood catalogue', 'Choose your seafood and check current availability.')} {button('@root/products/', 'View all seafood', 'button button-secondary')}</div>
  <div class="product-grid">{product_cards(['red-snapper', 'white-pomfret', 'tiger-prawns', 'grouper'])}</div>
</section>
<section class="section wholesale-band" id="wholesale">
  <div class="shell band-grid">
    <div>{heading('Seafood for busy kitchens', 'Request a quote for your preferred species, size, cut and delivery city.', 'Restaurants, hotels and caterers')}
    <p class="offer">Bulk discounts on seafood orders of {BULK_MINIMUM} kg or more.</p>
    {button('@root/wholesale/', 'Get a wholesale quote', 'button button-gold')}</div>
    <div class="trade-points"><div><h3>Order to your specifications</h3><p>Share preferred grades, portion sizes, cuts and weekly needs.</p></div>
    <div><h3>Plan your next delivery</h3><p>Ask about current supply and dispatch options for your city.</p></div></div>
  </div>
</section>
<section class="section shell guide-teaser" id="cutting-guide">
  <img src="@root/assets/cuts/steaks.webp" alt="Fish steaks with the centre bone" width="800" height="530" loading="lazy">
  <div>{heading('Choose your cut', 'From whole cleaned fish to steaks and fillets, see what each preparation looks like.')}
  {button('@root/cutting-guide/', 'View the cutting guide', 'button button-secondary')}</div>
</section>
<section class="section process-section" id="process"><div class="shell">
  {heading('From the harbour to your kitchen', 'Tell us what you need and we’ll confirm the details in chat.')}
  <ol class="steps">
    <li><h3>Choose your seafood</h3><p>Add fish or prawns, quantities and cut preferences to your cart.</p></li>
    <li><h3>Confirm on WhatsApp</h3><p>We check the catch, quote today’s rate and confirm delivery to your city.</p></li>
    <li><h3>Prepare and dispatch</h3><p>We clean and cut your seafood as agreed and pack it for your delivery route.</p></li>
  </ol>
</div></section>
<section class="section shell about" id="about">
  <div>{heading('About Hamza Ocean Seafood', 'We source seafood through Karachi Fish Harbour for households and business kitchens.')}
  <p>Looking for a specific fish or cut? Tell us what you need and we’ll check the catch.</p>
  {button(message_link('Hi Hamza Ocean Seafood! I’m looking for a specific seafood item.'), 'Ask about availability', 'button button-secondary')}</div>
  <div class="about-media"><img src="@root/assets/images/About-2.jpg" alt="Fresh seafood sourcing" width="1000" height="1500" loading="lazy"><details><summary>Watch our process video <span aria-hidden="true">+</span></summary><a href="https://vimeo.com/1223723417">Open the sourcing and preparation video on Vimeo</a></details></div>
</section>
<section class="section faq-section" id="faq"><div class="shell faq-layout">
  {heading('Ordering FAQs', 'Find out how quotes, cleaning and delivery work.')}
  <div class="faq-list">
    {faq('How do I place an order?', 'Add your seafood to the cart, enter your city and continue to WhatsApp. Send the prepared message and we will confirm your order details.')}
    {faq('How do I find today’s prices?', 'Rates depend on the catch, grade, preparation and delivery. Send your selection on WhatsApp for a current quote.')}
    {faq('Can I order outside Karachi?', 'Send your city and required date so we can confirm available routes, packing, timing and charges.')}
    {faq('Which payment methods are available?', 'Ask about advance payment and cash on delivery. COD availability depends on your city and order.')}
    {faq('Can I choose how my fish is cut?', 'Yes. Request a cut from the catalogue and we’ll confirm what is available for the fish and size you select. Ask how the quote is calculated before confirming.')}
    {faq('What if I have a problem with my order?', 'Message us on WhatsApp within 24 hours of delivery with your order details so we can help.')}
  </div>
</div></section>
'''

products_page = f'''
<section class="page-intro"><div class="shell">
  <h1>Seafood catalogue</h1><p>Choose your seafood, weight and preferred cut. We’ll confirm today’s prices and availability on WhatsApp.</p>
</div></section>
<section class="section shell catalogue-section">
  <div class="catalogue-tools">
    <div class="filter-tabs" aria-label="Filter products">
      <button type="button" data-filter="All" aria-pressed="true">All seafood</button>
      <button type="button" data-filter="Fish" aria-pressed="false">Fish</button>
      <button type="button" data-filter="Small fish" aria-pressed="false">Small fish</button>
      <button type="button" data-filter="Prawns" aria-pressed="false">Prawns</button>
    </div>
    <label class="search-label">Search seafood<input id="catalogue-search" type="search" placeholder="e.g. Pomfret or Paplet" autocomplete="off" maxlength="60"></label>
  </div>
  <p class="result-count" id="results-count" role="status">{len(PRODUCTS)} products</p>
  <div class="product-grid" id="catalogue-grid">{''.join(card(p) for p in PRODUCTS)}</div>
  <div id="empty-results" class="empty-state" hidden><p>No seafood matches your search.</p><button class="button button-secondary" id="reset-filters" type="button">Clear filters</button></div>
  <div class="catalogue-footer"><div><h2>Looking for another catch?</h2><p>Send us the name and we’ll check what’s available.</p></div>{button(message_link('Hi Hamza Ocean Seafood! Can you check availability for a specific seafood item?'), 'Ask on WhatsApp', 'button button-secondary')}</div>
</section>
'''

wholesale_page = f'''
<section class="page-intro wholesale-intro"><div class="shell">
  <p class="eyebrow">Restaurants, hotels and caterers</p>
  <h1>Wholesale seafood<br>for Punjab kitchens.</h1>
  <p>Share the seafood, grades and cuts you need. We’ll confirm availability, current rates and delivery to your city.</p>
  <p class="offer">Bulk discounts on seafood orders of {BULK_MINIMUM} kg or more.</p>
  <div class="actions">{button('#quote', 'Request a bulk quote', 'button button-gold')}{button('@root/products/', 'Browse seafood', 'button button-outline')}</div>
</div></section>
<section class="section shell wholesale-grid" id="quote">
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
    <button class="button button-whatsapp" type="submit">Continue to WhatsApp {icon('arrow')}</button>
  </form>
</section>
'''

guide_page = f'''
<section class="page-intro"><div class="shell">
  <h1>Seafood cutting guide</h1><p>Compare common preparations and choose your preferred cut when adding seafood to your cart. The images are illustrative.</p>
</div></section>
<section class="section shell">
  <div class="guide-grid">
  {''.join(f'<article class="guide-card"><img src="@root/assets/cuts/{key}.webp" alt="Illustration of {escape(name.lower())}" width="800" height="530" loading="lazy"><div><h2>{escape(name)}</h2><p>{escape(desc)}</p><p class="guide-use">{escape(use)}</p></div></article>' for key, name, desc, use in CUT_GUIDE)}
  </div>
  <div class="catalogue-footer"><div><h2>Ready to choose your seafood?</h2><p>We’ll confirm the cut and whether the quote uses whole or cleaned weight.</p></div>{button('@root/products/', 'Browse seafood', 'button button-secondary')}</div>
</section>
'''


def main():
    pages = [
        ('', f'Fresh Seafood for Homes & Restaurants | {BRAND}', 'Shop fresh fish and prawns sourced through Karachi Fish Harbour. Choose your cuts, order on WhatsApp or request a bulk quote for your restaurant.', homepage),
        ('products/', f'Fresh Fish & Prawns Catalogue | {BRAND}', 'Browse fresh fish, small fish and prawns. Choose weight and cuts, build your seafood cart and ask for today’s prices on WhatsApp.', products_page),
        ('wholesale/', f'Wholesale Seafood Supplier for Punjab Restaurants | {BRAND}', f'Request a wholesale quote for fish and prawns in Lahore and other major Punjab cities. Bulk discounts on orders of {BULK_MINIMUM} kg or more. Ask about cuts, grades and delivery.', wholesale_page),
        ('cutting-guide/', f'Seafood Cutting Guide | {BRAND}', 'Compare whole cleaned fish, bone-in steaks, boneless fillets, curry cuts and peeled prawns. Choose your preferred cut for your seafood order.', guide_page),
    ]
    for path, title, description, body in pages:
        folder = ROOT / path
        folder.mkdir(exist_ok=True)
        (folder / 'index.html').write_text(layout(path, title, description, body), encoding='utf-8')
    urls = '\n'.join(f'  <url><loc>{HOME}{path}</loc></url>' for path, *_ in pages)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n', encoding='utf-8')
    (ROOT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {HOME}sitemap.xml\n', encoding='utf-8')


if __name__ == '__main__':
    main()
