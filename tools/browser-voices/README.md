# Fixed-voice listening trial

The public trial is limited to the October 27, 2026 edition (66 cards).
`dist/english-listening-loader.js` keeps all other dates on the existing player.

Teachers / partners: Heart / Puck, Bella / Fenrir, Sky / Michael,
Aoede / Echo, Kore / Onyx, Sarah / Liam.
The speaking paces are 0.75, 0.80, 0.85, 0.90, 0.95 and 1.00.

Title and conversation recordings are prepared ahead of playback. Conversation
turns share a single WAV file, with a 160 ms inserted gap and short natural
leading/trailing margins. Voice pitch is kept independent of the speaking pace.
The browser preloads and decodes only the selected level's recordings.

Full-card narration uses the same fixed voices in a lazy-loaded, on-device
Kokoro worker. Its first playback still needs model download and synthesis.
Lesson text is never sent to a speech API. PNG downloads remain silent.

Run `python3 tools/audit_oct27_listening.py` to check this edition.

To rebuild the browser worker, run `npm ci` and `npm run build` here.
Set JR_KOKORO_MODEL_CACHE to a local copy of the official
onnx-community/Kokoro-82M-v1.0-ONNX repository containing config.json,
tokenizer files and onnx/model_quantized.onnx. The build script patches the
voice loader to use same-origin files and includes the twelve selected voices.
Third-party license files are shipped alongside the model/runtime assets.
