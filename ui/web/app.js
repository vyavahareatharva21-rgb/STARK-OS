const form = document.getElementById("chat-form");
const input = document.getElementById("message-input");
const messages = document.getElementById("messages");
const state = document.getElementById("state");


// ---------------------------------------------------------
// CHAT
// ---------------------------------------------------------

function addMessage(label, text, type) {

    const message = document.createElement("div");

    message.className = `message ${type}`;

    const labelElement = document.createElement("div");

    labelElement.className = "message-label";
    labelElement.textContent = label;

    const textElement = document.createElement("div");

    textElement.textContent = text;

    message.appendChild(labelElement);
    message.appendChild(textElement);

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


// ---------------------------------------------------------
// STATE
// ---------------------------------------------------------

function setState(text) {

    state.textContent = text;

}


// ---------------------------------------------------------
// FORMAT UPTIME
// ---------------------------------------------------------

function formatUptime(seconds) {

    seconds = Math.floor(seconds);

    const days = Math.floor(seconds / 86400);

    seconds %= 86400;

    const hours = Math.floor(seconds / 3600);

    seconds %= 3600;

    const minutes = Math.floor(seconds / 60);

    seconds %= 60;


    if (days > 0) {

        return `${days}d ${hours}h ${minutes}m`;

    }


    return `${String(hours).padStart(2, "0")}:` +
           `${String(minutes).padStart(2, "0")}:` +
           `${String(seconds).padStart(2, "0")}`;

}


// ---------------------------------------------------------
// LIVE SYSTEM STATUS
// ---------------------------------------------------------

async function loadStatus() {

    try {

        const response = await fetch(
            "/api/status",
            {
                cache: "no-store"
            }
        );


        if (!response.ok) {

            throw new Error("Status request failed");

        }


        const data = await response.json();


        // SYSTEM STATES

        document.getElementById(
            "core-text"
        ).textContent = data.core;


        document.getElementById(
            "memory-text"
        ).textContent = data.memory;


        document.getElementById(
            "ai-text"
        ).textContent = data.ai;


        // TOP STATUS INDICATORS

        document.getElementById(
            "core-status"
        ).textContent = "●";


        document.getElementById(
            "memory-status"
        ).textContent = "●";


        document.getElementById(
            "ai-status"
        ).textContent = "●";


        // CPU

        document.getElementById(
            "cpu-value"
        ).textContent =
            `${Number(data.cpu_percent).toFixed(1)}%`;


        // RAM PERCENTAGE

        document.getElementById(
            "ram-value"
        ).textContent =
            `${Number(data.memory_percent).toFixed(1)}%`;


        // RAM USAGE

        document.getElementById(
            "memory-usage"
        ).textContent =
            `${Number(data.memory_used_gb).toFixed(2)} / ` +
            `${Number(data.memory_total_gb).toFixed(1)} GB`;


        // PYTHON

        document.getElementById(
            "python-value"
        ).textContent = data.python;


        // PLATFORM

        document.getElementById(
            "platform-value"
        ).textContent = data.platform;


        // UPTIME

        document.getElementById(
            "uptime-value"
        ).textContent =
            formatUptime(data.uptime_seconds);


    } catch (error) {

        console.error(
            "STARK status error:",
            error
        );

        setState("BACKEND OFFLINE");

    }

}


// ---------------------------------------------------------
// CHAT FORM
// ---------------------------------------------------------

form.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        const message = input.value.trim();


        if (!message) {

            return;

        }


        addMessage(
            "YOU",
            message,
            "user-message"
        );


        input.value = "";


        setState("PROCESSING");


        try {

            const response = await fetch(
                "/api/chat",
                {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        message: message
                    })

                }
            );


            if (!response.ok) {

                throw new Error(
                    "Chat request failed"
                );

            }


            const data = await response.json();


            addMessage(
                "STARK",
                data.response,
                "stark-message"
            );


            setState("SYSTEM READY");


        } catch (error) {

            console.error(
                "STARK chat error:",
                error
            );


            addMessage(
                "STARK",
                "Unable to connect to the STARK backend.",
                "stark-message"
            );


            setState(
                "CONNECTION ERROR"
            );

        }

    }
);


// ---------------------------------------------------------
// START SYSTEM MONITOR
// ---------------------------------------------------------

loadStatus();


// Refresh system information every 3 seconds.

setInterval(
    loadStatus,
    3000
);