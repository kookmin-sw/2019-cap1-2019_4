var user_data = {
	"user_id" : 23,
	"product_name" : "apple",
	"product_id" : 52,
	"aisle" : "fruit"
}

var user = document.getElementById('user')

user.innerHTML = "<span style='color: DarkViolet;'>" + user_data.user_id + "</span>"+ "번 고객님, " + 
				"<span style='color: MediumVioletRed;'>" + user_data.product_name + "</span>" + "은 어떠세요? " + 
				"<span style='color: SaddleBrown;'>" + user_data.aisle + "</span>" +  "코너에 준비되어있습니다.";

