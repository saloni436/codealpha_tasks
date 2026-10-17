const sourceText = document.getElementById("sourceText");
const sourceLanguage = document.getElementById("sourceLanguage");
const targetLanguage = document.getElementById("targetLanguage");
const result = document.getElementById("result");
const message = document.getElementById("message");
const charCount = document.getElementById("charCount");


document.getElementById("translate").addEventListener("click", async () => {

    const text = sourceText.value.trim();

    if (!text) {
        message.textContent = "Please enter some text.";
        return;
    }

    result.textContent = "Translating...";
    message.textContent = "";

    try {

        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                source: sourceLanguage.value,
                target: targetLanguage.value
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Translation failed.");
        }

        result.textContent = data.translatedText;
        message.textContent = "Translation completed.";

    } catch (error) {

        result.textContent = "Unable to translate.";
        message.textContent = error.message;

    }
});


document.getElementById("clear").addEventListener("click", () => {

    sourceText.value = "";
    result.textContent = "Your translation will appear here...";
    message.textContent = "";
    charCount.textContent = "0 / 5000";

});


sourceText.addEventListener("input", () => {

    charCount.textContent =
        `${sourceText.value.length} / 5000`;

});


document.getElementById("copy").addEventListener("click", async () => {

    const text = result.textContent;

    if (!text || text === "Your translation will appear here...") {
        message.textContent = "Nothing to copy.";
        return;
    }

    await navigator.clipboard.writeText(text);
    message.textContent = "Copied!";

});


document.getElementById("speak").addEventListener("click", () => {

    const text = result.textContent;

    if (!text || text === "Your translation will appear here...") {
        message.textContent = "Nothing to speak.";
        return;
    }

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = targetLanguage.value;

    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(speech);

});


document.getElementById("swap").addEventListener("click", () => {

    if (sourceLanguage.value === "auto") {
        message.textContent =
            "Select a source language before swapping.";
        return;
    }

    const oldSource = sourceLanguage.value;

    sourceLanguage.value = targetLanguage.value;
    targetLanguage.value = oldSource;

    const oldText = sourceText.value;

    sourceText.value =
        result.textContent.includes("Your translation")
            ? ""
            : result.textContent;

    result.textContent =
        oldText || "Your translation will appear here...";

});