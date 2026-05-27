import { ConvertToBraillePayload, ConvertToBrailleResult } from "./contracts.js";

const brailleMap = {
    a: "⠁",
    b: "⠃",
    c: "⠉",
    d: "⠙",
    e: "⠑",
    f: "⠋",
    g: "⠛",
    h: "⠓",
    i: "⠊",
    j: "⠚",
    k: "⠅",
    l: "⠇",
    m: "⠍",
    n: "⠝",
    o: "⠕",
    p: "⠏",
    q: "⠟",
    r: "⠗",
    s: "⠎",
    t: "⠞",
    u: "⠥",
    v: "⠧",
    w: "⠺",
    x: "⠭",
    y: "⠽",
    z: "⠵",
    á: "⠷",
    é: "⠮",
    í: "⠌",
    ó: "⠬",
    ú: "⠾",
    ü: "⠳",
    ñ: "⠫",
    " ": " ",
    ",": "⠂",
    ".": "⠲",
    ";": "⠆",
    ":": "⠒",
    "!": "⠖",
    "?": "⠦",
    "(" : "⠷",
    ")": "⠾",
    "-": "⠤",
    "'": "⠄",
    "@": "⠈",
    "/": "⠌",
    "&": "⠯",
    "%": "⠩",
    "+": "⠖",
    "*": "⠡",
    "=": "⠿"
};

const digitMap = {
    1: "⠁",
    2: "⠃",
    3: "⠉",
    4: "⠙",
    5: "⠑",
    6: "⠋",
    7: "⠛",
    8: "⠓",
    9: "⠊",
    0: "⠚"
};

const numberPrefix = "⠼";
const capitalPrefix = "⠠";

const sourceText = document.getElementById("sourceText");
const translateButton = document.getElementById("translateButton");
const clearButton = document.getElementById("clearButton");
const brailleOutput = document.getElementById("brailleOutput");
const sourcePreview = document.getElementById("sourcePreview");
const brailleCount = document.getElementById("brailleCount");
const inputCount = document.getElementById("inputCount");
const translationStatus = document.getElementById("translationStatus");

function normalizeInput(value) {
    return value.replace(/\r\n/g, "\n");
}

function convertTextToBraille(value) {
    let result = "";
    let isNumberMode = false;

    for (const char of normalizeInput(value)) {
        if (/\d/.test(char)) {
            if (!isNumberMode) {
                result += numberPrefix;
                isNumberMode = true;
            }

            result += digitMap[char] ?? "";
            continue;
        }

        isNumberMode = false;

        if (/[A-ZÁÉÍÓÚÜÑ]/.test(char)) {
            result += capitalPrefix;
            result += brailleMap[char.toLowerCase()] ?? "⠿";
            continue;
        }

        result += brailleMap[char] ?? "⠿";
    }

    return result;
}

function setOutputState(result) {
    brailleOutput.textContent = result.braille || "⠤⠤⠤";
    sourcePreview.textContent = result.text ? result.text.slice(0, 60) : "—";
    brailleCount.textContent = String(result.brailleLength);
    translationStatus.textContent = result.text ? "Traducción simulada" : "Listo para traducir";
}

function translate() {
    const payload = new ConvertToBraillePayload(sourceText.value.trim(), "unicode");
    const braille = convertTextToBraille(payload.text);
    const result = new ConvertToBrailleResult({
        text: payload.text,
        braille,
        format: payload.format,
        sourceLength: payload.text.length,
        brailleLength: braille.length
    });

    setOutputState(result);
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

sourceText.addEventListener("input", updateCounters);
sourceText.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        translate();
    }
});

updateCounters();