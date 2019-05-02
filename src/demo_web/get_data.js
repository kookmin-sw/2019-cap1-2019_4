var user_data = {
	"user_id" : 23,
	"product_name" : "apple",
	"product_id" : 52,
	"aisle" : "fruit"
}

var user = document.getElementById('user')
user.innerHTML = user_data.user_id + "번 고객님, " + user_data.product_name + "은 어떠세요? " + user_data.aisle + "코너에 준비되어있습니다.";
