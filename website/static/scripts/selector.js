// slider initial position
const slider = document.getElementById("item-selector-slider");
const itemSelector = document.getElementById("item-selector");

// slider animation
for (let i = 0; i < itemSelector.children.length; i++) {
	const element = itemSelector.children[i];

	// handle when clicked
	element.addEventListener("click", () => {
		let details = element.getBoundingClientRect();
		slider.style.width = details.width + "px";
		slider.style.left = details.x + "px";

		let id = element.innerHTML.toLowerCase().replace(" ", "-");
		const newElement = document.getElementById(id);
		let oldID = document.getElementsByClassName("selected")[0].innerHTML.toLowerCase().replace(" ", "-");
		const oldElement = document.getElementById(oldID);

		// transition oldElement out by fading
		oldElement.style.opacity = 0;
		setTimeout(() => {
			// hide oldElement
			oldElement.style.display = "none";
			oldElement.style.zIndex = 0;

			// transition newElement in by fading
			newElement.style.display = "block";
			newElement.style.opacity = 1;
			newElement.style.zIndex = 1;
		}, 200);

		// change selected classname
		document.getElementsByClassName("selected")[0].classList.remove("selected");
		element.classList.add("selected");
	});
};

itemSelector.children[0].dispatchEvent(new Event("mouseover"));
itemSelector.children[0].click();