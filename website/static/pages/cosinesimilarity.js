const button = document.getElementById("cosine-similarity-run")
button.addEventListener("click", async () => {
	button.classList.add("disabled");

	const resultElements = [
		document.getElementById("cosine-similarity-text-pruning-result"),
		document.getElementById("cosine-similarity-mask-result1"),
		document.getElementById("cosine-similarity-mask-result2"),
		document.getElementById("cosine-similarity-regenerate"),
		document.getElementById("cosine-similarity-tokenized-new"),
		document.getElementById("cosine-similarity-word-embeddings-new"),
		document.getElementById("cosine-similarity-tokenized-old"),
		document.getElementById("cosine-similarity-word-embeddings-old"),
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
		data = (await response.json()).result.slice(truncatedHalf.length + 343);
		resultElements[3].innerHTML = data;

		//! tokenize and embed maskedHalf
		response = await fetch("/api/tokenize-embed", {
			method: "POST",
			body: JSON.stringify({
				input_data: maskedHalf
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let maskedHalfEmbedding = (await response.json()).result;
		resultElements[4].innerHTML = maskedHalfEmbedding[0];
		resultElements[5].innerHTML = maskedHalfEmbedding[1];

		//! tokenize and embed regenerated half
		response = await fetch("/api/tokenize-embed", {
			method: "POST",
			body: JSON.stringify({
				input_data: data
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let regeneratedHalfEmbedding = (await response.json()).result;
		resultElements[6].innerHTML = regeneratedHalfEmbedding[0];
		resultElements[7].innerHTML = regeneratedHalfEmbedding[1];



	} catch (error) {
		console.error(error);
	}
	button.classList.remove("disabled");
});