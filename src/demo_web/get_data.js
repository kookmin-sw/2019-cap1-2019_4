function parse_query_string(query) {
  var vars = query.split("&");
  var query_string = {};

  for (var i = 0; i < vars.length; i++) {
    var pair = vars[i].split("=");
    var key = decodeURIComponent(pair[0]);
    var value = decodeURIComponent(pair[1]);

    // '===': 형식이 같은지 비교
    if (typeof query_string[key] === "undefined") {
      query_string[key] = decodeURIComponent(value);
    } else if (typeof query_string[key] === "string") {
      var arr = [query_string[key], decodeURIComponent(value)];
      query_string[key] = arr;
    } else {
      query_string[key].push(decodeURIComponent(value));
    }
  }
  return query_string;
}

var query = window.location.search.substring(1);
var qs = parse_query_string(query);

var user_id = qs.user
var user_name = qs.user_name
var product_id = qs.product_id
var product_name = qs.product_name
var bucket_url = qs.bucket_url
var product_aisle = 43

// HTML 내용 구성
document.write( '<p> <span style="color: DarkViolet; font-size:20px;"><b>' + user_name + '</b></span> 고객님 ' );
document.write( '<span style="color: MediumVioletRed; font-size:20px;"><b>' + product_name + '</b></span>은 어떠세요? <span style="color: SaddleBrown;  font-size:20px;"><b>' + product_aisle + '</b></span>번 코너에 준비되어 있습니다.<br></p>' );
document.write('<img src=' + bucket_url + ' alt="ad">')
