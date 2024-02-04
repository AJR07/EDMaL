const buttonRFC = document.getElementById("rfc-run");

buttonRFC.addEventListener("click", async () => {
	buttonRFC.classList.add("disabled");
	buttonRFC.disabled = true;

	const resultElements = [
		document.getElementById("rfc-text-pruning-result"),
		document.getElementById("rfc-mask-result1"),
		document.getElementById("rfc-mask-result2"),
		document.getElementById("rfc-regenerate"),
		document.getElementById("rfc-tokenized-old"),
		document.getElementById("rfc-tokenized-new"),
		document.getElementById("rfc-ngram"),
		document.getElementById("rfc-score"),
		document.getElementById("rfc-result")
	];

	for (let element of resultElements) {
		element.innerHTML = "loading...";
	}

	try {
		//! prune data
		let text = document.getElementById("rfc-text").value;
		if (text.split(" ").length < 10) {
			alert("Please enter at least 10 words.");
			return;
		}

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

		//! N Gram Calculation
		response = await fetch("/api/ngram", {
			method: "POST",
			body: JSON.stringify({
				text1: truncatedHalf,
				text2: regeneratedHalf
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let [tokensMasked, tokensRegenerated, ngram] = (await response.json()).result;
		resultElements[4].innerHTML = tokensMasked;
		resultElements[5].innerHTML = tokensRegenerated;
		resultElements[6].innerHTML = ngram.join(", ");

		//! RFC Score Calculation
		response = await fetch("/api/svm", {
			method: "POST",
			body: JSON.stringify({
				ngram: ngram
			}),
			headers: {
				"Content-Type": "application/json"
			}
		});
		let score = (await response.json()).result;
		resultElements[7].innerHTML = score;
		resultElements[8].innerHTML = score == 0 ? "Human Written" : "AI Generated";
	} catch (error) {
		console.error(error);
	}
	buttonRFC.disabled = false;
	buttonRFC.classList.remove("disabled");
});