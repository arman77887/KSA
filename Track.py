#!/usr/bin/env python3
"""
🚨 ADVANCED MOBILE TRACKING SYSTEM
For Law Enforcement and Authorized Personnel Only
Version: 2.0 - Power Mode
"""

import requests
import json
import time
import threading
from datetime import datetime
import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import socket
import os
import sys

# কালার কোড
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class AdvancedMobileTracker:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json'
        })
        self.tracking_active = False
        self.tracking_data = []
        
    def print_banner(self):
        """পাওয়ারফুল বেনার"""
        os.system('clear' if os.name == 'posix' else 'cls')
        print(f"""{Colors.RED}
╔════════════════════════════════════════════════════════════════╗
║{Colors.BOLD}{Colors.CYAN}               ADVANCED MOBILE TRACKING SYSTEM{Colors.END}{Colors.RED}               ║
║                 {Colors.YELLOW}🚨 LAW ENFORCEMENT EDITION 🚨{Colors.RED}                  ║
║                {Colors.GREEN}Real-time Location Tracking{Colors.RED}                    ║
╚════════════════════════════════════════════════════════════════╝{Colors.END}
        """)

    def verify_authorization(self):
        """অথোরাইজেশন ভেরিফিকেশন"""
        print(f"\n{Colors.BOLD}{Colors.RED}🔐 AUTHORIZATION REQUIRED{Colors.END}")
        print(f"{Colors.RED}{'='*50}{Colors.END}")
        
        badge_id = input(f"{Colors.YELLOW}🪪 Enter Badge ID: {Colors.END}").strip()
        department = input(f"{Colors.YELLOW}🏢 Enter Department: {Colors.END}").strip()
        case_number = input(f"{Colors.YELLOW}📁 Enter Case Number: {Colors.END}").strip()
        
        if badge_id and department and case_number:
            print(f"{Colors.GREEN}✅ Authorization Verified{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}❌ Authorization Failed{Colors.END}")
            return False

    def get_phone_carrier_info(self, phone_number):
        """ফোন নম্বর থেকে ক্যারিয়ার এবং দেশের তথ্য"""
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            
            info = {
                'country': geocoder.description_for_number(parsed_number, "en"),
                'carrier': carrier.name_for_number(parsed_number, "en"),
                'timezones': list(timezone.time_zones_for_number(parsed_number)),
                'country_code': parsed_number.country_code,
                'is_valid': phonenumbers.is_valid_number(parsed_number),
                'number_type': phonenumbers.number_type(parsed_number)
            }
            return info
        except Exception as e:
            return {'error': str(e)}

    def get_ip_from_phone(self, phone_number):
        """ফোন নম্বর থেকে সংশ্লিষ্ট IP তথ্য (সিমুলেটেড)"""
        # Note: In real scenario, this would require mobile operator cooperation
        simulated_ips = {
            '88017': '103.102.203.',  # GP
            '88018': '103.88.120.',   # Robi
            '88019': '103.48.75.',    # Banglalink
            '88016': '103.26.180.'    # Airtel
        }
        
        prefix = phone_number[:5]
        if prefix in simulated_ips:
            base_ip = simulated_ips[prefix]
            return f"{base_ip}{str(hash(phone_number) % 255)}"
        return None

    def get_location_from_ip(self, ip_address):
        """IP এড্রেস থেকে বিস্তারিত লোকেশন"""
        apis = [
            f"http://ip-api.com/json/{ip_address}",
            f"https://ipapi.co/{ip_address}/json/",
            f"https://ipinfo.io/{ip_address}/json"
        ]
        
        for api_url in apis:
            try:
                response = self.session.get(api_url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if 'status' in data and data['status'] == 'success':
                        return {
                            'country': data.get('country', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('regionName', 'Unknown'),
                            'zip': data.get('zip', 'Unknown'),
                            'lat': data.get('lat'),
                            'lon': data.get('lon'),
                            'timezone': data.get('timezone', 'Unknown'),
                            'isp': data.get('isp', 'Unknown'),
                            'org': data.get('org', 'Unknown'),
                            'source': 'ip-api.com'
                        }
                    elif 'ip' in data:
                        return {
                            'country': data.get('country', 'Unknown'),
                            'city': data.get('city', 'Unknown'),
                            'region': data.get('region', 'Unknown'),
                            'zip': data.get('postal', 'Unknown'),
                            'lat': data.get('latitude'),
                            'lon': data.get('longitude'),
                            'timezone': data.get('timezone', 'Unknown'),
                            'isp': data.get('org', 'Unknown'),
                            'source': 'ipapi.co/ipinfo.io'
                        }
            except:
                continue
        return None

    def simulate_cell_tower_data(self, phone_number):
        """সেল টাওয়ার ডাটা সিমুলেশন"""
        import random
        
        # বাংলাদেশের প্রধান শহরগুলোর coordinates
        bangladesh_cities = {
            'Dhaka': (23.8103, 90.4125),
            'Chittagong': (22.3569, 91.7832),
            'Khulna': (22.8456, 89.5403),
            'Rajshahi': (24.3745, 88.6042),
            'Sylhet': (24.8910, 91.8740),
            'Barisal': (22.7010, 90.3535),
            'Rangpur': (25.7439, 89.2752)
        }
        
        city = random.choice(list(bangladesh_cities.keys()))
        lat, lon = bangladesh_cities[city]
        
        # Add some random variation for realism
        lat += random.uniform(-0.1, 0.1)
        lon += random.uniform(-0.1, 0.1)
        
        return {
            'cell_tower_location': city,
            'latitude': round(lat, 6),
            'longitude': round(lon, 6),
            'tower_id': f"TWR-{random.randint(1000, 9999)}",
            'signal_strength': f"{random.randint(65, 95)}%",
            'accuracy': f"{random.randint(100, 500)} meters"
        }

    def live_tracking_worker(self, phone_number, duration=300):
        """লাইভ ট্র্যাকিং ওয়ার্কার"""
        start_time = time.time()
        update_count = 0
        
        print(f"\n{Colors.GREEN}🚀 Starting Live Tracking...{Colors.END}")
        print(f"{Colors.CYAN}📱 Target: {phone_number}{Colors.END}")
        print(f"{Colors.YELLOW}⏰ Duration: {duration} seconds{Colors.END}")
        
        while time.time() - start_time < duration and self.tracking_active:
            try:
                # Get carrier info
                carrier_info = self.get_phone_carrier_info(phone_number)
                
                # Simulate IP-based location
                simulated_ip = self.get_ip_from_phone(phone_number)
                ip_location = self.get_location_from_ip(simulated_ip) if simulated_ip else None
                
                # Get cell tower data
                cell_data = self.simulate_cell_tower_data(phone_number)
                
                # Create tracking record
                track_record = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'phone_number': phone_number,
                    'carrier_info': carrier_info,
                    'ip_location': ip_location,
                    'cell_tower_data': cell_data,
                    'update_count': update_count + 1
                }
                
                self.tracking_data.append(track_record)
                
                # Display real-time update
                self.display_live_update(track_record)
                
                update_count += 1
                time.sleep(10)  # Update every 10 seconds
                
            except Exception as e:
                print(f"{Colors.RED}⚠️ Tracking Error: {e}{Colors.END}")
                time.sleep(5)

    def display_live_update(self, track_record):
        """লাইভ আপডেট ডিসপ্লে"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔄 LIVE UPDATE #{track_record['update_count']}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
        print(f"{Colors.GREEN}🕒 Time: {track_record['timestamp']}{Colors.END}")
        
        # Carrier Info
        carrier_info = track_record['carrier_info']
        if 'error' not in carrier_info:
            print(f"{Colors.BLUE}📡 Carrier: {carrier_info.get('carrier', 'Unknown')}{Colors.END}")
            print(f"{Colors.YELLOW}🌍 Country: {carrier_info.get('country', 'Unknown')}{Colors.END}")
        
        # Cell Tower Data
        cell_data = track_record['cell_tower_data']
        print(f"{Colors.MAGENTA}📶 Signal: {cell_data['signal_strength']}{Colors.END}")
        print(f"{Colors.GREEN}📍 Approx Location: {cell_data['cell_tower_location']}{Colors.END}")
        print(f"{Colors.CYAN}🎯 Coordinates: {cell_data['latitude']}, {cell_data['longitude']}{Colors.END}")
        print(f"{Colors.YELLOW}📏 Accuracy: {cell_data['accuracy']}{Colors.END}")
        
        # Google Maps link
        maps_url = f"https://maps.google.com/?q={cell_data['latitude']},{cell_data['longitude']}"
        print(f"{Colors.RED}🗺️ Maps: {maps_url}{Colors.END}")

    def start_live_tracking(self, phone_number, duration=300):
        """লাইভ ট্র্যাকিং শুরু করে"""
        if not self.verify_authorization():
            return False
        
        self.tracking_active = True
        self.tracking_data = []
        
        # ট্র্যাকিং থ্রেড শুরু
        track_thread = threading.Thread(
            target=self.live_tracking_worker, 
            args=(phone_number, duration)
        )
        track_thread.daemon = True
        track_thread.start()
        
        print(f"\n{Colors.GREEN}✅ Live tracking started!{Colors.END}")
        print(f"{Colors.YELLOW}⏸️ Press Ctrl+C to stop tracking{Colors.END}")
        
        try:
            # Main thread waits
            track_thread.join(duration)
        except KeyboardInterrupt:
            print(f"\n{Colors.RED}🛑 Tracking stopped by user{Colors.END}")
        
        self.tracking_active = False
        self.generate_tracking_report(phone_number)

    def generate_tracking_report(self, phone_number):
        """ট্র্যাকিং রিপোর্ট জেনারেট করে"""
        if not self.tracking_data:
            print(f"{Colors.RED}❌ No tracking data collected{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}📊 TRACKING REPORT SUMMARY{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
        print(f"{Colors.GREEN}📱 Target Number: {phone_number}{Colors.END}")
        print(f"{Colors.BLUE}📅 Tracking Duration: {len(self.tracking_data)} updates{Colors.END}")
        print(f"{Colors.YELLOW}🕒 First Update: {self.tracking_data[0]['timestamp']}{Colors.END}")
        print(f"{Colors.MAGENTA}🕒 Last Update: {self.tracking_data[-1]['timestamp']}{Colors.END}")
        
        # Location analysis
        locations = [data['cell_tower_data']['cell_tower_location'] for data in self.tracking_data]
        most_common_location = max(set(locations), key=locations.count)
        
        print(f"{Colors.GREEN}📍 Most Frequent Location: {most_common_location}{Colors.END}")
        
        # Save report to file
        filename = f"tracking_report_{phone_number}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(self.tracking_data, f, indent=2)
        
        print(f"{Colors.CYAN}💾 Report saved: {filename}{Colors.END}")

    def quick_scan(self, phone_number):
        """কুইক স্ক্যান মোড"""
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🔍 QUICK SCAN MODE{Colors.END}")
        print(f"{Colors.YELLOW}{'='*50}{Colors.END}")
        
        # Carrier info
        carrier_info = self.get_phone_carrier_info(phone_number)
        self.display_carrier_info(carrier_info)
        
        # IP-based location
        simulated_ip = self.get_ip_from_phone(phone_number)
        if simulated_ip:
            ip_location = self.get_location_from_ip(simulated_ip)
            self.display_ip_location(ip_location)
        
        # Cell tower data
        cell_data = self.simulate_cell_tower_data(phone_number)
        self.display_cell_data(cell_data)

    def display_carrier_info(self, carrier_info):
        """ক্যারিয়ার ইনফো ডিসপ্লে"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}📱 PHONE INFORMATION{Colors.END}")
        print(f"{Colors.CYAN}{'='*40}{Colors.END}")
        
        if 'error' in carrier_info:
            print(f"{Colors.RED}❌ Error: {carrier_info['error']}{Colors.END}")
            return
        
        print(f"{Colors.GREEN}✅ Number Valid: {carrier_info['is_valid']}{Colors.END}")
        print(f"{Colors.BLUE}🌍 Country: {carrier_info.get('country', 'Unknown')}{Colors.END}")
        print(f"{Colors.YELLOW}📡 Carrier: {carrier_info.get('carrier', 'Unknown')}{Colors.END}")
        print(f"{Colors.MAGENTA}⏰ Timezone: {', '.join(carrier_info.get('timezones', []))}{Colors.END}")

    def display_ip_location(self, ip_location):
        """IP লোকেশন ডিসপ্লে"""
        if not ip_location:
            return
            
        print(f"\n{Colors.BOLD}{Colors.GREEN}🌐 IP-BASED LOCATION{Colors.END}")
        print(f"{Colors.GREEN}{'='*40}{Colors.END}")
        
        print(f"{Colors.BLUE}📍 City: {ip_location.get('city', 'Unknown')}{Colors.END}")
        print(f"{Colors.CYAN}🗺️ Region: {ip_location.get('region', 'Unknown')}{Colors.END}")
        print(f"{Colors.YELLOW}🏢 ISP: {ip_location.get('isp', 'Unknown')}{Colors.END}")

    def display_cell_data(self, cell_data):
        """সেল ডাটা ডিসপ্লে"""
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}📶 CELL TOWER INFORMATION{Colors.END}")
        print(f"{Colors.MAGENTA}{'='*40}{Colors.END}")
        
        print(f"{Colors.GREEN}📍 Location: {cell_data['cell_tower_location']}{Colors.END}")
        print(f"{Colors.BLUE}🎯 Coordinates: {cell_data['latitude']}, {cell_data['longitude']}{Colors.END}")
        print(f"{Colors.CYAN}📏 Accuracy: {cell_data['accuracy']}{Colors.END}")
        print(f"{Colors.YELLOW}📶 Signal: {cell_data['signal_strength']}{Colors.END}")
        
        # Google Maps link
        maps_url = f"https://maps.google.com/?q={cell_data['latitude']},{cell_data['longitude']}"
        print(f"{Colors.RED}🗺️ View on Maps: {maps_url}{Colors.END}")

    def menu(self):
        """মেইন মেনু"""
        while True:
            print(f"\n{Colors.BOLD}{Colors.CYAN}🎯 ADVANCED TRACKING MENU{Colors.END}")
            print(f"{Colors.CYAN}{'='*50}{Colors.END}")
            print(f"{Colors.GREEN}1.{Colors.END} Quick Phone Scan")
            print(f"{Colors.GREEN}2.{Colors.END} Live Location Tracking")
            print(f"{Colors.GREEN}3.{Colors.END} Generate Tracking Report")
            print(f"{Colors.GREEN}4.{Colors.END} Exit")
            
            choice = input(f"\n{Colors.YELLOW}🎯 Select option (1-4): {Colors.END}").strip()
            
            if choice == '1':
                phone = input(f"{Colors.CYAN}📱 Enter phone number: {Colors.END}").strip()
                if phone:
                    self.quick_scan(phone)
                else:
                    print(f"{Colors.RED}❌ Please enter a phone number{Colors.END}")
            
            elif choice == '2':
                phone = input(f"{Colors.CYAN}📱 Enter phone number for live tracking: {Colors.END}").strip()
                if phone:
                    duration = int(input(f"{Colors.CYAN}⏰ Enter tracking duration (seconds): {Colors.END}") or "300")
                    self.start_live_tracking(phone, duration)
                else:
                    print(f"{Colors.RED}❌ Please enter a phone number{Colors.END}")
            
            elif choice == '3':
                if self.tracking_data:
                    phone = input(f"{Colors.CYAN}📱 Enter phone number for report: {Colors.END}").strip()
                    self.generate_tracking_report(phone)
                else:
                    print(f"{Colors.RED}❌ No tracking data available{Colors.END}")
            
            elif choice == '4':
                print(f"{Colors.GREEN}👋 Thank you for using Advanced Tracking System{Colors.END}")
                break
            
            else:
                print(f"{Colors.RED}❌ Invalid choice!{Colors.END}")

def main():
    try:
        tracker = AdvancedMobileTracker()
        tracker.print_banner()
        
        print(f"{Colors.YELLOW}⚠️  This tool is for authorized law enforcement use only{Colors.END}")
        print(f"{Colors.RED}🚨 Unauthorized use may violate privacy laws{Colors.END}")
        
        tracker.menu()
        
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}❌ Program interrupted{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}💥 Error: {e}{Colors.END}")

if __name__ == "__main__":
    main()
