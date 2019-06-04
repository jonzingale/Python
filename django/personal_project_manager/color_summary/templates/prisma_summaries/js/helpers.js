function normalize(array, total=0) {
  var biggest = array[0].percent

  array.forEach(function(item, i){
    array[i]['percent'] = item.percent / biggest
  })
}

function pp(data) {
  console.log(JSON.stringify(data))
}

function mod(a,b){return(((a % b) + b) % b)}

function div(a,b){return(Math.floor(a/b))}

function add(ls) {return ls.reduce((a,i) => a+i)}