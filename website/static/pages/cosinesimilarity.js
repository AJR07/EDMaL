const button = document.getElementById("cosine-similarity-run")
button.addEventListener("click", async () => {
	button.classList.add("disabled");
	button.disabled = true;

	const resultElements = [
		document.getElementById("cosine-similarity-text-pruning-result"),
		document.getElementById("cosine-similarity-mask-result1"),
		document.getElementById("cosine-similarity-mask-result2"),
		document.getElementById("cosine-similarity-regenerate"),
		document.getElementById("cosine-similarity-tokenized-new"),
		document.getElementById("cosine-similarity-word-embeddings-new"),
		document.getElementById("cosine-similarity-tokenized-old"),
		document.getElementById("cosine-similarity-word-embeddings-old"),
		document.getElementById("cosine-similarity-score"),
		document.getElementById("cosine-similarity-result")
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
		let regeneratedHalf = (await response.json()).result.slice(truncatedHalf.length + 343);
		resultElements[3].innerHTML = regeneratedHalf;

		//! cosineSimilarity
		response = await fetch("/api/cosine-similarity", {
			method: "POST",
			body: JSON.stringify({
				text1: maskedHalf,
				text2: regeneratedHalf
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let [tokensMasked, embeddingsMasked, tokensRegenerated, embeddingsRegenerated, cosineSimilarityScore] = (await response.json()).result;
		resultElements[4].innerHTML = tokensMasked;
		resultElements[5].innerHTML = embeddingsMasked.map((x) => x.toFixed(3));
		resultElements[6].innerHTML = tokensRegenerated;
		resultElements[7].innerHTML = embeddingsRegenerated.map((x) => x.toFixed(3));
		resultElements[8].innerHTML = cosineSimilarityScore;
		resultElements[9].innerHTML = (cosineSimilarityScore > 0.764 ? "AI-Generated" : "Human-Written")
	} catch (error) {
		console.error(error);
	}
	button.disabled = false;
	button.classList.remove("disabled");
});