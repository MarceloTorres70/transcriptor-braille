import { ConvertToBraillePayload, ConvertToBrailleResult } from "./contracts.js";
const API_URL = "http://localhost:5000/api/traducir";
const OCR_API_URL = "http://localhost:5000/api/ocr";

let currentMode = "es-br";

const sourceText = document.getElementById("sourceText");
const translateButton = document.getElementById("translateButton");
const clearButton = document.getElementById("clearButton");
const brailleOutput = document.getElementById("brailleOutput");
const sourcePreview = document.getElementById("sourcePreview");
const brailleCount = document.getElementById("brailleCount");
const inputCount = document.getElementById("inputCount");
const translationStatus = document.getElementById("translationStatus");
const imageInput = document.getElementById("imageInput");
const printButton = document.getElementById("printButton");
const swapModeButton = document.getElementById("swapModeButton");
const imageUploadContainer = document.querySelector(".image-upload-container");
const sourceLabel = document.getElementById("sourceLabel");
const inputHeading = document.getElementById("inputHeading");
const outputTag = document.getElementById("outputTag");
const outputHeading = document.getElementById("outputHeading");

function setOutputState(result, statusText = "Traducción completada") {
    brailleOutput.textContent = result.braille || "⠤⠤⠤";
    sourcePreview.textContent = result.text ? result.text.slice(0, 60) : "—";
    brailleCount.textContent = String(result.brailleLength);
    translationStatus.textContent = result.text ? statusText : "Listo para traducir";
}

function applyModeUi() {
    const isReverse = currentMode === "br-es";

    swapModeButton.textContent = isReverse
        ? "⇄ Traducir Español a Braille"
        : "⇄ Traducir Braille a Español";

    if (isReverse) {
        imageUploadContainer.classList.remove("hidden");
        inputHeading.textContent = "Texto en Braille Unicode";
        sourceLabel.textContent = "Pega aquí el Braille Unicode o sube una imagen";
        sourceText.placeholder = "Ejemplo: ⠨⠓⠕⠇⠁";
        outputTag.textContent = "Salida español";
        outputHeading.textContent = "Texto traducido";
    } else {
        imageUploadContainer.classList.add("hidden");
        inputHeading.textContent = "Texto en español";
        sourceLabel.textContent = "Escribe o pega aquí tu texto";
        sourceText.placeholder = "Ejemplo: Hola, mundo. 123";
        outputTag.textContent = "Salida braille";
        outputHeading.textContent = "Vista Unicode";
    }
}

async function translate() {
    const payload = new ConvertToBraillePayload(sourceText.value.trim(), "unicode");

    if (!payload.text) {
        setOutputState(new ConvertToBrailleResult(), "Listo para traducir");
        return;
    }

    translationStatus.textContent = "Traduciendo...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                texto: payload.text,
                direction: currentMode
            })
        });

        const data = await response.json();

        if (!response.ok || !data.ok) {
            throw new Error(data.error || "No se pudo traducir el texto.");
        }

        const braille = data.braille || "";
        const result = new ConvertToBrailleResult({
            text: payload.text,
            braille,
            format: payload.format,
            sourceLength: payload.text.length,
            brailleLength: braille.length
        });

        setOutputState(result, "Traducción desde API");
    } catch (error) {
        const result = new ConvertToBrailleResult({
            text: payload.text,
            braille: "",
            format: payload.format,
            sourceLength: payload.text.length,
            brailleLength: 0
        });
        setOutputState(result, "Error de conexión");
        translationStatus.textContent = `Error: ${error.message}`;
    }
}

function updateCounters() {
    const text = sourceText.value;
    inputCount.textContent = `${text.length} caracteres`;

    if (!text.trim()) {
        translationStatus.textContent = "Listo para traducir";
        sourcePreview.textContent = "—";
        brailleCount.textContent = "0";
    }
}

translateButton.addEventListener("click", translate);
clearButton.addEventListener("click", () => {
    sourceText.value = "";
    inputCount.textContent = "0 caracteres";
    setOutputState(new ConvertToBrailleResult({ text: "", braille: "", format: "unicode", sourceLength: 0, brailleLength: 0 }));
    sourceText.focus();
});

swapModeButton.addEventListener("click", () => {
    currentMode = currentMode === "es-br" ? "br-es" : "es-br";
    applyModeUi();
    sourceText.value = "";
    updateCounters();
    setOutputState(new ConvertToBrailleResult({ text: "", braille: "", format: "unicode", sourceLength: 0, brailleLength: 0 }));
});

printButton.addEventListener("click", () => {
    brailleOutput.classList.add("braille-output--mirror");
    window.print();
});
window.addEventListener("afterprint", () => {
    brailleOutput.classList.remove("braille-output--mirror");
});

sourceText.addEventListener("input", updateCounters);
sourceText.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        translate();
    }
});

imageInput.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
        const base64_string = e.target.result.split(",")[1];

        const response = await fetch(OCR_API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ imagen: base64_string })
        });

        if (response.ok) {
            const data = await response.json();
            sourceText.value = data.texto;
            updateCounters();
            await translate();
        }
    };
    reader.readAsDataURL(file);
});

applyModeUi();
updateCounters();
