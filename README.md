# Daily-News-Digest
🌍 A Python CLI tool that aggregates global news and analyzes daily sentiment using RSS feeds.



The project focuses on readability, pedagogy, and perspective when facing the constant flow of news, thanks to a simple yet effective rule-based sentiment analysis.

---

## ✨ Key Features


* 📰 **Multi-source news aggregation**
  Automatically fetches the latest headlines from well-known international media outlets (Le Monde, BBC, New York Times, The Guardian, Al Jazeera, France Info, TechCrunch, etc.).

* 📊 **Sentiment analysis**
  Each article is evaluated using positive and negative keyword dictionaries to compute an emotional impact score.

* 🧭 **Automatic topic categorization**
  Articles are classified into major themes: politics, economy, technology, science, health, environment, conflicts, disasters, culture, sports, and society.

* 🏆 **Top stories of the day**
  Highlights the most emotionally impactful articles, displaying full titles, sources, and visual indicators.

* 📈 **Global daily score**
  A synthetic score represents the overall tone of the day’s news (from very difficult to excellent), accompanied by a visual progress bar.

* 📊 **Detailed statistics**
  Topic distribution, sentiment breakdown, dominant keywords, extreme scores, and key metrics.

* 💡 **Daily perspective**
  A contextual message encouraging emotional distance and critical thinking depending on the news climate.

* 🎨 **Enhanced terminal interface**
  Colored output, emojis, dynamic layout, and automatic adaptation to terminal width.

---

## 🛠️ Tech Stack

* **Python 3**
* **Requests** – RSS feed retrieval
* **BeautifulSoup (bs4)** – XML parsing
* **Collections / Regex / Datetime** – analysis and statistics

No paid APIs are used: the project relies exclusively on public RSS feeds.

---

## 🚀 Usage

### Requirements

* Python 3.8+

### Run

* python news_digest.py

## 🎯 Project Goals

* Provide a **concise and intelligible overview** of global news
* Help users **gain emotional perspective** on headlines
* Demonstrate a **transparent, rule-based sentiment analysis** approach
* Offer a **pedagogical, extensible, and offline-friendly** tool

---

## 🔮 Possible Improvements

* NLP / machine learning–based sentiment analysis
* Daily score history and trend comparison
* Export formats (JSON, Markdown, HTML)
* Additional languages and news sources
* Quiet mode or short-summary mode

---

## ⚠️ Disclaimer

The sentiment analysis is keyword-based and does not replace human or contextual interpretation. Scores are indicative and designed to encourage reflection, not absolute judgment.

---

## 📄 License

Open-source project – free to use for personal, educational, or experimental purposes.

---

👤 *Project developed with the goal of making news more readable, more human, and less anxiety-inducing.*

<img width="944" height="473" alt="1" src="https://github.com/user-attachments/assets/4ea6036e-2f51-4f7c-b01e-e7b30801f7fc" />
<img width="937" height="458" alt="2" src="https://github.com/user-attachments/assets/5294dfb9-71fe-442d-9f6c-f3bc8aff0128" />

