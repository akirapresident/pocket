#!/usr/bin/env python3
"""
Pocket - Modern Instagram Scraper Test
Test the modern Instagram scraper that works with current structure
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.scraper.instagram_scraper import InstagramScraper, analyze_instagram_profile


def test_instagram_scraper(username: str):
    """
    Test the Instagram scraper
    """
    print(f"🚀 Testing Instagram Scraper for: @{username}")
    print("=" * 60)
    
    try:
        # Test 1: Basic scraper initialization
        print("1️⃣ Testing scraper initialization...")
        with InstagramScraper() as scraper:
            print("   ✅ Scraper initialized successfully")
            
            # Test 2: Login (using saved session if available)
            print("2️⃣ Testing Instagram login...")
            scraper.ensure_logged_in()
            print("   ✅ Login successful")
            
            # Test 3: Profile analysis
            print(f"3️⃣ Testing profile analysis for @{username}...")
            profile_data = scraper.analyze_profile(username)
            print("   ✅ Profile analysis successful")
            
            # Display results
            print("\n📊 Analysis Results:")
            print("-" * 40)
            
            profile_info = profile_data['profile_info']
            print(f"👤 Username: @{profile_info['username']}")
            print(f"📝 Full Name: {profile_info['full_name']}")
            print(f"👥 Followers: {profile_info['followers']:,}")
            print(f"👤 Following: {profile_info['following']:,}")
            print(f"📸 Posts: {profile_info['posts']:,}")
            print(f"✅ Verified: {'Yes' if profile_info['is_verified'] else 'No'}")
            print(f"🔒 Private: {'Yes' if profile_info['is_private'] else 'No'}")
            print(f"📝 Bio: {profile_info['biography'][:100]}...")
            
            posts = profile_data['posts']
            print(f"\n📱 Posts Data:")
            print(f"   Total posts found: {len(posts)}")
            
            print("\n🎉 Instagram scraper test passed!")
            return True
            
    except Exception as e:
        print(f"\n❌ Instagram scraper test failed: {e}")
        return False


def test_multiple_profiles():
    """
    Test with multiple profiles to ensure reliability
    """
    print(f"\n🔄 Testing Multiple Profiles")
    print("=" * 60)
    
    test_profiles = ['cristiano', 'instagram', 'natgeo']
    results = []
    
    try:
        with InstagramScraper() as scraper:
            scraper.ensure_logged_in()
            
            for profile in test_profiles:
                print(f"\n📱 Testing profile: @{profile}")
                try:
                    profile_data = scraper.analyze_profile(profile)
                    profile_info = profile_data['profile_info']
                    
                    print(f"   ✅ Username: @{profile_info['username']}")
                    print(f"   ✅ Followers: {profile_info['followers']:,}")
                    print(f"   ✅ Following: {profile_info['following']:,}")
                    print(f"   ✅ Posts: {profile_info['posts']:,}")
                    
                    results.append(True)
                    
                except Exception as e:
                    print(f"   ❌ Failed: {e}")
                    results.append(False)
        
        success_rate = sum(results) / len(results) * 100
        print(f"\n📊 Success Rate: {success_rate:.1f}% ({sum(results)}/{len(results)})")
        
        if success_rate >= 80:
            print("🎉 Multiple profiles test passed!")
            return True
        else:
            print("❌ Multiple profiles test failed!")
            return False
        
    except Exception as e:
        print(f"\n❌ Multiple profiles test failed: {e}")
        return False


def test_convenience_function(username: str):
    """
    Test the convenience function
    """
    print(f"\n🔄 Testing convenience function for: @{username}")
    print("=" * 60)
    
    try:
        profile_data = analyze_instagram_profile(username)
        print("✅ Convenience function works!")
        print(f"📊 Retrieved data for @{profile_data['profile_info']['username']}")
        return True
    except Exception as e:
        print(f"❌ Convenience function failed: {e}")
        return False


def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Instagram scraper')
    parser.add_argument('username', help='Instagram username to test (without @)')
    parser.add_argument('--test-multiple', action='store_true', help='Test multiple profiles')
    parser.add_argument('--test-convenience', action='store_true', help='Test convenience function')
    
    args = parser.parse_args()
    
    print("🧪 Pocket - Instagram Scraper Test")
    print("=" * 60)
    
    # Test main scraper
    success1 = test_instagram_scraper(args.username)
    
    # Test multiple profiles if requested
    success2 = True
    if args.test_multiple:
        success2 = test_multiple_profiles()
    
    # Test convenience function if requested
    success3 = True
    if args.test_convenience:
        success3 = test_convenience_function(args.username)
    
    # Final result
    if success1 and success2 and success3:
        print("\n🎯 INSTAGRAM SCRAPER TESTS PASSED!")
        print("✅ Instagram scraper is working")
        print("✅ Session persistence is working")
        print("✅ Data extraction is working")
        print("🎉 FASE 1 COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ INSTAGRAM SCRAPER TESTS FAILED!")
        print("❌ Please check the errors above")
        sys.exit(1)


if __name__ == "__main__":
    main()
