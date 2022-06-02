document.querySelector('.img-btn').addEventListener('click', function()
	{
		document.querySelector('.cont').classList.toggle('s-signup')
	}
);
document.querySelector("#show-login").addEventListener("click",function(){
	document.querySelector(".popup").classList.add("active");
});
document.querySelector(".popup .close-btn").addEventListener("click", function(){
	document.querySelector(".popup").classList.remove("active");
});
