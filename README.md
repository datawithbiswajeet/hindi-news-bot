# 📰 AI Hindi News Summarizer Bot

<h1 align="center"><b>🤖 AI Hindi News Summarizer Bot</b></h1>

<p align="center">
  
[![Live Bot](https://img.shields.io/badge/Telegram-Live_Bot-blue?style=for-the-badge&logo=telegram)](https://t.me/pujahindinewsbot)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Gemini AI](https://img.shields.io/badge/Google_Gemini-AI_Model-4285F4?style=for-the-badge&logo=google&logoColor=white)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)]()
[![Render](https://img.shields.io/badge/Render-Deployment-46B3E6?style=for-the-badge&logo=render&logoColor=white)]()
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/datawithbiswajeet/hindi-news-bot)

</p>

---

## 🚀 Project Overview

An intelligent **AI-powered Telegram bot** that automatically processes any news article URL and generates **original Hindi content** with custom titles, exact English translations, and SEO-optimized tags using **Google Gemini AI**.

The bot transforms English news articles into **professional Hindi journalism** with:
- **Custom Hindi headlines** (not direct translations)
- **Exact English translations** 
- **Comprehensive Hindi articles**
- **SEO-optimized tags**

---

🔗 **Live Bot:** [@pujahindinewsbot](https://t.me/pujahindinewsbot)  

---

## ⚙️ Tech Architecture

## 💻 Tech Stack

| Layer | Technology Used |
|-------|-----------------|
| **AI Engine** | Google Gemini AI (Gemini 2.0 Flash) |
| **Backend Framework** | Python + pyTelegramBotAPI |
| **Web Scraping** | BeautifulSoup4 + Requests |
| **Hosting** | Render.com (24/7 Free Tier) |
| **API** | Telegram Bot API |
| **Content Processing** | Custom AI Prompts + NLP |

**Hosting & Deployment:**
- **Backend:** Render.com (Free 750 hours/month)
- **Bot Platform:** Telegram
- **Version Control:** GitHub

---

## 🎯 Key Features

### 🤖 **AI-Powered Content Generation**
- **Custom Hindi Titles** - AI-generated original headlines
- **Exact English Translations** - Word-to-word translation
- **Comprehensive Hindi Content** - Complete rewritten articles
- **Smart SEO Tags** - Automatically generated keywords

### 📊 **Output Format**
```
📰 1. हिंदी टाइटल:
[कस्टम AI-जेनरेटेड हेडलाइन]

🌐 2. English Title:
[एक्सैक्ट ट्रांसलेशन]

📝 3. हिंदी न्यूज कंटेंट:
[कंप्लीट ओरिजिनल आर्टिकल]

🏷️ 4. SEO Tags:
[रिलेवेंट कीवर्ड्स]
```

---

## 🔄 Workflow Process

### 1️⃣ **URL Input & Validation**
- User sends any news article URL to Telegram bot
- Bot validates URL format and accessibility

### 2️⃣ **Content Extraction**
```python
# Multi-strategy content extraction
content_selectors = [
    'article', '.article-content', 
    '.story-content', 'main', '[role="main"]'
]
```

### 3️⃣ **AI Processing Pipeline**
- **Step 1:** Generate custom Hindi title using Gemini AI
- **Step 2:** Create exact English translation
- **Step 3:** Rewrite complete article in Hindi
- **Step 4:** Generate relevant SEO tags

### 4️⃣ **Structured Output Delivery**
- Formats all components professionally
- Delivers back to user in Telegram

---

## 📁 Project Structure

```
hindi-news-bot/
├── app.py                 # Main bot application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── render.yaml           # Deployment configuration
```

### 🔧 **Core Components**

| File | Purpose |
|------|---------|
| `app.py` | Main bot logic and AI processing |
| `requirements.txt` | Python package dependencies |
| `render.yaml` | Cloud deployment configuration |

---

## 🎯 Use Cases

### 📱 **For News Applications**
- Automatic Hindi content generation
- SEO-optimized article creation
- Multi-language news distribution

### 📊 **For Content Creators**
- Quick news summarization
- Social media content creation
- Multi-platform publishing

### 🌐 **For Media Houses**
- Automated news translation
- Content localization
- Rapid publishing pipeline

---

## ⚡ Performance Metrics

- **Processing Time:** 20-30 seconds per article
- **Content Length:** 250-300 word articles
- **Supported Sites:** Most major news websites
- **Uptime:** 24/7 on Render cloud
- **AI Model:** Gemini 2.0 Flash (Latest)

---

## 🚀 Quick Start

### 🔗 **Live Bot Access**
Simply message: [@pujahindinewsbot](https://t.me/pujahindinewsbot) on Telegram

### 💻 **Local Development**
```bash
# 1. Clone repository
git clone https://github.com/datawithbiswajeet/hindi-news-bot.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set credentials in app.py
BOT_TOKEN = "your-bot-token"
GEMINI_API_KEY = "your-gemini-key"

# 4. Run the bot
python app.py
```

### ☁️ **Cloud Deployment**
1. Fork the GitHub repository
2. Connect to [Render.com](https://render.com)
3. Set environment variables
4. Auto-deploy from GitHub

---

## 🛠️ Technical Implementation

### **AI Prompt Engineering**
```python
# Custom Hindi title generation
prompt = """
TASK: Create COMPLETELY NEW Hindi news headline
ORIGINAL: "{english_title}"
CONTEXT: {article_content}
OUTPUT: Only Hindi headline
"""
```

### **Content Extraction**
- Multi-selector strategy for robust scraping
- HTML cleaning and text processing
- Content length optimization

### **Error Handling**
- Auto-restart on crashes
- Comprehensive logging
- User-friendly error messages

---

## 📈 Business Value

### 💰 **Cost Effective**
- **Free hosting** on Render.com
- **Free AI credits** from Google
- **No infrastructure costs**

### ⚡ **Efficient**
- **20-30 second processing**
- **24/7 availability**
- **Scalable architecture**

### 🎯 **High Quality**
- **Professional Hindi journalism**
- **SEO-optimized output**
- **Original content generation**

---

## 🔮 Future Enhancements

- [ ] **Multi-language support** (Bengali, Tamil, etc.)
- [ ] **Image content generation**
- [ ] **Scheduled news summaries**
- [ ] **User preferences and history**
- [ ] **Advanced content analytics**
- [ ] **Multi-platform integration**

---

## ⚠️ Technical Notes

> The bot uses **Google Gemini AI 2.0 Flash** model for optimal performance and cost-effectiveness
> 
> **Web scraping** respects robots.txt and implements proper headers
> 
> **Error handling** ensures smooth user experience even with problematic URLs

---

## 👨‍💻 Author

**Developed by:** [Biswajeet | Data with Biswajeet](https://www.linkedin.com/in/datawithbiswajeet/)  
📧 **Email:** datawithbiswajeet@gmail.com  
💼 **LinkedIn:** [datawithbiswajeet](https://www.linkedin.com/in/datawithbiswajeet/)

---

## 🌐 Project Links

🔗 **Live Bot:** [@pujahindinewsbot](https://t.me/pujahindinewsbot)  
📁 **GitHub Repository:** [hindi-news-bot](https://github.com/datawithbiswajeet/hindi-news-bot)  
🐦 **Twitter:** [@datawithbiswaj](https://twitter.com/datawithbiswaj)

---

### ⭐ **If you find this project useful, don't forget to give it a star on GitHub!**

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ using Python, Gemini AI, and Telegram Bot API**

---

<p align="center">
  <i>"Transforming English news into professional Hindi journalism with AI"</i>
</p>
