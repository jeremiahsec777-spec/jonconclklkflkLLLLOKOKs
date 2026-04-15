CocoonGlass: Offline Liquid-UI Voice Architect
CocoonGlass is a high-performance recreation of the CocoonWeaver concept, built for Android 13+ (MIUI 14). It leverages local AI transcription and a futuristic "Liquid Glass" iOS 26-inspired aesthetic to transform voice thoughts into structured, local-first knowledge.

🌀 Project Philosophy
100% Air-Gapped: No data leaves the device. All transcription and processing happen locally.

Vibecoding Ready: Designed for seamless interaction with AI-assisted development workflows.

Architectural Stability: Optimized for the Snapdragon 732G chipset with strict RAM management for MIUI 14.

Tactile UI: A "Liquid Glass" interface utilizing GLSL shaders for real-time refraction and 120Hz fluid motion.

🛠 Tech Stack
Framework: Python (Kivy + KivyMD) with pyjnius for deep Android API integration.

Transcription Engine: whisper.cpp (ARM64 NEON optimized).

Models: Support for GGML quantized models (Tiny to Medium).

UI/UX: Custom GLSL Shaders for glass refraction and speculative highlights.

Data Persistence: Local Markdown (.md) with YAML frontmatter + SQLite indexing.

📱 Optimization for Xiaomi Redmi Note 10 Pro
To ensure stability on MIUI 14, the app implements:

Load-Run-Unload Logic: The Whisper model is loaded into RAM only during transcription and purged immediately after to prevent system-level process killing.

Foreground Service: All transcription tasks run as high-priority services to bypass aggressive MIUI battery management.

Scoped Storage: Full integration with the Android Storage Access Framework (SAF) for persistent folder permissions.

📂 Directory Structure
The app operates within a user-defined folder (e.g., /Documents/CocoonGlass/) to maintain 100% data portability.

Plaintext
/CocoonGlass/
├── models/             # Place .bin Whisper models here (Tiny, Base, Small, Medium)
├── notes/              # Organized by categories (Folders)
│   ├── Work/           # Example Category
│   │   └── note_001.md # Transcribed text + YAML metadata
│   └── Ideas/
├── cache/              # Temporary .wav captures
└── index.db            # SQLite database for fast local search
📝 Markdown Format
Every note is stored as a portable Markdown file with the following header:

Markdown
---
id: [UUID]
title: [Auto-generated or Manual]
created_at: YYYY-MM-DD HH:MM:SS
updated_at: YYYY-MM-DD HH:MM:SS
model: whisper-medium-q5_0
language: ru/en
category: [Category Name]
---

# Transcription
The actual text content starts here...
🚀 Getting Started
Prerequisites
Python 3.10+

Buildozer (for Android APK packaging)

Whisper.cpp Binaries: Compiled for arm64-v8a.

Installation
Clone the repository.

Download your preferred Whisper GGML models.

Transfer the models to your phone's chosen directory.

Run the initial "System Check" within the app to grant MIUI-specific permissions:

Display pop-up windows while running in background.

Battery Saver -> No Restrictions.

Autostart -> Enabled.

🎨 UI Controls
Center Orb: Tap to record. The liquid pulses based on audio input.

Drag & Drop: Pull the Orb to a "Category Node" to categorize before transcription.

Automatic Pop: Once transcription is complete, the note "condenses" from steam into clear text on a glass card automatically.

Status: Under Active Development

Target Device: Xiaomi Redmi Note 10 Pro (Sweet)

OS: MIUI 14 / Android 13+
