# 🏰 Ainia Adventure Learning Stories

## AI-powered educational storytelling for children aged 5-9

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.49+-red.svg)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![uv](https://img.shields.io/badge/uv-package_manager-purple.svg)](https://github.com/astral-sh/uv)

> *Making learning magical, one story at a time* ✨

---

## 🎯 Overview

Ainia Adventure Learning Stories is an innovative AI-powered platform that creates personalized, multi-part adventure stories with embedded learning challenges for children. Each story adapts in real-time to your child's responses, featuring an intelligent difficulty system that grows with their abilities.

### ✨ Key Features

- **🎭 Three Magical Themes**: Dragons, Pirates, and Princesses
- **📚 Adaptive Learning**: Multi-question stories with difficulty adjustment based on performance
- **🎨 Creative Expression**: Interactive drawing canvas for children to illustrate their adventures
- **🎵 Audio Narration**: Text-to-speech functionality for immersive storytelling
- **🛡️ Safety First**: Comprehensive content validation and age-appropriate content
- **🎉 Child-Friendly Interface**: Colorful, engaging UI with celebrations and animations
- **👨‍👩‍👧‍👦 Parent Transparency**: Detailed progress tracking and educational insights
- **🧠 Smart Difficulty**: AI-powered adaptive system adjusts challenge level in real-time

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Jai-Dhiman/Ainia-Prototype.git
   cd Ania-Prototype
   ```

2. **Install dependencies with uv** (recommended)

   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Install project dependencies
   uv sync
   ```

   *Alternative with pip:*

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenAI API key:

   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. **Run the application**

   ```bash
   uv run streamlit run main.py
   ```

   *Or with pip:*

   ```bash
   streamlit run main.py
   ```

5. **Open your browser**

   Navigate to `http://localhost:8501` to experience the magic! 🎭

---

## 📖 How It Works

**Ainia** creates personalized, multi-part adventure stories that adapt to your child's learning level:

1. **Choose Your Adventure**: Select from Dragons, Pirates, or Princesses themes
2. **Personalized Story**: Enter your child's name and learning focus
3. **Interactive Journey**: Read 3-part stories with learning challenges embedded naturally
4. **Adaptive Learning**: Questions adjust difficulty based on your child's responses
5. **Creative Expression**: Draw scenes from your completed adventure
6. **Audio Experience**: Listen to stories with text-to-speech narration

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │     Python      │    │   OpenAI API    │
│   Frontend      │───▶│     Backend     │───▶│   Service       │
│                 │    │                 │    │                 │
│ • Theme Select  │    │ • Multi-Q Gen   │    │ • Story Parts   │
│ • Child Input   │    │ • Adaptive Sys  │    │ • Questions     │
│ • Drawing UI    │    │ • Safety Check  │    │ • Explanations  │
│ • Audio Player  │    │ • Progress Trk  │    │ • Content Safe  │
│ • Celebrations  │    │ • TTS Manager   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Core Components

- **`MultiQuestionStoryGenerator`**: Orchestrates multi-part story generation with adaptive difficulty
- **`AdaptiveDifficultyManager`**: Adjusts question difficulty based on child's performance
- **`StorySession`**: Manages story state, progress, and question results
- **`TextToSpeechManager`**: Provides audio narration using Google TTS
- **`DrawingCanvas`**: Interactive canvas for children to create artwork
- **`SafetyValidator`**: Ensures all content meets child safety standards

---

## 🎯 Learning Focuses

Choose from three learning areas that seamlessly integrate into your adventure:

| Learning Focus | Age Range | Skills Developed | Example Challenges |
|----------------|-----------|------------------|-------------------|
| **🔢 Counting & Addition** | 5-7 years | Basic math skills, number recognition | "Count the dragon eggs in the nest!" |
| **📚 Vocabulary** | 6-8 years | Word recognition, language expansion | "What word describes the pirate's brave action?" |
| **🧩 Problem Solving** | 7-9 years | Critical thinking, logical reasoning | "How should the princess solve this kingdom puzzle?" |

---

## 🧠 Adaptive Difficulty System

**Ainia** features an intelligent difficulty adjustment system that grows with your child:

### How It Works

- **📈 Smart Progression**: Questions automatically adjust based on previous answers
- **✅ Correct Answer**: Next question becomes slightly more challenging to encourage growth
- **❌ Incorrect Answer**: Next question becomes easier to build confidence and understanding
- **🎯 Perfect Balance**: System finds the optimal challenge level for each child

### Difficulty Levels

| Level | Indicator | Description | Example (Dragons Theme) |
|-------|-----------|-------------|-------------------------|
| 🟢 **Easy** | Green dot | Foundation building | "Count 1-5 dragon eggs" |
| 🟡 **Medium** | Yellow dot | Skill development | "Add 3 + 2 dragon treasures" |
| 🔴 **Hard** | Red dot | Advanced challenge | "Solve the dragon's riddle: 7 + 6" |

---

## 📁 Project Structure

```
Ainia-Prototype/
├── 📁 src/ainia/                    # Core application package
│   ├── 📁 apps/
│   │   └── app.py                   # Main Streamlit application
│   ├── 📁 core/                     # Core business logic
│   │   ├── multi_question_system.py # Multi-part story generation
│   │   ├── story_generator.py       # Base story generation
│   │   ├── adaptive_system.py       # Adaptive difficulty management
│   │   ├── learning_integrator.py   # Educational content integration
│   │   ├── emotion_branching.py     # Emotional response handling
│   │   └── prompt_builder.py        # AI prompt construction
│   ├── 📁 utils/                    # Utility modules
│   │   ├── safety_validator.py      # Content safety validation
│   │   └── progress_reporter.py     # Progress tracking
│   └── 📁 config/                   # Configuration files
├── 📁 examples/                     # Example stories and demos
├── 📁 notebooks/                    # Jupyter notebooks for analysis
├── 📁 scripts/                      # Utility scripts
├── 📁 tests/                        # Test suites
│   ├── 📁 unit/                     # Unit tests
│   ├── 📁 integration/              # Integration tests
│   └── 📁 performance/              # Performance tests
├── 📁 saved_artwork/                # Children's drawings (auto-created)
├── main.py                          # Application entry point
├── pyproject.toml                   # uv dependency configuration
├── .env.example                     # Environment variables template
└── README.md                        # This file
```

---

## 🛡️ Safety & Privacy

### Content Safety

- **Age-appropriate validation** for 5-9 year olds
- **Zero tolerance** for scary, violent, or inappropriate content
- **Positive messaging** with growth mindset encouragement
- **Inclusive representation** across all stories

### Privacy Protection

- **No personal data storage** beyond session state
- **API key security** with environment variable protection
- **Cache privacy** - child names excluded from cache keys
- **Transparent AI reasoning** for parent understanding

---

## 🎨 Creative Features

### Interactive Drawing Canvas

After completing your adventure, children can:

- **🖼️ Draw Their Favorite Scene**: Illustrate memorable moments from their story
- **🎨 Free-Form Creation**: Use digital brushes and colors to express creativity
- **💾 Save Artwork**: Automatically saves drawings with child's name and adventure theme
- **🌟 Celebrate Achievement**: Artwork becomes a lasting memento of their learning journey

### Text-to-Speech Narration

- **🎵 Listen Mode**: Every story part can be read aloud with natural-sounding voices
- **🔊 On-Demand Audio**: Click to hear individual story sections
- **👂 Accessibility**: Supports different learning styles and reading abilities
- **🎭 Immersive Experience**: Makes stories come alive through audio narration

---

## 🎓 Educational Impact

### Learning Philosophy

Our "invisible learning" approach ensures educational content feels like a natural part of the adventure:

- **Contextual Embedding**: Math problems emerge from story events
- **Age-Appropriate Challenges**: Difficulty scales with child's development
- **Positive Reinforcement**: Celebrations and encouragement for all attempts
- **Parent Insights**: Transparent explanations of educational choices

### Learning Objectives

- **Math**: Counting, simple addition within age-appropriate ranges
- **Vocabulary**: Context-rich word learning with age-appropriate terms
- **Problem Solving**: Creative thinking and logical reasoning challenges

---

## 🔧 Development & Testing

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run specific test categories
uv run pytest tests/unit/          # Unit tests
uv run pytest tests/integration/   # Integration tests
uv run pytest tests/performance/   # Performance tests

# Run with enhanced features test
uv run python test_enhanced_features.py
```

### Development Setup

```bash
# Install development dependencies
uv add --dev pytest black ruff

# Format code
uv run black src/

# Lint code
uv run ruff check src/
```

---

## 👨‍👩‍👧‍👦 For Parents

### Progress Tracking

- **📊 Detailed Results**: View question-by-question performance after each story
- **🎯 Difficulty Insights**: Understand how the adaptive system adjusts for your child
- **📈 Learning Journey**: Track progression across multiple story sessions
- **🧠 Educational Rationale**: See explanations for each learning challenge

### Safety Features

- **🛡️ Content Validation**: All stories are automatically screened for age-appropriateness
- **🔒 Privacy Protection**: No personal data is stored beyond the current session
- **👀 Transparency**: Full visibility into AI decision-making and educational choices

---

**🎉 Ready to create magical learning adventures? Get started now!**

```bash
uv run streamlit run main.py
```

*Visit <http://localhost:8501> and watch the magic happen!* ✨

---

<div align="center">
  <strong>Ainia Adventure Learning Stories</strong><br>
  <em>Making learning magical, one story at a time</em> 🏰✨
</div>
