// Update each product here. Leave unknown prices, artwork, and URLs unset.
const products = [
  { name: 'Ocean Hero figurines', image: 'hero.webp', alt: 'Ocean Guardian #001 surfing above a coral reef and hex habitat module', description: 'Ocean Guardian #001 pairs a surfer with a wave and reef display base. Concept artwork shown.' },
  { name: 'Stickers', description: 'Planned stickers inspired by the Ocean Guardians collection.' },
  { name: 'Keychains', description: 'Planned pocket-sized Ocean Guardians collectibles.' },
  { name: 'T-shirts', image: 'tee.webp', alt: 'Navy Ocean Guardian T-shirt concept featuring a surfer and reef', description: 'Surf and reef artwork inspired by Ocean Guardian #001. Concept mockup shown.' },
  { name: 'Collectors card set', description: 'A planned physical card set featuring Ocean Guardians characters, waves, and reef habitats.' },
];

const grid = document.querySelector('#products');
const template = document.querySelector('#product-card');
for (const product of products) {
  const card = template.content.cloneNode(true);
  card.querySelector('h3').textContent = product.name;
  if (product.name === 'Collectors card set') card.querySelector('h3').id = 'collector-card-set';
  card.querySelector('.pending').textContent = product.price ?? 'Coming soon';
  card.querySelector('.description').textContent = product.description;
  const art = card.querySelector('.card-art');
  if (product.image) {
    const image = document.createElement('img');
    image.src = 'assets/ocean-guardians/' + product.image;
    image.alt = product.alt;
    image.loading = 'lazy';
    art.append(image);
  } else {
    art.textContent = 'Artwork pending';
  }
  const link = card.querySelector('a');
  link.href = product.checkoutUrl ?? product.inquiryUrl ??
    'mailto:infobalamha@gmail.com?subject=' + encodeURIComponent('Ocean Guardians inquiry — ' + product.name);
  link.textContent = (product.checkoutUrl ? 'Shop ' : 'Ask about ') + product.name.toLowerCase();
  grid.append(card);
}
