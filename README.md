# 🚀 RomaPy

**RomaPy** is a high-performance JIT (Just-In-Time) optimization engine that turns sluggish Python math into compiled machine code speeds.

## 🏎️ Performance
- **Standard Python:** ~60.0s (10M operations)
- **RomaPy:** **0.32s** (10M operations)
- **Speedup:** ~180x

## ⚡ Quick Start
1. Install: `pip install -e .`
2. Run any script: `romapy your_script.py`

## 🛠️ Features
- **Auto-Acceleration:** No complex code changes needed.
- **AI Optimized:** Built for NumPy and heavy vector logic.
- **Smart Fallback:** If it can't be JIT-ed, it runs at normal speed (no crashes).
