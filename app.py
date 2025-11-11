import os
import telebot
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import random
import time

# 🔑 DIRECT CREDENTIALS (No environment variables)
BOT_TOKEN = "7955308006:AAEY4c6OGIwYjmj6vuge5Dyf0g2OOiy_0TQ"
GEMINI_API_KEY = "AIzaSyDazMYKfcb9bk4KM9Zy9ogFi8lGUqO0WnY"

class HindiNewsBot:
    def __init__(self):
        # Use direct credentials
        self.bot_token = BOT_TOKEN
        self.gemini_api_key = GEMINI_API_KEY
        
        self.bot = telebot.TeleBot(self.bot_token)
        
        # Configure Gemini
        try:
            genai.configure(api_key=self.gemini_api_key)
            self.model = genai.GenerativeModel('models/gemini-2.0-flash')
            print("✅ Gemini AI Configured Successfully!")
        except Exception as e:
            print(f"❌ Gemini Configuration Failed: {e}")
            raise e
        
        self.setup_handlers()

    def extract_article_content(self, url):
        """Extract clean article content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=25)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title_tag = soup.find('title')
            original_title = title_tag.text.strip() if title_tag else "Latest News"
            
            # Get content
            content = ""
            content_selectors = ['article', '.article-content', '.story-content', 'main']
            
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    content = element.get_text()
                    break
            
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text()
            
            content = ' '.join(content.split()[:500])
            return {'success': True, 'original_title': original_title, 'content': content}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def generate_with_gemini(self, prompt):
        """Generate content using Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except:
            return None

    def create_custom_hindi_title(self, original_title, content):
        """Create custom Hindi title"""
        prompt = f"Create Hindi news headline: {original_title}. Context: {content[:200]}. Output only Hindi."
        hindi_title = self.generate_with_gemini(prompt)
        return hindi_title if hindi_title else "ताजा खबर: अपडेट"

    def get_exact_english_translation(self, hindi_title):
        """Get exact English translation"""
        prompt = f"Translate exactly: {hindi_title}. Output only English."
        english_title = self.generate_with_gemini(prompt)
        return english_title if english_title else "Latest News"

    def create_hindi_news_content(self, original_title, content):
        """Create Hindi news content"""
        prompt = f"Write Hindi news: {original_title}. Content: {content[:300]}. Output only Hindi."
        hindi_content = self.generate_with_gemini(prompt)
        return hindi_content if hindi_content else "विस्तृत जानकारी उपलब्ध नहीं।"

    def generate_seo_tags(self, hindi_title):
        """Generate SEO tags"""
        prompt = f"Generate SEO tags for: {hindi_title}. Output comma-separated."
        seo_tags = self.generate_with_gemini(prompt)
        return seo_tags if seo_tags else "news, india, latest"

    def process_news(self, url):
        """Main processing function"""
        try:
            article_data = self.extract_article_content(url)
            if not article_data['success']:
                return {'success': False, 'error': article_data['error']}
            
            hindi_title = self.create_custom_hindi_title(article_data['original_title'], article_data['content'])
            english_title = self.get_exact_english_translation(hindi_title)
            hindi_content = self.create_hindi_news_content(article_data['original_title'], article_data['content'])
            seo_tags = self.generate_seo_tags(hindi_title)
            
            return {
                'success': True,
                'hindi_title': hindi_title,
                'english_title': english_title,
                'hindi_content': hindi_content,
                'seo_tags': seo_tags,
                'original_url': url
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def setup_handlers(self):
        """Setup bot handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = """
नमस्ते! पुजा जी 🙏
मैं आपका Hindi News Bot हूं!

🤖 AI Features:
• कस्टम हिंदी टाइटल
• इंग्लिश ट्रांसलेशन  
• हिंदी न्यूज कंटेंट
• SEO टैग्स

🔗 बस किसी भी न्यूज लिंक भेजें!
            """
            self.bot.reply_to(message, welcome_text)

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            url = message.text.strip()
            
            if not url.startswith(('http://', 'https://')):
                self.bot.reply_to(message, "❌ कृपया वैध URL भेजें")
                return
            
            msg = self.bot.reply_to(message, "🤖 प्रोसेसिंग शुरू...")
            
            try:
                result = self.process_news(url)
                
                if not result['success']:
                    self.bot.edit_message_text("❌ प्रोसेसिंग फेल हुई", message.chat.id, msg.message_id)
                    return
                
                response = f"""
📰 {result['hindi_title']}

🌐 {result['english_title']}

📝 {result['hindi_content']}

🏷️ {result['seo_tags']}

✅ तैयार!
                """
                self.bot.edit_message_text(response, message.chat.id, msg.message_id)
            except Exception as e:
                self.bot.edit_message_text("❌ त्रुटि हुई", message.chat.id, msg.message_id)

    def run(self):
        """Start the bot with auto-restart"""
        print("🚀 Hindi News Bot Started on Render!")
        print("✅ Using direct credentials")
        while True:
            try:
                self.bot.infinity_polling()
            except Exception as e:
                print(f"❌ Bot crashed: {e}")
                time.sleep(10)

if __name__ == "__main__":
    bot = HindiNewsBot()
    bot.run()