"""
Pocket - Instagram Scraper
Fase 1: Instagram scraper that works with current Instagram structure
"""

import time
import json
import os
import logging
import re
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class InstagramScraper:
    """
    Instagram scraper that works with current Instagram structure
    """
    
    def __init__(self):
        self.settings = get_settings()
        self.driver: Optional[webdriver.Chrome] = None
        self.is_logged_in = False
        self.session_file = "sessions/instagram_session.json"
        
    def __enter__(self):
        """Context manager entry"""
        self.init()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def init(self):
        """Initialize Selenium driver"""
        try:
            # Chrome options for stealth
            chrome_options = Options()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--disable-features=VizDisplayCompositor')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--disable-features=site-per-process')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-plugins')
            chrome_options.add_argument('--disable-images')
            chrome_options.add_argument('--disable-javascript')
            chrome_options.add_argument('--disable-default-apps')
            chrome_options.add_argument('--disable-sync')
            chrome_options.add_argument('--disable-translate')
            chrome_options.add_argument('--hide-scrollbars')
            chrome_options.add_argument('--mute-audio')
            chrome_options.add_argument('--no-default-browser-check')
            chrome_options.add_argument('--no-pings')
            chrome_options.add_argument('--password-store=basic')
            chrome_options.add_argument('--use-mock-keychain')
            chrome_options.add_argument('--disable-background-timer-throttling')
            chrome_options.add_argument('--disable-backgrounding-occluded-windows')
            chrome_options.add_argument('--disable-renderer-backgrounding')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Disable automation indicators
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Create driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute stealth script
            self.driver.execute_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            logger.info("Instagram scraper initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Instagram scraper: {e}")
            raise
    
    def save_session(self):
        """Save current session"""
        try:
            os.makedirs("sessions", exist_ok=True)
            
            cookies = self.driver.get_cookies()
            localStorage = self.driver.execute_script("""
                var ls = {};
                for (var i = 0; i < localStorage.length; i++) {
                    var key = localStorage.key(i);
                    ls[key] = localStorage.getItem(key);
                }
                return ls;
            """)
            
            session_data = {
                'cookies': cookies,
                'localStorage': localStorage,
                'timestamp': time.time(),
                'url': self.driver.current_url
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f, indent=2)
            
            logger.info(f"Session saved to {self.session_file}")
            
        except Exception as e:
            logger.error(f"Failed to save session: {e}")
    
    def load_session(self):
        """Load saved session"""
        try:
            if not os.path.exists(self.session_file):
                return False
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            if time.time() - session_data['timestamp'] > 24 * 3600:
                return False
            
            self.driver.get('https://www.instagram.com/')
            time.sleep(2)
            
            for cookie in session_data['cookies']:
                try:
                    self.driver.add_cookie(cookie)
                except:
                    continue
            
            self.driver.refresh()
            time.sleep(3)
            
            for key, value in session_data['localStorage'].items():
                try:
                    self.driver.execute_script(f"localStorage.setItem('{key}', '{value}');")
                except:
                    continue
            
            current_url = self.driver.current_url
            if '/accounts/login/' not in current_url:
                self.is_logged_in = True
                logger.info("Session restored successfully")
                return True
            
            return False
                
        except Exception as e:
            logger.error(f"Failed to load session: {e}")
            return False
    
    def login(self, username: str = None, password: str = None):
        """Login to Instagram"""
        username = username or self.settings.instagram_username
        password = password or self.settings.instagram_password
        
        if not username or not password:
            raise ValueError("Instagram credentials not provided")
        
        try:
            logger.info(f"Logging into Instagram with username: {username}")
            
            self.driver.get('https://www.instagram.com/')
            time.sleep(3)
            
            try:
                login_link = self.driver.find_element(By.CSS_SELECTOR, 'a[href="/accounts/login/"]')
                login_link.click()
                time.sleep(3)
            except:
                self.driver.get('https://www.instagram.com/accounts/login/')
                time.sleep(3)
            
            wait = WebDriverWait(self.driver, 10)
            username_field = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="username"]')))
            password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
            
            username_field.click()
            time.sleep(0.5)
            username_field.clear()
            time.sleep(0.5)
            username_field.send_keys(username)
            time.sleep(1)
            
            password_field.click()
            time.sleep(0.5)
            password_field.clear()
            time.sleep(0.5)
            password_field.send_keys(password)
            time.sleep(1)
            
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            submit_button.click()
            
            time.sleep(5)
            
            current_url = self.driver.current_url
            if '/accounts/login/' in current_url:
                raise Exception("Login failed - still on login page")
            
            self.is_logged_in = True
            logger.info("Successfully logged into Instagram")
            self.save_session()
            
        except Exception as e:
            logger.error(f"Login failed: {e}")
            raise
    
    def ensure_logged_in(self, username: str = None, password: str = None):
        """Ensure user is logged in"""
        if self.is_logged_in:
            return
        
        if self.load_session():
            return
        
        self.login(username, password)
    
    def analyze_profile(self, username: str) -> Dict[str, Any]:
        """
        Analyze Instagram profile using modern extraction methods
        """
        self.ensure_logged_in()
        
        try:
            logger.info(f"Analyzing profile: {username}")
            
            profile_url = f"https://www.instagram.com/{username}/"
            self.driver.get(profile_url)
            time.sleep(5)
            
            # Method 1: Try to extract from meta tags
            profile_data = self._extract_from_meta_tags()
            if profile_data:
                logger.info("Successfully extracted data from meta tags")
                return profile_data
            
            # Method 2: Try to extract from page content
            profile_data = self._extract_from_page_content()
            if profile_data:
                logger.info("Successfully extracted data from page content")
                return profile_data
            
            # Method 3: Try to extract from JavaScript variables
            profile_data = self._extract_from_js_variables()
            if profile_data:
                logger.info("Successfully extracted data from JavaScript variables")
                return profile_data
            
            raise Exception("Could not extract profile data using any method")
            
        except Exception as e:
            logger.error(f"Failed to analyze profile {username}: {e}")
            raise
    
    def _extract_from_meta_tags(self) -> Optional[Dict[str, Any]]:
        """Extract profile data from meta tags"""
        try:
            meta_tags = self.driver.find_elements(By.CSS_SELECTOR, "meta")
            
            profile_data = {
                'username': '',
                'full_name': '',
                'biography': '',
                'followers': 0,
                'following': 0,
                'posts': 0,
                'is_verified': False,
                'is_private': False,
                'profile_pic_url': '',
                'external_url': ''
            }
            
            for meta in meta_tags:
                property_attr = meta.get_attribute("property")
                content = meta.get_attribute("content")
                
                if property_attr == "og:title" and content:
                    # Extract username and full name from title
                    # Format: "Full Name (@username) • Instagram photos and videos"
                    match = re.match(r'^(.+?)\s*\(@([^)]+)\)', content)
                    if match:
                        profile_data['full_name'] = match.group(1).strip()
                        profile_data['username'] = match.group(2).strip()
                
                elif property_attr == "og:description" and content:
                    profile_data['biography'] = content
                    
                    # Extract stats from description
                    # Format: "664M Followers, 623 Following, 3,932 Posts - See Instagram photos..."
                    followers_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+Followers?', content)
                    if followers_match:
                        profile_data['followers'] = self._parse_number(followers_match.group(1))
                    
                    following_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+Following', content)
                    if following_match:
                        profile_data['following'] = self._parse_number(following_match.group(1))
                    
                    posts_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+Posts?', content)
                    if posts_match:
                        profile_data['posts'] = self._parse_number(posts_match.group(1))
                
                elif property_attr == "og:image" and content:
                    profile_data['profile_pic_url'] = content
            
            # Check if we got meaningful data
            if profile_data['username'] and profile_data['full_name']:
                return {
                    'profile_info': profile_data,
                    'posts': [],  # Meta tags don't contain post data
                    'total_posts': 0,
                    'scraped_at': time.time()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract from meta tags: {e}")
            return None
    
    def _extract_from_page_content(self) -> Optional[Dict[str, Any]]:
        """Extract profile data from page content"""
        try:
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            
            profile_data = {
                'username': '',
                'full_name': '',
                'biography': '',
                'followers': 0,
                'following': 0,
                'posts': 0,
                'is_verified': False,
                'is_private': False,
                'profile_pic_url': '',
                'external_url': ''
            }
            
            # Check if account is private
            if "This account is private" in page_text:
                profile_data['is_private'] = True
            
            # Extract stats from page text
            followers_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+followers?', page_text, re.IGNORECASE)
            if followers_match:
                profile_data['followers'] = self._parse_number(followers_match.group(1))
            
            following_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+following', page_text, re.IGNORECASE)
            if following_match:
                profile_data['following'] = self._parse_number(following_match.group(1))
            
            posts_match = re.search(r'(\d+(?:\.\d+)?[KMB]?)\s+posts?', page_text, re.IGNORECASE)
            if posts_match:
                profile_data['posts'] = self._parse_number(posts_match.group(1))
            
            # Check if verified
            if "Verified" in page_text:
                profile_data['is_verified'] = True
            
            return {
                'profile_info': profile_data,
                'posts': [],
                'total_posts': 0,
                'scraped_at': time.time()
            }
            
        except Exception as e:
            logger.error(f"Failed to extract from page content: {e}")
            return None
    
    def _extract_from_js_variables(self) -> Optional[Dict[str, Any]]:
        """Extract profile data from JavaScript variables"""
        try:
            # Look for any JavaScript variables that might contain profile data
            page_source = self.driver.page_source
            
            # Look for patterns like "username": "cristiano"
            username_match = re.search(r'"username":\s*"([^"]+)"', page_source)
            if username_match:
                username = username_match.group(1)
                
                profile_data = {
                    'username': username,
                    'full_name': '',
                    'biography': '',
                    'followers': 0,
                    'following': 0,
                    'posts': 0,
                    'is_verified': False,
                    'is_private': False,
                    'profile_pic_url': '',
                    'external_url': ''
                }
                
                # Try to find other data
                full_name_match = re.search(r'"full_name":\s*"([^"]+)"', page_source)
                if full_name_match:
                    profile_data['full_name'] = full_name_match.group(1)
                
                followers_match = re.search(r'"followers":\s*(\d+)', page_source)
                if followers_match:
                    profile_data['followers'] = int(followers_match.group(1))
                
                following_match = re.search(r'"following":\s*(\d+)', page_source)
                if following_match:
                    profile_data['following'] = int(following_match.group(1))
                
                posts_match = re.search(r'"posts":\s*(\d+)', page_source)
                if posts_match:
                    profile_data['posts'] = int(posts_match.group(1))
                
                return {
                    'profile_info': profile_data,
                    'posts': [],
                    'total_posts': 0,
                    'scraped_at': time.time()
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract from JS variables: {e}")
            return None
    
    def _parse_number(self, number_str: str) -> int:
        """Parse number string like '664M', '1.2K', '1234' to integer"""
        try:
            number_str = number_str.upper().replace(',', '')
            
            if 'K' in number_str:
                return int(float(number_str.replace('K', '')) * 1000)
            elif 'M' in number_str:
                return int(float(number_str.replace('M', '')) * 1000000)
            elif 'B' in number_str:
                return int(float(number_str.replace('B', '')) * 1000000000)
            else:
                return int(float(number_str))
        except:
            return 0
    
    def close(self):
        """Close driver and cleanup"""
        try:
            if self.driver:
                self.driver.quit()
            logger.info("Instagram scraper closed successfully")
        except Exception as e:
            logger.error(f"Error closing Instagram scraper: {e}")


# Convenience function
def analyze_instagram_profile(username: str, instagram_username: str = None, instagram_password: str = None) -> Dict[str, Any]:
    """
    Convenience function to analyze an Instagram profile
    """
    with InstagramScraper() as scraper:
        scraper.ensure_logged_in(instagram_username, instagram_password)
        return scraper.analyze_profile(username)
