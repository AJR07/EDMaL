// slider initial position
const slider = document.getElementById("item-selector-slider");
const itemSelector = document.getElementById("item-selector");
slider.style.width = itemSelector.children[0].getBoundingClientRect().width + "px";
slider.style.left = (itemSelector.children[0].getBoundingClientRect().x - 1) + "px";



// slider animation
for (let i = 0; i < itemSelector.children.length; i++) {
	const element = itemSelector.children[i];
	// handle when hovered
	element.addEventListener("mouseover", () => {
		// transition the slider to the center of the hovered element
		let details = element.getBoundingClientRect();
		slider.style.width = details.width + "px";
		slider.style.left = (details.x - 1) + "px";
	});

	// handle when clicked
	element.addEventListener("click", () => {
		let id = element.innerHTML.toLowerCase().replace(" ", "-");
		const newElement = document.getElementById(id);
		let oldID = document.getElementsByClassName("selected")[0].innerHTML.toLowerCase().replace(" ", "-");
		const oldElement = document.getElementById(oldID);

		// transition oldElement out by fading
		oldElement.style.opacity = 0;

		// transition newElement in by fading
		newElement.style.opacity = 1;

		// change selected classname
		document.getElementsByClassName("selected")[0].classList.remove("selected");
		element.classList.add("selected");
	});
};