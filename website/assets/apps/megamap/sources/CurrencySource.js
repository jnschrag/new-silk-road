function createQueryForRange(range) {
  const currencyKey = 'funding__currency_amount';
  const currencyCode = 'USD';
  let q = {};
  for (var key in range) {
    if (range.hasOwnProperty(key)) {
      q[`${currencyKey}__${key}`] = range[key] ? `${range[key]} ${currencyCode}` : null;
    }
  }
  return q;
}

// We need to have the same keys throughout so that null values clear that entry from the query. Hurm
const lookups = {
  '<25 million USD': createQueryForRange({gte: null, lt: 25000000}),
  '25 to 80 million USD': createQueryForRange({gte:25000000, lt: 80000000}),
  '80 to 250 million USD': createQueryForRange({gte:80000000, lt: 250000000}),
  '250 to 450 million USD': createQueryForRange({gte:250000000, lt: 450000000}),
  '450 to 800 million USD': createQueryForRange({gte:450000000, lt: 800000000}),
  '800 million USD and above': createQueryForRange({gte:800000000, lt: null})
};

export default class CurrencySource {
  static fetch() {
    return new Promise(function (resolve, reject) {
      resolve(lookups);
    })
  }
}