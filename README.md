# Hamza Ocean Seafood

## Deploy to GitHub Pages

1. Extract the ZIP. Put its contents at the root of the existing HamzaOceanSeafood repository or in the existing Pages publishing folder if you use one. The site needs no build step to deploy.
2. Commit and push to the existing Pages branch. Keep the current repository name and Pages source settings to retain the public URL.
3. Open the published home, catalogue, cutting guide, and wholesale pages. Check the WhatsApp draft on a phone and confirm Google Analytics receives events in the existing property.

To preview locally, run `python3 -m http.server 8000` from the extracted folder and open `http://localhost:8000`.

## Update products or settings

Edit `catalogue.json`. The order of the products in the file is the order shown in the catalogue. Use a unique product ID, keep the category set to Fish, Small fish, or Prawns, and put new catalogue photos in `assets/catalogue/`. Leave the image field empty when a verified photo is unavailable. Run `python3 tools/build.py` and commit the changed JSON, assets, and generated HTML together.

The cart and quote form prepare WhatsApp drafts for +92 371 0359521. Customers send the drafts from WhatsApp. The secondary number appears in Contact. The discount starts at 20 kg of requested seafood. Rates and delivery are confirmed in chat.

## Analytics

The site retains GA4 measurement ID `G-JGS17XB776` and the `whatsapp_order_click` event. Wholesale handoffs are recorded as `wholesale_whatsapp_click`. The site measures WhatsApp handoffs. It cannot see whether a visitor sent the draft or completed a purchase.

Replace `YOUR_META_PIXEL_ID` in `catalogue.json` with the numeric ID and rerun the builder to activate Meta Pixel. Check PageView, AddToCart and Contact in Meta Events Manager after publishing. Analytics loads on the existing production origin. If you later change domains, update the canonical homepage URL in `tools/build.py` and rebuild.

## Product images

The supplied catalogue photos were restyled for a consistent background. Black Barracuda uses an AI-restyled [reference photo by Nasser Halaweh](https://commons.wikimedia.org/wiki/File:Military_Barracuda_imported_from_iNaturalist_photo_18012051_on_1_February_2023.jpg), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The cutting-guide photos illustrate the available preparation styles. Queenfish, Mushka and Indian Salmon (Rawas) are listed with photos on request. Kanarcha is shown as a red snapper market name based on the [FAO Pakistan fisheries field guide](https://www.fao.org/4/r7066e/r7066e13.pdf).
