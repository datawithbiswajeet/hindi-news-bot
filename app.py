import os
import telebot
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import random
import time

# 🔑 DIRECT CREDENTIALS
BOT_TOKEN = "7955308006:AAEY4c6OGIwYjmj6vuge5Dyf0g2OOiy_0TQ"
GEMINI_API_KEY = "AIzaSyDazMYKfcb9bk4KM9Zy9ogFi8lGUqO0WnY"

class FinalHindiNewsBot:
    def __init__(self):
        # Use direct credentials (no parameters needed)
        self.bot = telebot.TeleBot(BOT_TOKEN)
        
        # Configure Gemini with correct model
        try:
            genai.configure(api_key=GEMINI_API_KEY)
            
            # Use the working model
            self.model_name = "models/gemini-2.0-flash"
            self.model = genai.GenerativeModel(self.model_name)
            
            # Test the model
            test_response = self.model.generate_content("Say 'API Connected' in Hindi")
            print(f"✅ Gemini AI Configured with: {self.model_name}")
            print(f"🧪 Test Response: {test_response.text}")
            
        except Exception as e:
            print(f"❌ Gemini Configuration Failed: {e}")
            raise e
        
        self.setup_handlers()

    def extract_article_content(self, url):
        """Extract clean article content"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            print(f"📡 Fetching: {url}")
            response = requests.get(url, headers=headers, timeout=25)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Get title
            title_tag = soup.find('title')
            original_title = title_tag.text.strip() if title_tag else "Latest News Update"
            print(f"📰 Original Title: {original_title}")
            
            # Get main content
            content = ""
            content_selectors = [
                'article',
                '.article-content',
                '.story-content',
                '.post-content',
                '.entry-content',
                '.article-body',
                '.story-details',
                '[role="main"]',
                'main',
                '.content',
                '.story'
            ]
            
            for selector in content_selectors:
                element = soup.select_one(selector)
                if element:
                    # Remove unwanted elements
                    for unwanted in element(['script', 'style', 'nav', 'header', 'footer', 'aside', 'button', 'a']):
                        unwanted.decompose()
                    content = element.get_text()
                    print(f"✅ Content found using: {selector}")
                    break
            
            if not content:
                body = soup.find('body')
                if body:
                    for unwanted in body(['script', 'style', 'nav', 'header', 'footer', 'aside', 'button', 'a']):
                        unwanted.decompose()
                    content = body.get_text()
                    print("✅ Content extracted from body")
            
            # Clean content
            content = ' '.join(content.split()[:800])
            print(f"✅ Content extracted: {len(content)} characters")
            
            return {
                'success': True,
                'original_title': original_title,
                'content': content
            }
            
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return {'success': False, 'error': str(e)}

    def generate_with_gemini(self, prompt):
        """Generate content using Gemini AI"""
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"❌ Gemini error: {e}")
            return None

    def create_custom_hindi_title(self, original_title, content):
        """Create creative Hindi title using Gemini"""
        prompt = f"""
        TASK: Create a COMPLETELY NEW and ORIGINAL Hindi news headline based on this news content.
        
        ORIGINAL ENGLISH TITLE: "{original_title}"
        
        NEWS CONTEXT: {content[:400]}
        
        IMPORTANT INSTRUCTIONS:
        1. DO NOT directly translate the original title
        2. Create a BRAND NEW Hindi headline that captures the essence of the news
        3. Make it catchy, attention-grabbing like Indian newspaper headlines
        4. Use dramatic but appropriate Hindi language
        5. Maximum 8-10 words
        6. Make it sound like a breaking news headline
        7. OUTPUT ONLY THE HINDI HEADLINE, NOTHING ELSE
        
        Examples of good custom headlines:
        - "दिल्ली में भूकंप के हल्के झटके, लोगों में दहशत"
        - "सरकार का ऐलान: पेट्रोल-डीजल के दामों में बदलाव"
        - "मौसम विभाग का अलर्ट: उत्तर भारत में बारिश का कहर"
        - "क्रिकेट विश्व कप: टीम इंडिया की शानदार जीत"
        
        Now create a completely new Hindi headline for this news:
        """
        
        hindi_title = self.generate_with_gemini(prompt)
        if hindi_title:
            # Clean the response
            hindi_title = hindi_title.replace('"', '').strip()
            return hindi_title
        else:
            # Fallback creative titles
            fallback_titles = [
                "ताजा खबर: महत्वपूर्ण अपडेट जारी",
                "ब्रेकिंग न्यूज: नई जानकारी सामने",
                "एक्सक्लूसिव: आज की बड़ी खबर"
            ]
            return random.choice(fallback_titles)

    def get_exact_english_translation(self, hindi_title):
        """Get exact English translation of Hindi title"""
        prompt = f"""
        TASK: Translate this Hindi news headline to English EXACTLY as it is.
        
        HINDI HEADLINE: "{hindi_title}"
        
        IMPORTANT:
        1. Translate word-to-word exactly
        2. DO NOT improve grammar or make it sound better
        3. Keep the same sentence structure and meaning
        4. Preserve the dramatic tone
        5. OUTPUT ONLY THE ENGLISH TRANSLATION, NOTHING ELSE
        
        Example:
        Input: "दिल्ली में भूकंप के हल्के झटके, लोगों में दहशत"
        Output: "Delhi in earthquake light shocks, people in panic"
        
        Now translate this exactly:
        """
        
        english_title = self.generate_with_gemini(prompt)
        if english_title:
            english_title = english_title.replace('"', '').strip()
            return english_title
        else:
            return "Latest News Update"

    def create_hindi_news_content(self, original_title, content):
        """Create ORIGINAL Hindi news content using multiple sources approach"""
        prompt = f"""
        TASK: Write a COMPLETE and ORIGINAL Hindi news article based on the given information.
        
        ORIGINAL NEWS TITLE: "{original_title}"
        NEWS CONTENT: {content[:600]}
        
        IMPORTANT INSTRUCTIONS:
        1. Write a COMPLETE news article in Hindi (250-300 words)
        2. DO NOT copy sentences from the original content
        3. Create ORIGINAL content in your own words
        4. Write like a professional Hindi news reporter
        5. Cover all important points from the news
        6. Include: introduction, main events, consequences, reactions, future implications
        7. Make it engaging and informative
        8. Use proper Hindi journalism style
        9. OUTPUT ONLY THE HINDI NEWS CONTENT, NOTHING ELSE
        
        Write as if you're reporting this news for a Hindi newspaper:
        """
        
        hindi_content = self.generate_with_gemini(prompt)
        return hindi_content if hindi_content else "विस्तृत खबर तैयार नहीं हो सकी। कृपया मूल लिंक देखें।"

    def generate_seo_tags(self, hindi_title, english_title, content):
        """Generate relevant SEO tags"""
        prompt = f"""
        TASK: Generate SEO tags for this news article.
        
        HINDI TITLE: {hindi_title}
        ENGLISH TITLE: {english_title}
        CONTEXT: {content[:200]}
        
        Requirements:
        1. Generate 8-10 relevant SEO tags in English
        2. Include location names, topics, key entities
        3. Make them search-engine friendly
        4. Comma-separated format
        5. OUTPUT ONLY THE TAGS, NOTHING ELSE
        
        Example: india news, delhi earthquake, breaking news, latest updates, seismic activity
        
        Generate tags for this news:
        """
        
        seo_tags = self.generate_with_gemini(prompt)
        return seo_tags if seo_tags else "news, india, latest, update, breaking"

    def process_news(self, url):
        """Main processing function with Gemini AI"""
        try:
            print(f"🔄 Processing: {url}")
            
            # Extract article
            article_data = self.extract_article_content(url)
            if not article_data['success']:
                return {'success': False, 'error': article_data['error']}
            
            # Step 1: Create CUSTOM Hindi title (not from Python file)
            print("🤖 Generating CUSTOM Hindi title...")
            hindi_title = self.create_custom_hindi_title(
                article_data['original_title'], 
                article_data['content']
            )
            print(f"🇮🇳 Custom Hindi Title: {hindi_title}")
            
            # Step 2: Get exact English translation
            print("🔄 Getting exact English translation...")
            english_title = self.get_exact_english_translation(hindi_title)
            print(f"🇺🇸 Exact English Title: {english_title}")
            
            # Step 3: Create COMPLETE Hindi news content
            print("📝 Creating original Hindi news content...")
            hindi_content = self.create_hindi_news_content(
                article_data['original_title'],
                article_data['content']
            )
            print(f"✅ Hindi content created: {len(hindi_content)} chars")
            
            # Step 4: Generate SEO tags
            print("🏷️ Generating SEO tags...")
            seo_tags = self.generate_seo_tags(
                hindi_title, 
                english_title, 
                article_data['content']
            )
            print(f"📊 SEO Tags: {seo_tags}")
            
            return {
                'success': True,
                'hindi_title': hindi_title,
                'english_title': english_title,
                'hindi_content': hindi_content,
                'seo_tags': seo_tags,
                'original_url': url
            }
            
        except Exception as e:
            print(f"❌ Processing error: {e}")
            return {'success': False, 'error': str(e)}

    def setup_handlers(self):
        """Setup bot handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = """
नमस्ते! पुजा जी 🙏
मैं आपका **Advanced Hindi News Creator Bot** हूं!

🤖 **AI-Powered Features:**
• कस्टम हिंदी हेडलाइन (ओरिजिनल)
• एक्सैक्ट इंग्लिश ट्रांसलेशन  
• कंप्लीट हिंदी न्यूज कंटेंट (कॉपी नहीं)
• ऑटो SEO टैग्स

🔗 **बस किसी भी न्यूज लिंक भेजें!**

⚡ **आउटपुट फॉर्मेट:**
1. हिंदी टाइटल
2. इंग्लिश टाइटल  
3. हिंदी न्यूज कंटेंट
4. SEO टैग्स
            """
            self.bot.reply_to(message, welcome_text)

        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            user_url = message.text.strip()
            
            if not user_url.startswith(('http://', 'https://')):
                self.bot.reply_to(message, "❌ कृपया वैध URL भेजें (http:// या https:// के साथ)")
                return
            
            # Send processing message
            processing_msg = self.bot.reply_to(message, "🤖 AI प्रोसेसिंग शुरू... (20-30 सेकंड लग सकते हैं)")
            
            try:
                result = self.process_news(user_url)
                
                if not result['success']:
                    self.bot.edit_message_text(
                        chat_id=message.chat.id,
                        message_id=processing_msg.message_id,
                        text="❌ इस लिंक को प्रोसेस नहीं कर पाया। कृपया दूसरा न्यूज लिंक ट्राई करें।"
                    )
                    return
                
                # SEPARATE OUTPUT FORMAT as requested
                response = f"""
📰 **1. हिंदी टाइटल:**
{result['hindi_title']}

🌐 **2. English Title:**
{result['english_title']}

📝 **3. हिंदी न्यूज कंटेंट:**
{result['hindi_content']}

🏷️ **4. SEO Tags:**
{result['seo_tags']}

🔗 **सोर्स लिंक:** {result['original_url']}

✅ **ओरिजिनल कंटेंट तैयार! आपके न्यूज ऐप के लिए परफेक्ट!**
                """
                
                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id,
                    text=response
                )
                
            except Exception as e:
                self.bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=processing_msg.message_id,
                    text=f"❌ प्रोसेसिंग में त्रुटि: {str(e)}"
                )

    def run(self):
        """Start the bot with auto-restart"""
        print("🚀 Advanced Hindi News Bot Started on Render!")
        print(f"🤖 Using model: {self.model_name}")
        print("☁️ Running 24/7 on Render Cloud!")
        print("📍 Bot will auto-restart if any error occurs")
        
        # Auto-restart for cloud reliability
        while True:
            try:
                self.bot.infinity_polling()
            except Exception as e:
                print(f"❌ Bot crashed: {e}")
                print("🔄 Restarting in 10 seconds...")
                time.sleep(10)

if __name__ == "__main__":
    print("🚀 Starting Advanced Hindi News Bot on Render...")
    try:
        bot = FinalHindiNewsBot()
        bot.run()
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
