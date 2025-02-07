# 🎭 YouTube & Google Reviews Sentiment Analyzer

> A Flask-based web application that fetches YouTube comments via the YouTube API, scrapes Google Maps reviews using web scraping, and performs sentiment analysis. The app includes a machine learning model with feature extraction and prediction components and features an interactive UI built with HTML and Element UI.

---

## 📌 Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Technologies Used](#technologies-used)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgments](#acknowledgments)

---

## 🚀 Introduction

The **YouTube & Google Reviews Sentiment Analyzer** is a Flask-powered web application that automates the process of:

- Fetching **YouTube comments** using the **YouTube API**.
- Scraping **Google Maps business reviews**.
- Performing **sentiment analysis** on fetched data.
- Using a **machine learning models** one of feature extraction & one of prediction components.
- Providing an intuitive **UI with HTML & Element UI**.

---

## 🌟 Features

✅ **Fetch YouTube comments** using the official **YouTube API**.  
✅ **Scrape Google Maps reviews** from Google Business listings.  
✅ **Sentiment analysis** of comments and reviews using NLP techniques.  
✅ **Machine Learning Model** for feature extraction and prediction.  
✅ **Modular Flask app** with blueprints for better scalability.  
✅ **Web-based UI** built with **HTML and Element UI**.  
✅ **Testing framework included** for validating functionalities.  

---

## 🛠️ Installation

### 1️⃣ Prerequisites

Ensure you have the following installed:

- **Python 3.x**
- **pip (Python package manager)**
- **Virtual Environment (optional but recommended)**
- **Flask** (installed via `requirements.txt`)
- **Google API Key** (for YouTube API access)

### 2️⃣ Clone the Repository

```bash
git clone https://github.com/thezohaibkhalid/Youtube-Comments-Sentimental-Analyser.git
cd Youtube-Comments-Sentimental-Analyser
```

### 3️⃣ Create and Activate a Virtual Environment (Optional)

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Set Up API Keys

- Obtain a **Google API Key** for YouTube Data API.
- Store the API key in a `.env` file:

```bash
YOUTUBE_API_KEY=your_youtube_api_key_here
```

---

## 🚀 Usage

### 1️⃣ Run the Flask Application

```bash
python app.py
```

### 2️⃣ Access the Web UI

Open your browser and visit:  
👉 **`http://127.0.0.1:5000/`**

### 3️⃣ Fetch YouTube Comments

- Enter the **YouTube video URL**.
- Click **Fetch Comments** to retrieve comments.

### 4️⃣ Scrape Google Maps Reviews

- Enter the **Google Business name or link**.
- Click **Scrape Reviews**.

### 5️⃣ Sentiment Analysis & Predictions

- The app will process the comments/reviews.
- Sentiment predictions will be displayed in real-time.

---

## 📂 Project Structure

```
📦 Youtube-Comments-Sentimental-Analyser
│── 📂 blueprints/             # Modular Flask blueprints for different features
│── 📂 config/                 # Configuration files
│── 📂 models/                 # ML Model (Feature Extraction & Predictions)
│── 📂 services/               # API integration & web scraping logic
│── 📂 static/                 # Static files (CSS, JS)
│── 📂 templates/              # HTML templates for UI
│── 📂 tests/                  # Unit tests for the application
│── 📂 utils/                  # Utility functions
│── .gitignore                 # Git ignore file
│── README.md                  # Project Documentation
│── app.py                     # Flask Application Entry Point
│── requirements.txt            # Python dependencies
```

### 📌 Key Folder Descriptions

- **`blueprints/`** → Organizes Flask routes into modular components.  
- **`config/`** → Contains configuration settings.  
- **`models/`** → Stores machine learning models for sentiment analysis.  
- **`services/`** → Handles API requests (YouTube API, web scraping).  
- **`static/`** → Contains CSS, JavaScript, and other static assets.  
- **`templates/`** → Stores HTML templates for the front-end UI.  
- **`tests/`** → Includes test cases for verifying functionality.  
- **`utils/`** → Contains utility functions for data processing.  

---

## 🛠️ Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Element UI
- **APIs**: YouTube Data API, Google Maps scraping
- **Machine Learning**: Sentiment Analysis (NLP-based)
- **Web Scraping**: BeautifulSoup, Selenium
- **Database (optional, if used)**: SQLite / PostgreSQL

---

## 🤝 Contributing

Contributions are welcome! 🎉 To contribute:

1. **Fork the repository**.
2. **Create a new branch** (`git checkout -b feature-branch`).
3. **Commit your changes** (`git commit -m "Add new feature"`).
4. **Push to your branch** (`git push origin feature-branch`).
5. **Create a Pull Request**.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for more details.

---

## 🙏 Acknowledgments

A big thank you to:

- **Google** for the **YouTube API**.
- **BeautifulSoup & Selenium** for web scraping.
- **Element UI** for an intuitive frontend design.
- Everyone who has contributed to this project! 🚀

---

🎯 **Happy Analyzing!** 🎯  
📬 Feel free to reach out for any questions or contributions!

---
