// Jaguar Marine Systems merchandise catalog.
// No product is available for purchase until a real checkout URL and approved price are supplied.
// Images marked as references are NOT production-ready garment previews.
const products = [
  {
    name: 'Ocean Hero figurines',
    image: 'hero.webp',
    alt: 'Ocean Guardian #001 surfer with a wave and reef display base, concept artwork',
    description: 'Ocean Guardian #001 pairs a surfer with a wave and reef display base. Concept artwork shown; manufacturing and release details are pending.'
  },
  { name: 'Stickers', description: 'Planned stickers featuring Ocean Guardians, jaguar, and hex-reef artwork. Final designs and pricing are pending.' },
  { name: 'Keychains', description: 'Planned pocket-sized Ocean Guardians and Jaguar Marine Systems collectibles. Final materials and pricing are pending.' },
  { name: 'Collectors card set', description: 'A planned physical card set featuring Ocean Guardians characters, waves, reef habitats, and the hex-module story.' }
];

const grid = document.querySelector('#products');
const template = document.querySelector('#product-card');
if (grid && template) {
  for (const product of products) {
    const card = template.content.cloneNode(true);
    card.querySelector('h3').textContent = product.name;
    if (product.name === 'Collectors card set') card.querySelector('h3').id = 'collector-card-set';
    card.querySelector('.pending').textContent = product.price ?? 'Coming soon';
    card.querySelector('.description').textContent = product.description;
    const art = card.querySelector('.card-art');
    if (product.image || product.imageUrl) {
      const image = document.createElement('img');
      image.src = product.imageUrl ?? 'assets/ocean-guardians/' + product.image;
      image.alt = product.alt ?? product.name + ' concept reference';
      image.loading = 'lazy';
      art.append(image);
    } else {
      art.textContent = product.artworkStatus ?? 'Artwork pending';
    }
    const link = card.querySelector('a');
    link.href = product.checkoutUrl ?? product.inquiryUrl ??
      'mailto:infobalamha@gmail.com?subject=' + encodeURIComponent('JMS merchandise inquiry — ' + product.name);
    link.textContent = (product.checkoutUrl ? 'Shop ' : 'Ask about ') + product.name.toLowerCase();
    grid.append(card);
  }
}
