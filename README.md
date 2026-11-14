# Hamza Ocean Seafood

## Publish

1. Extract this ZIP into the same GitHub Pages publishing folder you used for the previous website. Upload its contents, including `.nojekyll`.
2. Replace matching files. Keep your existing Pages branch and settings. The previous `cutting-guide/index.html` is now a redirect, so replace it as well.
3. After deployment, check the homepage video, catalogue, wholesale page, and contact form on the published URL.

The site has three pages: Home, Products (with the cutting guide), and Wholesale. The ZIP already contains the generated HTML and needs no build step for publishing. To preview locally, run `python3 -m http.server 8000` in the extracted folder and open `http://localhost:8000`.

## Updating the site

- Edit `catalogue.json` to update seafood, photos, contact numbers and analytics. Add catalogue photos to `assets/catalogue/`. Use an empty image field when a confirmed photo is unavailable.
- Homepage, header, and footer copy is in `tools/templates/`. Run `python3 tools/build.py` after editing the templates or catalogue, then commit the regenerated HTML, changed source, and assets.
- The hero uses the original Vimeo ocean video and shows its original image first. It keeps the image when background playback is unavailable. The process video is embedded with Vimeo's playback controls and has a direct link.
- The WhatsApp cart and wholesale quote direct customers to +92 371 0359521. The Contact section also lists +92 335 0213648. Bulk discounts apply from 20 kg.
- The site retains GA4 measurement ID `G-JGS17XB776`. To enable Meta Pixel, replace `YOUR_META_PIXEL_ID` with your numeric ID in `catalogue.json` and rebuild. Analytics loads on the production origin. WhatsApp events track opening a draft.
- The contact form uses the original Web3Forms integration. Check delivery to your inbox after deployment.

## Product photos

The product cards use original photos from the brand or supplied for this catalogue, resized for the web. The Rawas card uses the newly supplied Indian Salmon photo. The Black Barracuda card uses a resized [reference photo by Nasser Halaweh](https://commons.wikimedia.org/wiki/File:Military_Barracuda_imported_from_iNaturalist_photo_18012051_on_1_February_2023.jpg), licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Queenfish and Mushka are listed with photos on request. The cutting guide uses diagrams.
