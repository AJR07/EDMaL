document.getElementById("navbar-right").childNodes.forEach((element) => {
	// handle when hovered
	const slider = document.getElementById("navbar-slider");
	element.addEventListener("mouseover", () => {
		// transition the slider to the center of the hovered element
		let details = element.getBoundingClientRect();
		slider.style.width = details.width + "px";
		slider.style.left = (details.x - 15) + "px";
	});

	// handle when clicked
	element.addEventListener("click", () => {
		let id = element.nodeValue.toLowerCase().replace(" ", "-");
		document.getElementById(id)?.scrollIntoView({ behavior: "smooth" });
	});
});