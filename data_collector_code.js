// this is the code for my data collector which you can build at http://brightdata.grsm.io/tuomas

// Stage 1
for (let i=101; i < 300; i++) {
  next_stage({page_link: `https://www.propertyfinder.ae/en/search?c=2&fu=0&l=1&ob=mr&page=${i}&rp=y`});
}

// Stage 2
try {
 navigate(input.page_link); 
 let data = parse();
 for (const link of data.links) {
  try {
    next_stage({url: link});
  }
  catch {
    console.log('no link provided')
  }
}
} catch {
  console.log("link error")
}

// Parser code Stage 2
return {
//   title: $('h1').text().trim(),
  links: $('a.card__link').toArray().map(e=>new URL($(e).attr('href'), "https://www.propertyfinder.ae/").href),
};

// Stage 3
navigate(input.url)
wait('.text.text--size1.property-page__search-items', {timeout: 10000});
wait('.property-facts__value', {timeout: 10000});
wait('.property-price__price', {timeout: 10000})
collect(parse())

// Parser code Stage 3
return {
  url: location.href,
  area: $('.text.text--size1.property-page__search-items').text().replace(/Properties for Rent in /g, '').replace(/[\n\t]/g, ''),
  price: $('.property-price__price').text().substring(0, $('.property-price__price').text().indexOf(' ')).replace(',', ''),
  facts: $('.property-facts__value').toArray().map(e=>$(e).text().replace(/[\n\t]/g, '')),
  amenities: $('.property-amenities__list').toArray().map(e=>$(e).text().replace(/[\n\t]/g, '')),
}
