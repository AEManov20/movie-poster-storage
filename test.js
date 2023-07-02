let tst = require('./movies.json');

console.log(tst.filter((v) => v.id === 7 || v.id == 9))