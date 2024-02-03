const buttonEditDistance = document.getElementById("edit-distance-run")
buttonEditDistance.addEventListener("click", async () => {
	buttonEditDistance.classList.add("disabled");
	buttonEditDistance.disabled = true;

	const resultElements = [
		document.getElementById("edit-distance-text-pruning-result"),
		document.getElementById("edit-distance-mask-result1"),
		document.getElementById("edit-distance-mask-result2"),
		document.getElementById("edit-distance-regenerate"),
		document.getElementById("edit-distance-tokenized-old"),
		document.getElementById("edit-distance-tokenized-new"),
		document.getElementById("edit-distance-score"),
		document.getElementById("edit-distance-result")
	];

	for (let element of resultElements) {
		element.innerHTML = "loading...";
	}

	try {
		//! prune data
		let text = document.getElementById("edit-distance-text").value;
		let response = await fetch("/api/prune", {
			method: "POST",
			body: JSON.stringify({
				input_data: text
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let data = (await response.json()).result;
		resultElements[0].innerHTML = data;

		//! mask out half
		let truncatedHalf = data.slice(0, Math.floor(data.length / 2));
		resultElements[1].innerHTML = truncatedHalf;
		let maskedHalf = data.slice(Math.floor(data.length / 2));
		resultElements[2].innerHTML = maskedHalf;

		//! regenerate half
		response = await fetch("/api/regenerate", {
			method: "POST",
			body: JSON.stringify({
				input_data: truncatedHalf
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let regeneratedHalf = (await response.json()).result.slice(truncatedHalf.length + 343);
		resultElements[3].innerHTML = regeneratedHalf;

		//! editDistance
		response = await fetch("/api/edit-distance", {
			method: "POST",
			body: JSON.stringify({
				text1: truncatedHalf,
				text2: regeneratedHalf
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let [tokensMasked, tokensRegenerated, editDistanceScore, prediction] = (await response.json()).result;
		resultElements[4].innerHTML = tokensMasked;
		resultElements[5].innerHTML = tokensRegenerated;
		resultElements[6].innerHTML = editDistanceScore;
		resultElements[7].innerHTML = prediction;
	} catch (error) {
		console.error(error);
	}
	buttonEditDistance.disabled = false;
	buttonEditDistance.classList.remove("disabled");
});