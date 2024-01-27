const button = document.getElementById("cosine-similarity-run")
button.addEventListener("click", async () => {
	button.classList.add("disabled");

	const resultElements = [
		document.getElementById("cosine-similarity-text-pruning-result"),
		document.getElementById("cosine-similarity-mask-result1"),
		document.getElementById("cosine-similarity-mask-result2"),
	];

	for (let element of resultElements) {
		element.innerHTML = "loading...";
	}

	try {
		//! prune data
		let text = document.getElementById("cosine-similarity-text").value;
		let response = await fetch("/api/prune", {
			method: "POST",
			body: JSON.stringify({
				input_data: text
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let data = await response.json();
		resultElements[0].innerHTML = data.result;

		//! mask out half
		let truncatedHalf = data.result.slice(0, Math.floor(data.result.length / 2));
		resultElements[1].innerHTML = truncatedHalf;
		let maskedHalf = data.result.slice(Math.floor(data.result.length / 2));
		resultElements[2].innerHTML = maskedHalf;

		//! regeneratre half
		

	} catch (error) {
		console.error(error);
	}
	button.classList.remove("disabled");
});