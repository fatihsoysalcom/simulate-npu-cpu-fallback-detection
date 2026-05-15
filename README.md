# Simulate NPU CPU Fallback Detection

This example simulates the detection of NPU (Neural Processing Unit) fallbacks to CPU in a CI environment. It measures the execution time of a simulated AI inference task and compares it against predefined performance thresholds. If the execution time exceeds the maximum acceptable limit, it flags a potential NPU fallback, mimicking how a CI system would catch such performance regressions.

## Language

`python`

## How to Run

Save the code as `npu_fallback_detector.py`.
Run from your terminal: `python npu_fallback_detector.py`

## Original Article

This example accompanies the Turkish article: [Snapdragon'da Sessiz NPU Geri Dönüşlerini CI Ortamında Yakalamanın Yolları](https://fatihsoysal.com/blog/snapdragonda-sessiz-npu-geri-donuslerini-ci-ortaminda-yakalamanin-yollari/).

## License

MIT — see [LICENSE](LICENSE).
