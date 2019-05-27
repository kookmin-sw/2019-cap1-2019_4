function parse_query_string(query) {
  var vars = query.split("&");
  var query_string = {};

  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    var key = pair[0];
    var value = pair[1];
    value = value.replace(/%20/g,' ');
    console.log(i , key, value)


    // '===': 형식이 같은지 비교
    if (typeof query_string[key] === "undefined") {
      query_string[key] = value;
    } else if (typeof query_string[key] === "string") {
      var arr = [query_string[key], value];
      query_string[key] = arr;
    } else {
      query_string[key].push(value);
    }
  }
  return query_string;
}

var query = window.location.search.substring(1);
var qs = parse_query_string(query);
console.log(qs)

var user_id = qs.user
var user_name = qs.user_name
var product_name = qs.product_name
var bucket_url = qs.bucket_url
var product_aisle = qs.product_aisle
var current_time = qs.current_time

function write_user_name() {
  var temp = user_name
  document.write(temp.fontcolor("DodgerBlue"))
}

function write_product_name() {
  var temp = product_name
  document.write(temp.fontcolor("Red"))
}

function write_product_aisle() {
  var temp = product_aisle
  document.write(temp.fontcolor("Orange"))
}

function write_current_time() {
  var temp = current_time
  document.write(temp.fontcolor("Gray"))
}

function write_image() {
  document.write('<img src=' + bucket_url + ' width="100%" alt="ad">')
}
