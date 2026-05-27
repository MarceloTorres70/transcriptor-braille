export class ConvertToBraillePayload {
    constructor(text, format = "unicode") {
        this.text = text;
        this.format = format;
    }
}

export class ConvertToBrailleResult {
    constructor({ text = "", braille = "", format = "unicode", sourceLength = 0, brailleLength = 0 } = {}) {
        this.text = text;
        this.braille = braille;
        this.format = format;
        this.sourceLength = sourceLength;
        this.brailleLength = brailleLength;
    }
}
