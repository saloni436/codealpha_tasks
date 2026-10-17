
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const typing = document.getElementById("typing");
const sendButton = document.getElementById("send-button");

let isBusy = false;

function addMessage(text, sender) {
    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const label = document.createElement("span");
    label.className = "message-label";
    label.textContent = sender === "user" ? "YOU" : "PYFAQ";

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    message.append(label, bubble);
    messages.appendChild(message);
    message.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

async function sendMessage(text) {
    const question = text.trim();

    if (!question || isBusy) {
        return;
    }

    isBusy = true;
    welcome.hidden = true;
    addMessage(question, "user");

    messageInput.value = "";
    messageInput.disabled = true;
    sendButton.disabled = true;
    typing.hidden = false;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message: question })
        });

        const data = await response.json();

        if (!response.ok) {
            addMessage(
                data.error || "Something went wrong. Please try again.",
                "bot"
            );
        } else {
            addMessage(
                data.answer || "Sorry, I couldn't find an answer.",
                "bot"
            );
        }
    } catch (error) {
        addMessage(
            "I couldn't connect to the server. Please check that PyFAQ is running and try again.",
            "bot"
        );
    } finally {
        isBusy = false;
        typing.hidden = true;
        messageInput.disabled = false;
        sendButton.disabled = false;
        messageInput.focus();
    }
}

chatForm.addEventListener("submit", function (event) {
    event.preventDefault();
    sendMessage(messageInput.value);
});

document.querySelectorAll(".suggestion").forEach(function (button) {
    button.addEventListener("click", function () {
        const question = button.textContent
            .replace("↗", "")
            .replace(/^\d+/, "")
            .trim();

        sendMessage(question);
    });
});
