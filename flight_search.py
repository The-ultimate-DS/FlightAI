import os
import requests
from datetime import datetime, timedelta
import json
from typing import Dict, List, Optional

class FlightSearcher:
    def __init__(self):
        # SerpAPI configuration
        self.api_key = os.getenv('SERPAPI_KEY', 'your_serpapi_key_here')
        self.base_url = "https://serpapi.com/search"
        self.default_departure_city = "Bangalore"
        self.default_departure_code = "BLR"
        
        # Search preferences (can be customized later)
        self.search_preferences = {
            'adults': 1,
            'children': 0,
            'infants': 0,
            'travel_class': 1,  # Economy by default
            'max_price': None,  # No price limit
            'preferred_airlines': [],  # No airline preference
            'deep_search': True  # More accurate results
        }
        
        # Comprehensive global airport code mapping
        self.city_codes = {
            # India
            'mumbai': 'BOM', 'bombay': 'BOM',
            'delhi': 'DEL', 'new delhi': 'DEL',
            'bangalore': 'BLR', 'bengaluru': 'BLR',
            'hyderabad': 'HYD', 'hyd': 'HYD',
            'chennai': 'MAA', 'madras': 'MAA',
            'kolkata': 'CCU', 'calcutta': 'CCU',
            'pune': 'PNQ', 'poona': 'PNQ',
            'goa': 'GOI', 'panaji': 'GOI',
            'ahmedabad': 'AMD', 'kochi': 'COK', 'cochin': 'COK',
            'trivandrum': 'TRV', 'thiruvananthapuram': 'TRV',
            'jaipur': 'JAI', 'udaipur': 'UDR', 'jodhpur': 'JDH',
            
            # Southeast Asia
            'singapore': 'SIN', 'bangkok': 'BKK', 'kuala lumpur': 'KUL',
            'jakarta': 'CGK', 'manila': 'MNL', 'ho chi minh': 'SGN',
            'hanoi': 'HAN', 'phnom penh': 'PNH', 'yangon': 'RGN',
            'denpasar': 'DPS', 'bali': 'DPS',
            
            # Middle East
            'dubai': 'DXB', 'abu dhabi': 'AUH', 'doha': 'DOH',
            'kuwait': 'KWI', 'riyadh': 'RUH', 'jeddah': 'JED',
            'muscat': 'MCT', 'tehran': 'IKA', 'baghdad': 'BGW',
            'beirut': 'BEY', 'amman': 'AMM', 'tel aviv': 'TLV',
            
            # Europe
            'london': 'LHR', 'heathrow': 'LHR', 'gatwick': 'LGW',
            'manchester': 'MAN', 'edinburgh': 'EDI', 'glasgow': 'GLA',
            'paris': 'CDG', 'charles de gaulle': 'CDG', 'orly': 'ORY',
            'amsterdam': 'AMS', 'frankfurt': 'FRA', 'munich': 'MUC',
            'berlin': 'BER', 'hamburg': 'HAM', 'cologne': 'CGN',
            'zurich': 'ZUR', 'geneva': 'GVA', 'basel': 'BSL',
            'madrid': 'MAD', 'barcelona': 'BCN', 'lisbon': 'LIS',
            'rome': 'FCO', 'fiumicino': 'FCO', 'milan': 'MXP',
            'venice': 'VCE', 'naples': 'NAP', 'vienna': 'VIE',
            'brussels': 'BRU', 'stockholm': 'ARN', 'copenhagen': 'CPH',
            'oslo': 'OSL', 'helsinki': 'HEL', 'reykjavik': 'KEF',
            'athens': 'ATH', 'istanbul': 'IST', 'ankara': 'ESB',
            'moscow': 'SVO', 'st petersburg': 'LED',
            
            # North America  
            'new york': 'JFK', 'jfk': 'JFK', 'laguardia': 'LGA', 'newark': 'EWR',
            'los angeles': 'LAX', 'san francisco': 'SFO', 'chicago': 'ORD',
            'miami': 'MIA', 'las vegas': 'LAS', 'seattle': 'SEA',
            'boston': 'BOS', 'washington': 'DCA', 'atlanta': 'ATL',
            'denver': 'DEN', 'phoenix': 'PHX', 'dallas': 'DFW',
            'houston': 'IAH', 'philadelphia': 'PHL', 'detroit': 'DTW',
            'toronto': 'YYZ', 'vancouver': 'YVR', 'montreal': 'YUL',
            'calgary': 'YYC', 'ottawa': 'YOW', 'winnipeg': 'YWG',
            'mexico city': 'MEX', 'cancun': 'CUN', 'guadalajara': 'GDL',
            
            # East Asia
            'tokyo': 'NRT', 'narita': 'NRT', 'haneda': 'HND',
            'osaka': 'KIX', 'kyoto': 'KIX', 'nagoya': 'NGO',
            'seoul': 'ICN', 'incheon': 'ICN', 'gimpo': 'GMP',
            'busan': 'PUS', 'beijing': 'PEK', 'capital': 'PEK',
            'shanghai': 'PVG', 'pudong': 'PVG', 'hongqiao': 'SHA',
            'guangzhou': 'CAN', 'shenzhen': 'SZX', 'chengdu': 'CTU',
            'hong kong': 'HKG', 'macau': 'MFM', 'taipei': 'TPE',
            'kaohsiung': 'KHH',
            
            # Oceania
            'sydney': 'SYD', 'melbourne': 'MEL', 'brisbane': 'BNE',
            'perth': 'PER', 'adelaide': 'ADL', 'darwin': 'DRW',
            'auckland': 'AKL', 'wellington': 'WLG', 'christchurch': 'CHC',
            'fiji': 'NAN', 'nadi': 'NAN',
            
            # Africa
            'cairo': 'CAI', 'casablanca': 'CMN', 'johannesburg': 'JNB',
            'cape town': 'CPT', 'nairobi': 'NBO', 'lagos': 'LOS',
            'addis ababa': 'ADD', 'tunis': 'TUN', 'algiers': 'ALG',
            
            # South America
            'sao paulo': 'GRU', 'rio de janeiro': 'GIG', 'brasilia': 'BSB',
            'buenos aires': 'EZE', 'lima': 'LIM', 'bogota': 'BOG',
            'santiago': 'SCL', 'caracas': 'CCS', 'quito': 'UIO'
        }
    
    def search_flights(self, travel_details: Dict[str, str]) -> Dict:
        """
        Search for flights using SerpAPI Google Flights
        """
        return self.search_flights_with_preferences(travel_details, {})
    
    def search_flights_with_preferences(self, travel_details: Dict[str, str], preferences: Dict = None) -> Dict:
        """
        Search for flights using SerpAPI Google Flights with separate outbound and return requests
        """
        try:
            # Check if it's a round trip
            departure_date = self._format_date(travel_details.get('departure', ''))
            return_date = self._format_date(travel_details.get('return', ''))
            is_round_trip = return_date and return_date != departure_date
            
            print(f"DEBUG: Trip type: {'Round-trip' if is_round_trip else 'One-way'}")
            
            if is_round_trip:
                # Make two separate API requests for round trip
                return self._search_round_trip_flights(travel_details, preferences)
            else:
                # Single request for one-way
                return self._search_one_way_flights(travel_details, preferences)
                
        except Exception as e:
            return {"error": f"Flight search failed: {str(e)}"}
    
    def _search_round_trip_flights(self, travel_details: Dict[str, str], preferences: Dict = None) -> Dict:
        """
        Search for round-trip flights with separate outbound and return requests
        """
        try:
            print("DEBUG: Making separate outbound and return flight requests...")
            
            # Search outbound flights
            outbound_result = self._search_one_way_flights(travel_details, preferences, flight_type="outbound")
            
            # Search return flights (reverse the route)
            return_travel_details = travel_details.copy()
            return_travel_details['departure'] = travel_details.get('return', '')  # Return date
            
            # Fix: Properly handle empty from_location by defaulting to Bangalore
            origin_location = preferences.get('from_location', 'Bangalore')
            if not origin_location or not origin_location.strip():
                origin_location = 'Bangalore'
            return_travel_details['destination'] = origin_location.lower()  # Going back to origin
            
            return_preferences = preferences.copy() if preferences else {}
            return_preferences['from_location'] = travel_details.get('destination', '')  # Starting from original destination
            
            print(f"DEBUG: Return flight setup - from {return_preferences.get('from_location')} to {return_travel_details.get('destination')} on {return_travel_details.get('departure')}")
            
            return_result = self._search_one_way_flights(return_travel_details, return_preferences, flight_type="return")
            
            print(f"DEBUG: Return flight result: {return_result.get('success', False)}")
            if not return_result.get('success'):
                print(f"DEBUG: Return flight error: {return_result.get('error', 'Unknown error')}")
            
            # Combine results - fix from_location defaulting like in travel details
            from_location = preferences.get('from_location', 'Bangalore')
            if not from_location or not from_location.strip():
                from_location = 'Bangalore'
            
            destination = travel_details.get('destination', 'Unknown')
            from_code = self._get_airport_code(from_location.lower())
            to_code = self._get_airport_code(destination.lower())
            from_city_corrected = self._get_corrected_city_name(from_code) if from_code else from_location.title()
            to_city_corrected = self._get_corrected_city_name(to_code) if to_code else destination.title()
            
            search_info = {
                "from_city": from_city_corrected,
                "to_city": to_city_corrected,
                "departure_date": self._format_date(travel_details.get('departure', '')),
                "return_date": self._format_date(travel_details.get('return', '')),
                "passengers": {
                    "adults": preferences.get('adults', self.search_preferences.get('adults', 1)),
                    "children": preferences.get('children', self.search_preferences.get('children', 0)), 
                    "infants": preferences.get('infants', self.search_preferences.get('infants', 0))
                },
                "cabin_class": self._map_travel_class_to_cabin(preferences.get('travel_class', self.search_preferences.get('travel_class', 1)))
            }
            
            print(f"DEBUG: Round-trip search_info - from_city: '{search_info.get('from_city', 'Bangalore')}', to_city: '{search_info.get('to_city', 'Unknown')}'")
            
            return {
                "success": True,
                "trip_type": "round_trip",
                "outbound": outbound_result,
                "return": return_result,
                "search_info": search_info
            }
            
        except Exception as e:
            return {"error": f"Round-trip flight search failed: {str(e)}"}
    
    def _search_one_way_flights(self, travel_details: Dict[str, str], preferences: Dict = None, flight_type: str = "outbound") -> Dict:
        """
        Search for one-way flights (used for both single trips and individual legs of round trips)
        """
        try:
            # Build search parameters for one-way flight
            search_params = self._build_one_way_search_params(travel_details, preferences, flight_type)
            
            if not search_params:
                return {"error": "Could not build search parameters from travel details"}
            
            # Make API request
            response = self._make_api_request(search_params)
            
            if response.get('error'):
                return {"error": response['error']}
            
            # Parse and format results
            flights = self._parse_flight_results(response)
            
            # Build proper search info based on actual API parameters
            departure_id = search_params.get('departure_id', self.default_departure_code)
            arrival_id = search_params.get('arrival_id', 'Unknown')
            departure_city = self._get_corrected_city_name(departure_id)
            destination_city = self._get_corrected_city_name(arrival_id)
            
            return {
                "success": True,
                "flights": flights,
                "flight_type": flight_type,
                "search_info": {
                    "from": departure_id,
                    "to": arrival_id,
                    "from_city": departure_city,
                    "to_city": destination_city,
                    "departure_date": search_params.get('outbound_date', 'Unknown'),
                    "return_date": 'One-way',
                    "passengers": {
                        "adults": preferences.get('adults', self.search_preferences.get('adults', 1)),
                        "children": preferences.get('children', self.search_preferences.get('children', 0)), 
                        "infants": preferences.get('infants', self.search_preferences.get('infants', 0))
                    },
                    "cabin_class": self._map_travel_class_to_cabin(preferences.get('travel_class', self.search_preferences.get('travel_class', 1)))
                }
            }
            
        except Exception as e:
            return {"error": f"One-way flight search failed: {str(e)}"}
    
    def _build_one_way_search_params(self, travel_details: Dict[str, str], preferences: Dict = None, flight_type: str = "outbound") -> Optional[Dict]:
        """
        Build SerpAPI search parameters for one-way flights
        """
        if preferences is None:
            preferences = {}
            
        try:
            # Get destination
            destination = travel_details.get('destination', '').lower()
            destination_code = self._get_airport_code(destination)
            
            if not destination_code:
                return None
            
            # Get departure date (for outbound use departure, for return use return date)
            if flight_type == "return":
                flight_date = self._format_date(travel_details.get('departure', ''))  # This is actually return date in return flight context
            else:
                flight_date = self._format_date(travel_details.get('departure', ''))
            
            # Get departure location
            from_location = preferences.get('from_location', 'Bangalore')
            departure_id = self._get_airport_code(from_location.lower())
            
            if not departure_id:
                departure_id = 'BLR'  # Fallback to Bangalore
            
            # Build search parameters for one-way flight with Indian market targeting
            params = {
                'engine': 'google_flights',
                'api_key': self.api_key,
                'departure_id': departure_id,
                'arrival_id': destination_code,
                'outbound_date': flight_date,
                'currency': 'INR',
                'hl': 'en',  # English language
                'gl': 'in',  # India country code - critical for Indian OTA visibility
                'adults': 1,
                'travel_class': preferences.get('travel_class', 1),
                'stops': preferences.get('stops', 2),
                'type': '2',  # Always one-way for individual legs
                'deep_search': True,  # Essential for OTA access
                'show_hidden': True  # Include hidden flight results for more flights
            }
            
            print(f"DEBUG: {flight_type.title()} flight - {from_location.title()} ({departure_id}) → {destination.title()} ({destination_code}) on {flight_date}")
            
            return params
            
        except Exception as e:
            print(f"Error building {flight_type} search params: {e}")
            return None

    def _build_search_params(self, travel_details: Dict[str, str], preferences: Dict = None) -> Optional[Dict]:
        """
        Build SerpAPI search parameters from travel details and user preferences
        """
        if preferences is None:
            preferences = {}
            
        try:
            # Get destination
            destination = travel_details.get('destination', '').lower()
            destination_code = self._get_airport_code(destination)
            
            if not destination_code:
                return None
            
            # Get dates
            departure_date = self._format_date(travel_details.get('departure', ''))
            return_date = self._format_date(travel_details.get('return', ''))
            
            # Get departure location (from preferences or default)
            from_location = preferences.get('from_location', 'Bangalore')
            departure_id = self._get_airport_code(from_location.lower())
            
            if not departure_id:
                departure_id = 'BLR'  # Fallback to Bangalore
            
            # Build search parameters with enhanced Indian market targeting
            params = {
                'engine': 'google_flights',
                'api_key': self.api_key,
                'departure_id': departure_id,
                'arrival_id': destination_code,
                'outbound_date': departure_date,
                'currency': 'INR',
                'hl': 'en',  # English language
                'gl': 'in',  # India country code - critical for Indian OTA visibility
                'adults': 1,  # Default to 1 adult
                'travel_class': preferences.get('travel_class', 1),  # User preference or Economy
                'stops': preferences.get('stops', 2),  # User preference or All flights
                'deep_search': True,  # More accurate results like browser - essential for OTA access
                'show_hidden': True,  # Include hidden flight results for more flights
                'type': '2'  # Default to one-way, will override below for round-trip
            }
            
            # Debug: Print search parameters
            print(f"Search Parameters: From={from_location}, Stops={preferences.get('stops')}, Class={preferences.get('travel_class')}")
            print(f"API Params: departure_id={departure_id}, stops={params['stops']}, travel_class={params['travel_class']}")
            
            # Add return date if available (round trip)
            if return_date and return_date != departure_date:
                params['return_date'] = return_date
                params['type'] = '1'  # Round trip
            else:
                params['type'] = '2'  # One way
            
            return params
            
        except Exception as e:
            print(f"Error building search params: {e}")
            return None
    
    def _get_airport_code(self, city_name: str) -> Optional[str]:
        """
        Get airport code for a city - enhanced with fuzzy matching for typos
        """
        if not city_name:
            return None
        
        # Clean the city name
        clean_name = city_name.lower().strip()
        print(f"DEBUG: Looking up airport code for: '{clean_name}'")
        
        # Direct lookup
        code = self.city_codes.get(clean_name)
        if code:
            print(f"DEBUG: Direct match found: {clean_name} -> {code}")
            return code
        
        # Try partial matching for common variations
        for city, code in self.city_codes.items():
            if clean_name in city or city in clean_name:
                print(f"DEBUG: Partial match found: {clean_name} matches {city} -> {code}")
                return code
        
        # Enhanced fuzzy matching for typos (like "hydrabad" -> "hyderabad")
        best_match = None
        best_score = 0
        
        for city, code in self.city_codes.items():
            # Calculate similarity score
            if len(clean_name) >= 3 and len(city) >= 3:
                # Count matching characters in sequence
                matches = 0
                min_len = min(len(clean_name), len(city))
                
                for i in range(min_len):
                    if clean_name[i] == city[i]:
                        matches += 1
                    else:
                        break
                
                # Also check if most characters match (allowing for typos)
                common_chars = set(clean_name) & set(city)
                char_similarity = len(common_chars) / max(len(set(clean_name)), len(set(city)))
                
                # Combined score: prefix match + character similarity
                score = (matches / min_len) * 0.7 + char_similarity * 0.3
                
                if score > best_score and score > 0.6:  # Threshold for match
                    best_score = score
                    best_match = (city, code)
        
        if best_match:
            print(f"DEBUG: Fuzzy match found: {clean_name} -> {best_match[0]} -> {best_match[1]} (score: {best_score:.2f})")
            return best_match[1]
        
        print(f"DEBUG: No match found for '{clean_name}', using fallback BLR")
        # Fallback to BLR if nothing found
        return 'BLR'
    
    def _get_corrected_city_name(self, airport_code: str) -> str:
        """
        Get proper city name from airport code
        """
        code_to_city = {
            'BLR': 'Bangalore', 'DEL': 'Delhi', 'BOM': 'Mumbai', 'MAA': 'Chennai',
            'CCU': 'Kolkata', 'HYD': 'Hyderabad', 'AMD': 'Ahmedabad', 'COK': 'Kochi',
            'SIN': 'Singapore', 'KUL': 'Kuala Lumpur', 'BKK': 'Bangkok', 'CGK': 'Jakarta',
            'DXB': 'Dubai', 'DOH': 'Doha', 'LHR': 'London', 'CDG': 'Paris', 'FRA': 'Frankfurt'
        }
        return code_to_city.get(airport_code, airport_code)
    
    def _get_destination_timezone(self, airport_code: str) -> str:
        """
        Get timezone display text based on airport code
        """
        timezone_map = {
            # India
            'BOM': 'Indian Time (IST)',
            'DEL': 'Indian Time (IST)', 
            'BLR': 'Indian Time (IST)',
            'HYD': 'Indian Time (IST)',
            'MAA': 'Indian Time (IST)',
            'CCU': 'Indian Time (IST)',
            'PNQ': 'Indian Time (IST)',
            'GOI': 'Indian Time (IST)',
            'AMD': 'Indian Time (IST)',
            'COK': 'Indian Time (IST)',
            'JAI': 'Indian Time (IST)',
            'TRV': 'Indian Time (IST)',
            'UDR': 'Indian Time (IST)',
            'JDH': 'Indian Time (IST)',
            
            # Southeast Asia
            'SIN': 'Singapore Time (SGT)',
            'BKK': 'Thailand Time (ICT)',
            'KUL': 'Malaysia Time (MYT)',
            'CGK': 'Indonesia Time (WIB)',
            'MNL': 'Philippines Time (PHT)',
            'HAN': 'Vietnam Time (ICT)',
            'SGN': 'Vietnam Time (ICT)',
            
            # Middle East
            'DXB': 'UAE Time (GST)',
            'AUH': 'UAE Time (GST)',
            'DOH': 'Qatar Time (AST)',
            'KWI': 'Kuwait Time (AST)',
            'RUH': 'Saudi Time (AST)',
            'JED': 'Saudi Time (AST)',
            'MCT': 'Oman Time (GST)',
            'TLV': 'Israel Time (IST)',
            'BEY': 'Lebanon Time (EET)',
            'AMM': 'Jordan Time (EET)',
            
            # Europe
            'LHR': 'UK Time (GMT/BST)',
            'LGW': 'UK Time (GMT/BST)',
            'MAN': 'UK Time (GMT/BST)',
            'CDG': 'France Time (CET/CEST)',
            'ORY': 'France Time (CET/CEST)',
            'AMS': 'Netherlands Time (CET/CEST)',
            'FRA': 'Germany Time (CET/CEST)',
            'MUC': 'Germany Time (CET/CEST)',
            'ZUR': 'Switzerland Time (CET/CEST)',
            'VIE': 'Austria Time (CET/CEST)',
            'FCO': 'Italy Time (CET/CEST)',
            'MXP': 'Italy Time (CET/CEST)',
            'MAD': 'Spain Time (CET/CEST)',
            'BCN': 'Spain Time (CET/CEST)',
            'IST': 'Turkey Time (TRT)',
            'SVO': 'Russia Time (MSK)',
            'ATH': 'Greece Time (EET)',
            
            # North America
            'JFK': 'US Eastern Time (EST/EDT)',
            'LGA': 'US Eastern Time (EST/EDT)',
            'EWR': 'US Eastern Time (EST/EDT)',
            'LAX': 'US Pacific Time (PST/PDT)',
            'SFO': 'US Pacific Time (PST/PDT)',
            'ORD': 'US Central Time (CST/CDT)',
            'DFW': 'US Central Time (CST/CDT)',
            'YYZ': 'Canada Eastern Time (EST/EDT)',
            'YVR': 'Canada Pacific Time (PST/PDT)',
            
            # East Asia
            'NRT': 'Japan Time (JST)',
            'HND': 'Japan Time (JST)',
            'KIX': 'Japan Time (JST)',
            'ICN': 'Korea Time (KST)',
            'GMP': 'Korea Time (KST)',
            'PEK': 'China Time (CST)',
            'PVG': 'China Time (CST)',
            'SHA': 'China Time (CST)',
            'HKG': 'Hong Kong Time (HKT)',
            'TPE': 'Taiwan Time (CST)',
            
            # Oceania
            'SYD': 'Australia Eastern Time (AEST/AEDT)',
            'MEL': 'Australia Eastern Time (AEST/AEDT)',
            'BNE': 'Australia Eastern Time (AEST/AEDT)',
            'PER': 'Australia Western Time (AWST)',
            'AKL': 'New Zealand Time (NZST/NZDT)',
            
            # Africa
            'CAI': 'Egypt Time (EET)',
            'JNB': 'South Africa Time (SAST)',
            'CPT': 'South Africa Time (SAST)',
            'NBO': 'Kenya Time (EAT)',
            'ADD': 'Ethiopia Time (EAT)'
        }
        
        return timezone_map.get(airport_code, 'Local Time')
    
    def _format_date(self, date_str: str) -> str:
        """
        Format date for SerpAPI (YYYY-MM-DD)
        """
        try:
            if not date_str or date_str == 'Not specified':
                # Default to next week
                default_date = datetime.now() + timedelta(days=7)
                return default_date.strftime('%Y-%m-%d')
            
            # Try to parse the date (assuming format like "15 Jun 2025")
            date_obj = datetime.strptime(date_str, "%d %b %Y")
            return date_obj.strftime('%Y-%m-%d')
            
        except:
            # Fallback to next week
            default_date = datetime.now() + timedelta(days=7)
            return default_date.strftime('%Y-%m-%d')
    
    def _make_api_request(self, params: Dict) -> Dict:
        """
        Make request to SerpAPI with proper error handling
        """
        try:
            # Debug: Print what parameters we're sending
            debug_params = {k: v for k, v in params.items() if k != 'api_key'}
            print(f"DEBUG: SerpAPI request parameters: {debug_params}")
            
            response = requests.get(self.base_url, params=params, timeout=30)
            
            # Handle specific HTTP status codes
            if response.status_code == 429:
                return {"error": "Rate limit exceeded. Please wait a few minutes before searching again. SerpAPI has usage limits per minute."}
            elif response.status_code == 401:
                return {"error": "Invalid API key. Please check your SerpAPI configuration."}
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Invalid request parameters')
                    return {"error": f"API request error: {error_msg}"}
                except:
                    return {"error": "Invalid request parameters sent to API"}
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            return {"error": "API request timed out. Please try again."}
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response format from API"}
    
    def _parse_flight_results(self, response: Dict) -> List[Dict]:
        """
        Parse flight results from SerpAPI response
        """
        # Combine both best_flights and other_flights to get all available flights
        best_flights = response.get('best_flights', [])
        other_flights = response.get('other_flights', [])
        flights = best_flights + other_flights
        
        print(f"DEBUG: Found {len(best_flights)} best flights and {len(other_flights)} other flights")
        print(f"DEBUG: Total {len(flights)} flights in API response")
        
        # Add some debug info about the full response structure
        if flights and len(flights) > 0:
            sample_flight = flights[0]
            print(f"DEBUG: Sample flight keys: {list(sample_flight.keys())}")
            if 'booking_token' in sample_flight:
                print(f"DEBUG: Sample booking_token present: {bool(sample_flight.get('booking_token'))}")
            if 'departure_token' in sample_flight:
                print(f"DEBUG: Sample departure_token present: {bool(sample_flight.get('departure_token'))}")
        
        parsed_flights = []
        for flight in flights:
            parsed_flight = self._extract_flight_info(flight)
            if parsed_flight:
                parsed_flights.append(parsed_flight)
        
        # Sort by departure time
        if parsed_flights:
            def parse_time_for_sorting(time_str):
                try:
                    if not time_str or time_str == 'Unknown':
                        return datetime.min
                    
                    # Handle various time formats from API
                    if ' ' in time_str:
                        time_part = time_str.split(' ')[1] if len(time_str.split(' ')) > 1 else time_str.split(' ')[0]
                    else:
                        time_part = time_str
                    
                    # Remove timezone info for parsing
                    time_clean = time_part.split(' ')[0] if ' ' in time_part else time_part
                    
                    # Parse time
                    if ':' in time_clean:
                        return datetime.strptime(time_clean, '%H:%M')
                    return datetime.min
                except:
                    return datetime.min
            
            parsed_flights.sort(key=lambda x: parse_time_for_sorting(x.get('raw_departure_time', '')))
        
        print(f"DEBUG: Successfully parsed {len(parsed_flights)} flights")
        return parsed_flights
    
    def _extract_flight_info(self, flight_data: Dict) -> Optional[Dict]:
        """
        Extract relevant information from a single flight
        """
        try:
            flights = flight_data.get('flights', [])
            if not flights:
                return None
            
            # Get first and last flight segments
            first_flight = flights[0]
            last_flight = flights[-1]
            
            # Extract basic info - ONLY from API, no fallbacks
            airline = first_flight.get('airline')
            if not airline:
                print(f"DEBUG: No airline data in API response")
                return None
                
            flight_number = first_flight.get('flight_number')
            if not flight_number:
                print(f"DEBUG: No flight_number in API response")
                return None
                
            departure_time = first_flight.get('departure_airport', {}).get('time')
            arrival_time = last_flight.get('arrival_airport', {}).get('time')
            
            if not departure_time or not arrival_time:
                print(f"DEBUG: Missing time data in API response")
                return None
            
            # Format duration - ONLY from API
            total_duration = flight_data.get('total_duration')
            if total_duration and isinstance(total_duration, (int, float)) and total_duration > 0:
                hours = total_duration // 60
                minutes = total_duration % 60
                duration = f"{hours}h {minutes}m"
            else:
                print(f"DEBUG: No valid duration in API response: {total_duration}")
                return None
            
            # Extract price - ONLY from API, no fallbacks
            price = flight_data.get('price')
            print(f"DEBUG: Raw price from API: {price}, type: {type(price)}")
            
            if isinstance(price, (int, float)) and price > 0:
                price_display = f"₹{price:,.0f}"
                price_value = price
            else:
                # Try alternative price field from API
                alt_price = flight_data.get('total_price')
                print(f"DEBUG: Alternative price: {alt_price}")
                if isinstance(alt_price, (int, float)) and alt_price > 0:
                    price_display = f"₹{alt_price:,.0f}"
                    price_value = alt_price
                else:
                    print(f"DEBUG: No valid price in API response")
                    return None
            
            # Determine stops and layover info
            layovers = flight_data.get('layovers', [])
            if len(flights) == 1:
                stops = "Non-Stop"
                layover_info = ""
            else:
                stops = f"{len(flights) - 1} stop(s)"
                if layovers:
                    layover_cities = [layover.get('id', 'Unknown') for layover in layovers]
                    layover_info = f" (via {', '.join(layover_cities)})"
                else:
                    layover_info = ""
            
            # Get route info - ONLY from API
            departure_id = first_flight.get('departure_airport', {}).get('id')
            arrival_id = last_flight.get('arrival_airport', {}).get('id')
            
            if not departure_id or not arrival_id:
                print(f"DEBUG: Missing airport IDs in API response")
                return None
                
            route = f"{departure_id} → {arrival_id}"
            
            # Store raw departure time for sorting
            raw_departure_time = first_flight.get('departure_airport', {}).get('time')
            
            # Get timezone information for both departure and arrival (already validated above)
            departure_airport_id = departure_id
            arrival_airport_id = arrival_id
            departure_timezone = self._get_destination_timezone(departure_airport_id)
            destination_timezone = self._get_destination_timezone(arrival_airport_id)
            
            # Format times with timezone information - ONLY if data exists
            if departure_time:
                if len(departure_time) > 10:
                    departure_time = departure_time.split(' ')[1] if ' ' in departure_time else departure_time[-5:]
                departure_time = f"{departure_time} {departure_timezone}"
                
            if arrival_time:
                if len(arrival_time) > 10:
                    arrival_time = arrival_time.split(' ')[1] if ' ' in arrival_time else arrival_time[-5:]
                arrival_time = f"{arrival_time} {destination_timezone}"
            
            # Get booking token for booking options (preferred over departure_token)
            booking_token = flight_data.get('booking_token', '')
            departure_token = flight_data.get('departure_token', '')
            
            print(f"DEBUG: Booking token extracted: '{booking_token}' (length: {len(booking_token) if booking_token else 0})")
            print(f"DEBUG: Departure token extracted: '{departure_token}' (length: {len(departure_token) if departure_token else 0})")
            
            # Use booking_token if available, otherwise fall back to departure_token
            primary_token = booking_token if booking_token else departure_token
            
            # If no real tokens available from API, set to None
            if not primary_token:
                print(f"DEBUG: No real tokens available from SerpAPI response")
                primary_token = None
            
            return {
                'airline': airline,
                'flight_number': flight_number,
                'route': route,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': duration,
                'price_display': price_display,
                'price_value': price_value,
                'stops': stops + layover_info,
                'booking_token': booking_token,  # Primary token for booking
                'departure_token': departure_token,  # Fallback token
                'primary_token': primary_token,  # The token to actually use (None if unavailable)
                'raw_departure_time': raw_departure_time,  # For sorting
                'flight_data': flight_data,  # Keep original data for booking links
                # Store context needed for booking token requests (already validated)
                'departure_id': departure_id,
                'arrival_id': arrival_id
            }
            
        except Exception as e:
            print(f"ERROR: Failed to extract flight info: {e}")
            print(f"DEBUG: Flight data was: {flight_data}")
            return None
    
    def format_flights_for_display(self, search_result: Dict) -> str:
        """
        Format flight results for HTML display with separate outbound and return sections
        """
        if search_result.get('error'):
            return f"""
            <div style="color: red; padding: 20px; text-align: center;">
                <h3>❌ Flight Search Error</h3>
                <p>{search_result['error']}</p>
                <p><small>Please check your SerpAPI key and try again.</small></p>
            </div>
            """
        
        # Check if this is a round-trip search with separate outbound and return
        if search_result.get('trip_type') == 'round_trip':
            return self._format_round_trip_flights(search_result)
        
        # Handle one-way flights (legacy format)
        flights = search_result.get('flights', [])
        search_info = search_result.get('search_info', {})
        
        if not flights:
            return """
            <div style="padding: 20px; text-align: center;">
                <h3>✈️ No Flights Found</h3>
                <p>No flights available for the selected route and dates.</p>
            </div>
            """
        
        # Build HTML for one-way flights
        return self._format_one_way_flights(flights, search_info, search_result.get('flight_type', 'outbound'))
    
    def _format_round_trip_flights(self, search_result: Dict) -> str:
        """
        Format round-trip flights with separate outbound and return sections
        """
        outbound_result = search_result.get('outbound', {})
        return_result = search_result.get('return', {})
        search_info = search_result.get('search_info', {})
        
        print(f"DEBUG: Round-trip search_info - from_city: '{search_info.get('from_city')}', to_city: '{search_info.get('to_city')}'")
        
        # Only show route info if we have valid API data
        from_city = search_info.get('from_city') or 'API data missing'
        to_city = search_info.get('to_city') or 'API data missing'
        departure_date = search_info.get('departure_date') or 'API data missing'
        return_date = search_info.get('return_date') or 'API data missing'
        
        html = f"""
        <div style="margin-top: 20px;">
            <h3 style="color: #2c3e50; margin-bottom: 20px;">✈️ Flight Results</h3>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                <p><strong>Route:</strong> {from_city} ↔ {to_city}</p>
                <p><strong>Departure:</strong> {departure_date} | <strong>Return:</strong> {return_date}</p>
            </div>
        """
        
        # Outbound flights section
        if outbound_result.get('success') and outbound_result.get('flights'):
            html += """
            <div style="margin-bottom: 30px;">
                <h4 style="color: #27ae60; border-bottom: 2px solid #27ae60; padding-bottom: 5px;">🛫 Outbound Flights</h4>
            """
            outbound_search_info = outbound_result.get('search_info', {})
            html += self._format_one_way_flights(outbound_result['flights'], outbound_search_info, 'outbound')
            html += "</div>"
        else:
            html += """
            <div style="margin-bottom: 30px;">
                <h4 style="color: #e74c3c;">🛫 Outbound Flights</h4>
                <div style="padding: 20px; text-align: center; background: #ffeaa7; border-radius: 8px;">
                    <p>❌ No outbound flights found or search failed</p>
                </div>
            </div>
            """
        
        # Return flights section
        if return_result.get('success') and return_result.get('flights'):
            html += """
            <div>
                <h4 style="color: #8e44ad; border-bottom: 2px solid #8e44ad; padding-bottom: 5px;">🛬 Return Flights</h4>
            """
            return_search_info = return_result.get('search_info', {})
            html += self._format_one_way_flights(return_result['flights'], return_search_info, 'return')
            html += "</div>"
        else:
            html += """
            <div>
                <h4 style="color: #e74c3c;">🛬 Return Flights</h4>
                <div style="padding: 20px; text-align: center; background: #ffeaa7; border-radius: 8px;">
                    <p>❌ No return flights found or search failed</p>
                </div>
            </div>
            """
        
        # Travel Itinerary section removed
        
        html += "</div>"
        return html
    
    def _format_one_way_flights(self, flights: list, search_info: Dict, flight_type: str = 'outbound') -> str:
        """
        Format one-way flights for display
        """
        if not flights:
            return """
            <div style="padding: 20px; text-align: center;">
                <p>No flights available for this route.</p>
            </div>
            """
        
        # Build HTML with readable city names and airport codes - ONLY from API data
        from_city = search_info.get('from_city', 'API data unavailable')
        from_code = search_info.get('from', 'N/A')
        to_city = search_info.get('to_city', 'API data unavailable') 
        to_code = search_info.get('to', 'N/A')
        
        from_display = f"{from_city} ({from_code})"
        to_display = f"{to_city} ({to_code})"
        
        html = f"""
        <div style="margin-bottom: 15px;">
            <p><strong>{from_display} → {to_display}</strong> <span style="font-size: 12px; color: #666;">(Sorted By Departure Time, Earliest First)</span></p>
            <p><strong>📊 Total Flights Found:</strong> {len(flights)}</p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 12px; margin-top: 15px;">
        """
        
        for i, flight in enumerate(flights, 1):
            # Determine flight badge (now based on departure time)
            badge = ""
            if i == 1:
                badge = '<span style="background: #3498db; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px;">EARLIEST</span>'
            elif i <= 3:
                badge = '<span style="background: #9b59b6; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin-left: 10px;">MORNING</span>'
            
            # Set border color based on flight type
            border_color = "#27ae60" if flight_type == "outbound" else "#8e44ad"
            
            # Generate MakeMyTrip URL for this specific flight
            airline_code = self._extract_airline_code(flight.get('airline', ''))
            departure_id = flight.get('departure_id', search_info.get('from', ''))
            arrival_id = flight.get('arrival_id', search_info.get('to', ''))
            flight_date = search_info.get('departure_date') or search_info.get('outbound_date') or search_info.get('return_date', '')
            
            # Get passenger and class info from search preferences (stored in search_info if available)
            passengers = search_info.get('passengers', {'adults': 1, 'children': 0, 'infants': 0})
            cabin_class = search_info.get('cabin_class', 'E')  # Default Economy
            
            # Generate MakeMyTrip URL for this flight
            makemytrip_url = self._generate_makemytrip_url(
                from_code=departure_id,
                to_code=arrival_id, 
                date=flight_date,
                passengers=passengers,
                cabin_class=cabin_class,
                airline_code=airline_code
            )
            
            # Create simple "Proceed To Book" button
            token_section = f"""
            <div style="margin-top: 10px; text-align: center;">
                <a href="{makemytrip_url}" target="_blank" 
                   style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                          color: white; border: none; padding: 6px 20px; border-radius: 20px;
                          font-weight: bold; text-decoration: none; font-size: 13px;
                          display: inline-block; box-shadow: 0 3px 6px rgba(0,0,0,0.2);
                          transition: transform 0.2s;">
                    🚀 Proceed To Book
                </a>
                <div style="font-size: 10px; color: red; font-weight: bold; margin-top: 4px;">
                    Select Non-Stop & Look for "{flight.get('flight_number', 'N/A')}" when you get there
                </div>
            </div>
            """
            
            html += f"""
            <div style="border: 1px solid {border_color}; border-radius: 8px; padding: 12px; background: #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div style="color: {border_color}; font-weight: bold; margin-bottom: 8px; font-size: 14px;">🎯 Flight {i}:{badge}</div>
                <div style="display: flex; flex-direction: column; gap: 4px; font-size: 13px;">
                    <div><strong>✈️ Airline:</strong> {flight['airline']}</div>
                    <div><strong>🔢 Flight Number:</strong> {flight.get('flight_number', 'API data missing')}</div>
                    <div><strong>🗺️ Route:</strong> {flight['route']}</div>
                    <div><strong>📅 Date:</strong> {search_info.get('departure_date') or search_info.get('outbound_date') or search_info.get('return_date') or 'API data missing'}</div>
                    <div><strong>🕐 Departure:</strong> {flight['departure_time']}</div>
                    <div><strong>🕐 Arrival:</strong> {flight['arrival_time']}</div>
                    <div><strong>⏱️ Duration:</strong> {flight['duration']}</div>
                    <div><strong>💰 Price:</strong> <span style="color: #e53e3e; font-weight: bold;">{flight['price_display']}</span></div>
                    <div><strong>🛑 Stops:</strong> {flight['stops']}</div>
                </div>
                {token_section}
            </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def get_price_insights(self, travel_details: Dict[str, str]) -> Dict:
        """
        Get price insights and trends for the route
        """
        try:
            search_params = self._build_search_params(travel_details)
            if not search_params:
                return {"error": "Could not build search parameters"}
            
            # Add price insights parameter
            search_params['show_price_insights'] = True
            
            response = self._make_api_request(search_params)
            
            if response.get('error'):
                return {"error": response['error']}
            
            price_insights = response.get('price_insights', {})
            return {
                "success": True,
                "insights": price_insights
            }
            
        except Exception as e:
            return {"error": f"Price insights failed: {str(e)}"}
    
    def get_booking_options(self, enriched_token: str, departure_id: str = None, arrival_id: str = None, outbound_date: str = None) -> Dict:
        """
        Get booking options for a specific flight using enriched token (includes context)
        Ensures fresh data with no caching or stored tokens
        """
        try:
            if not enriched_token or not enriched_token.strip():
                return {"error": "No booking token provided"}
            
            # Clean the token to ensure no whitespace issues
            enriched_token = enriched_token.strip()
            
            print(f"DEBUG: Processing fresh booking token request...")
            print(f"DEBUG: Enriched token starts with: {enriched_token[:20]}...")
            print(f"DEBUG: Enriched token ends with: ...{enriched_token[-20:]}")
            
            # Try to decode enriched token with context
            actual_token = enriched_token
            context_departure_id = departure_id
            context_arrival_id = arrival_id
            context_outbound_date = outbound_date
            context_return_date = None
            context_trip_type = 'one_way'  # Default to one-way for individual flights
            
            try:
                import json
                import base64
                # Try to decode as enriched token
                decoded_context = json.loads(base64.b64decode(enriched_token).decode())
                actual_token = decoded_context.get('token', '')
                context_departure_id = decoded_context.get('departure_id', departure_id)
                context_arrival_id = decoded_context.get('arrival_id', arrival_id)
                context_outbound_date = decoded_context.get('outbound_date', outbound_date)
                context_return_date = decoded_context.get('return_date', None)
                context_trip_type = decoded_context.get('trip_type', 'one_way')
                print(f"DEBUG: Successfully decoded enriched token with context:")
                print(f"DEBUG: - departure_id: {context_departure_id}")
                print(f"DEBUG: - arrival_id: {context_arrival_id}")
                print(f"DEBUG: - outbound_date: {context_outbound_date}")
                print(f"DEBUG: - return_date: {context_return_date}")
                print(f"DEBUG: - trip_type: {context_trip_type}")
            except:
                # If decoding fails, treat as regular token
                print(f"DEBUG: Token is not enriched, treating as regular booking token")
                actual_token = enriched_token
            
            # Validate token format integrity
            validation_error = self._validate_booking_token(actual_token)
            if validation_error:
                print(f"DEBUG: Token validation failed: {validation_error}")
                return {"error": validation_error}
            
            print(f"DEBUG: Token validation passed, making API request...")
            
            return self._handle_booking_request(actual_token, self.api_key, context_departure_id, context_arrival_id, context_outbound_date, context_return_date, context_trip_type)
            
        except Exception as e:
            print(f"DEBUG: Booking options error: {str(e)}")
            return {"error": f"Booking options failed: {str(e)}"}
    
    def _validate_booking_token(self, booking_token: str) -> Optional[str]:
        """
        Validate booking token format integrity
        """
        try:
            # Check length (should be 212-272 characters)
            if len(booking_token) < 200 or len(booking_token) > 300:
                return f"Invalid token length: {len(booking_token)} (expected 212-272 chars)"
            
            # Check for line breaks or whitespace corruption
            if '\n' in booking_token or '\r' in booking_token or '  ' in booking_token:
                return "Token contains line breaks or whitespace corruption"
            
            # Validate Base64 encoding integrity
            import base64
            try:
                # Token should be valid Base64
                base64.b64decode(booking_token, validate=True)
            except Exception:
                return "Token appears to be corrupted (invalid Base64 encoding)"
            
            print(f"DEBUG: Token validation passed - length: {len(booking_token)}, format: valid")
            return None  # No validation errors
            
        except Exception as e:
            return f"Token validation failed: {str(e)}"
    
    def _handle_booking_request(self, booking_token: str, api_key: str, departure_id: str = None, arrival_id: str = None, outbound_date: str = None, return_date: str = None, trip_type: str = 'one_way') -> Dict:
        """
        Handle booking request - use standard google_flights engine with booking_token
        This ensures we get fresh data and properly handle the token context
        """
        # Use the original working approach - booking tokens need flight context
        # Build complete parameters including required departure_id and arrival_id
        params = {
            'engine': 'google_flights',
            'booking_token': booking_token,
            'api_key': api_key,
            'currency': 'INR',
            'hl': 'en'
        }
        
        # Add required context parameters if provided
        if departure_id:
            params['departure_id'] = departure_id
        if arrival_id:
            params['arrival_id'] = arrival_id
        if outbound_date:
            params['outbound_date'] = outbound_date
        
        # For individual flight bookings, always treat as one-way (type=2)
        # Only add return_date and type=1 if explicitly specified as round_trip
        if trip_type == 'round_trip' and return_date:
            params['return_date'] = return_date
            params['type'] = '1'  # Round trip
        else:
            params['type'] = '2'  # One way
        
        print(f"DEBUG: Making booking request with token: {booking_token[:50]}...")
        print(f"DEBUG: Token length: {len(booking_token)}")
        print(f"DEBUG: Parameters: {list(params.keys())}")
        
        # Make direct API request
        import requests
        try:
            response = requests.get('https://serpapi.com/search.json', params=params, timeout=30)
            
            print(f"DEBUG: Response status code: {response.status_code}")
            
            # Handle specific HTTP status codes
            if response.status_code == 429:
                return {"error": "⚠️ Rate limit exceeded! Please wait 2-3 minutes before trying booking options again. SerpAPI has strict usage limits."}
            elif response.status_code == 401:
                return {"error": "Invalid API key. Please check your SerpAPI configuration."}
            elif response.status_code == 400:
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', 'Unknown API error')
                    print(f"DEBUG: 400 error details: {error_msg}")
                    
                    # Check if it's specifically a token issue
                    if 'token' in error_msg.lower() or 'expired' in error_msg.lower():
                        return {"error": "Booking token has expired or is invalid - please get fresh booking options from a new flight search"}
                    else:
                        return {"error": f"API validation error: {error_msg}"}
                except:
                    return {"error": "API request validation failed - token may be expired or malformed"}
            
            if response.status_code != 200:
                return {"error": f"API request failed with status {response.status_code}"}
            
            result = response.json()
            
            print(f"DEBUG: Response keys: {list(result.keys()) if result else 'None'}")
            
            if result.get('error'):
                return {"error": f"SerpAPI Error: {result['error']}"}
            
            # Extract booking options from the response
            booking_options = result.get('booking_options', [])
            selected_flights = result.get('selected_flights', [])
            
            print(f"DEBUG: Found {len(booking_options)} booking options")
            print(f"DEBUG: Found {len(selected_flights)} selected flights")
            
            # Show ALL available booking sources from API with flight context
            print(f"DEBUG: === ALL AVAILABLE BOOKING SOURCES FROM API ===")
            print(f"DEBUG: Flight Date: {outbound_date}")
            print(f"DEBUG: Route: {departure_id} → {arrival_id}")
            print(f"DEBUG: Trip Type: {trip_type}")
            
            for i, option in enumerate(booking_options):
                if 'together' in option:
                    together = option['together']
                    book_with = together.get('book_with', 'Unknown')
                    marketed_as = together.get('marketed_as', 'Unknown')
                    price = together.get('price', 'Unknown')
                    print(f"DEBUG: Source {i+1}: '{book_with}' (marketed as: '{marketed_as}', price: {price})")
                    print(f"DEBUG:   -> Date: {outbound_date}, Route: {departure_id}→{arrival_id}")
                    
                    # Check if there's a booking_request with URL
                    if 'booking_request' in together:
                        booking_req = together['booking_request']
                        if 'url' in booking_req:
                            print(f"DEBUG:   -> URL: {booking_req['url'][:100]}...")
                else:
                    book_with = option.get('book_with', 'Unknown')
                    print(f"DEBUG: Source {i+1}: '{book_with}' (direct structure)")
                    print(f"DEBUG:   -> Date: {outbound_date}, Route: {departure_id}→{arrival_id}")
            print(f"DEBUG: === END OF ALL AVAILABLE SOURCES ===")
            
            if booking_options and len(booking_options) > 0:
                sample_option = booking_options[0]
                print(f"DEBUG: Sample booking option keys: {list(sample_option.keys())}")
                if 'together' in sample_option:
                    print(f"DEBUG: Together option keys: {list(sample_option['together'].keys())}")
            
            # If no booking options found, return error
            if not booking_options:
                return {"error": "No booking options available from SerpAPI for this flight (token may have expired)"}
            
            # Filter and prioritize preferred Indian booking platforms
            preferred_sources = self._filter_preferred_booking_sources(booking_options)
            
            print(f"DEBUG: Filtered to {len(preferred_sources)} preferred sources")
            
            return {
                "success": True,
                "booking_options": preferred_sources,
                "selected_flights": selected_flights,
                "additional_details": result.get('search_metadata', {}),
                "baggage_prices": result.get('baggage_prices', []),
                "booking_phone": result.get('booking_phone', ''),
                "price_insights": result.get('price_insights', {})
            }
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Network error: {str(e)}"}
        except Exception as e:
            return {"error": f"Request processing failed: {str(e)}"}

    def get_booking_options_with_departure_token(self, departure_token: str) -> Dict:
        """
        Legacy method: Get booking options using departure token
        This is for backward compatibility if departure_token is still provided
        """
        try:
            params = {
                'engine': 'google_flights_booking_options',
                'api_key': self.api_key,
                'departure_token': departure_token
            }
            
            response = self._make_api_request(params)
            
            if response.get('error'):
                return {"error": response['error']}
            
            booking_options = response.get('booking_options', [])
            
            # Filter and prioritize preferred Indian booking platforms
            preferred_sources = self._filter_preferred_booking_sources(booking_options)
            
            # Add fallback Indian OTA links when Google doesn't provide them
            print(f"DEBUG: About to add fallback Indian OTAs - departure_id: {departure_id}, arrival_id: {arrival_id}, date: {outbound_date}")
            try:
                enhanced_sources = self._add_fallback_indian_otas(preferred_sources, departure_id, arrival_id, outbound_date)
                print(f"DEBUG: Fallback complete - Enhanced sources: {len(enhanced_sources)}")
            except Exception as e:
                print(f"DEBUG: ERROR in fallback method: {e}")
                enhanced_sources = preferred_sources  # Fallback to original sources
            
            return {
                "success": True,
                "booking_options": enhanced_sources,
                "additional_details": response.get('search_metadata', {}),
                "baggage_prices": response.get('baggage_prices', []),
                "booking_phone": response.get('booking_phone', '')
            }
            
        except Exception as e:
            return {"error": f"Booking options failed: {str(e)}"}

    def _filter_preferred_booking_sources(self, booking_options: List[Dict]) -> List[Dict]:
        """
        Filter and prioritize preferred booking sources with realistic expectations
        Always return up to 4 sources as requested, but clearly indicate limitations
        """
        # Prioritized platform list with MakeMyTrip first
        priority_platforms = ['makemytrip', 'cleartrip', 'goibibo', 'yatra', 'ixigo', 'easemytrip']
        
        # Separate booking options by priority
        makemytrip_options = []
        other_priority_platforms = []
        airline_direct = []
        other_platforms = []
        
        print(f"DEBUG: ⚠️  IMPORTANT: SerpAPI only returns booking platforms that Google Flights provides")
        print(f"DEBUG: Google Flights may not show Indian OTAs for all routes/airlines")
        print(f"DEBUG: Processing {len(booking_options)} total booking options from Google...")
        
        for i, option in enumerate(booking_options):
            # Get platform name from different possible fields
            book_with = ""
            if 'book_with' in option:
                book_with = option.get('book_with', '').lower()
            elif 'together' in option and 'book_with' in option['together']:
                book_with = option['together'].get('book_with', '').lower()
            elif 'together' in option and 'marketed_as' in option['together']:
                book_with = option['together'].get('marketed_as', '').lower()
            
            print(f"DEBUG: Option {i+1}: '{book_with}' (structure: {list(option.keys())})")
            
            # MakeMyTrip gets highest priority (check multiple variations)
            if any(term in book_with for term in ['makemytrip', 'make my trip', 'mmt']):
                makemytrip_options.append(option)
                print(f"DEBUG: ✅ Found MakeMyTrip: {book_with}")
            # Other preferred Indian platforms
            elif any(platform in book_with for platform in ['cleartrip', 'goibibo', 'yatra', 'ixigo', 'easemytrip']):
                other_priority_platforms.append(option)
                print(f"DEBUG: ✅ Found Indian OTA: {book_with}")
            # Airline direct booking
            elif any(airline in book_with for airline in ['air india', 'indigo', '6e', 'spicejet', 'vistara', 'jet airways', 'akasa', 'lufthansa', 'emirates', 'singapore airlines', 'thai airways', 'ai']):
                airline_direct.append(option)
                print(f"DEBUG: ✅ Found airline direct: {book_with}")
            else:
                other_platforms.append(option)
                print(f"DEBUG: ➡️ Found other platform: {book_with}")
        
        # Build final list with prioritized order
        final_sources = []
        
        # 1. MakeMyTrip first (highest priority)
        if makemytrip_options:
            final_sources.extend(makemytrip_options[:1])
            print(f"DEBUG: ✅ Added MakeMyTrip as #1 priority")
        else:
            print(f"DEBUG: ❌ MakeMyTrip not available from Google for this route")
        
        # 2. Other Indian OTAs (Cleartrip, Goibibo, etc.)
        remaining_slots = 4 - len(final_sources)
        if remaining_slots > 0 and other_priority_platforms:
            final_sources.extend(other_priority_platforms[:min(remaining_slots, 2)])
            print(f"DEBUG: ✅ Added {len(other_priority_platforms[:min(remaining_slots, 2)])} Indian OTA(s)")
        else:
            print(f"DEBUG: ❌ Other Indian OTAs not available from Google for this route")
        
        # 3. Airline Direct 
        remaining_slots = 4 - len(final_sources)
        if remaining_slots > 0 and airline_direct:
            final_sources.extend(airline_direct[:min(1, remaining_slots)])
            print(f"DEBUG: ✅ Added Airline Direct booking")
        
        # 4. Fill remaining slots with any other platforms
        remaining_slots = 4 - len(final_sources)
        if remaining_slots > 0:
            final_sources.extend(other_platforms[:remaining_slots])
            print(f"DEBUG: ➡️ Added {len(other_platforms[:remaining_slots])} other platform(s)")
        
        # If we don't have enough options, return all available options
        if len(final_sources) == 0 and len(booking_options) > 0:
            print("DEBUG: ⚠️  No preferred platforms found, showing what Google Flights provides")
            final_sources = booking_options[:4]
        
        # Summary for user
        indian_ota_count = len(makemytrip_options) + len(other_priority_platforms)
        if indian_ota_count == 0:
            print(f"DEBUG: 🔍 RECOMMENDATION: Google Flights doesn't show Indian OTAs for this route.")
            print(f"DEBUG: 💡 Try different dates, airlines, or search directly on MakeMyTrip/Cleartrip")
        
        print(f"DEBUG: Final booking sources returned: {len(final_sources)}")
        for i, source in enumerate(final_sources):
            book_with = source.get('book_with', 'Unknown')
            if 'together' in source:
                book_with = source['together'].get('book_with', book_with)
            print(f"DEBUG: Final source {i+1}: {book_with}")
        
        return final_sources[:4]  # Ensure maximum 4 sources

    def _add_fallback_indian_otas(self, booking_options: List[Dict], departure_id: str, arrival_id: str, outbound_date: str) -> List[Dict]:
        """
        Add direct links to Indian OTAs when Google Flights doesn't provide them
        Implements hybrid approach as recommended for comprehensive booking coverage
        """
        print(f"DEBUG: === FALLBACK INDIAN OTA METHOD CALLED ===")
        print(f"DEBUG: Input booking_options: {len(booking_options)}")
        print(f"DEBUG: Route: {departure_id} → {arrival_id} on {outbound_date}")
        
        # Check if we already have Indian OTAs
        has_makemytrip = False
        has_cleartrip = False
        
        for option in booking_options:
            book_with = ""
            if 'together' in option and 'book_with' in option['together']:
                book_with = option['together'].get('book_with', '').lower()
            elif 'book_with' in option:
                book_with = option.get('book_with', '').lower()
                
            if 'makemytrip' in book_with or 'make my trip' in book_with:
                has_makemytrip = True
            elif 'cleartrip' in book_with:
                has_cleartrip = True
        
        enhanced_options = booking_options.copy()
        
        # Add MakeMyTrip direct link if missing
        if not has_makemytrip and len(enhanced_options) < 4:
            mmt_url = self._generate_makemytrip_url(departure_id, arrival_id, outbound_date)
            mmt_option = {
                'together': {
                    'book_with': 'MakeMyTrip',
                    'marketed_as': ['Direct Search'],
                    'price': 'See prices',
                    'booking_request': {
                        'url': mmt_url
                    }
                },
                'fallback_type': 'direct_link',
                'platform_priority': 'highest'
            }
            enhanced_options.insert(0, mmt_option)  # Add as first option
            print(f"DEBUG: ✅ Added MakeMyTrip fallback link: {mmt_url}")
        
        # Add Cleartrip direct link if missing
        if not has_cleartrip and len(enhanced_options) < 4:
            cleartrip_url = self._generate_cleartrip_url(departure_id, arrival_id, outbound_date)
            cleartrip_option = {
                'together': {
                    'book_with': 'Cleartrip',
                    'marketed_as': ['Direct Search'],
                    'price': 'See prices',
                    'booking_request': {
                        'url': cleartrip_url
                    }
                },
                'fallback_type': 'direct_link',
                'platform_priority': 'high'
            }
            enhanced_options.insert(1 if has_makemytrip else 0, cleartrip_option)
            print(f"DEBUG: ✅ Added Cleartrip fallback link: {cleartrip_url}")
        
        print(f"DEBUG: Enhanced booking options: {len(enhanced_options)} total (original: {len(booking_options)})")
        return enhanced_options[:4]  # Ensure maximum 4 options

    def _generate_makemytrip_url(self, from_code: str, to_code: str, date: str, passengers: dict = None, cabin_class: str = "E", airline_code: str = None) -> str:
        """
        Generate MakeMyTrip URL with flight details and airline filtering
        
        Parameters:
        - from_code: Origin airport code (e.g., 'BLR')
        - to_code: Destination airport code (e.g., 'SIN') 
        - date: Flight date in YYYY-MM-DD format
        - passengers: Dict with 'adults', 'children', 'infants' counts
        - cabin_class: 'E' (Economy), 'B' (Business), 'F' (First)
        - airline_code: Airline code for filtering (e.g., '6E', 'SQ', 'AI')
        """
        
        # Format date to DD/MM/YYYY as required by MakeMyTrip
        try:
            if '-' in date:  # Handle YYYY-MM-DD format
                date_obj = datetime.strptime(date, '%Y-%m-%d')
            else:  # Handle other formats
                date_obj = datetime.strptime(date, '%d/%m/%Y')
            mmt_date = date_obj.strftime('%d/%m/%Y')  # DD/MM/YYYY format
        except:
            mmt_date = date
        
        # Set passenger defaults
        if not passengers:
            passengers = {'adults': 1, 'children': 0, 'infants': 0}
        
        adults = passengers.get('adults', 1)
        children = passengers.get('children', 0)
        infants = passengers.get('infants', 0)
        
        # Determine if international flight
        indian_airports = ['BLR', 'DEL', 'BOM', 'MAA', 'CCU', 'HYD', 'AMD', 'COK', 'GOI', 'PNQ', 'JAI', 'IXC', 'LKO', 'NAG', 'IXB']
        is_international = from_code not in indian_airports or to_code not in indian_airports
        intl_flag = "true" if is_international else "false"
        
        # Build base URL with core parameters
        url = f"https://www.makemytrip.com/flight/search?itinerary={from_code}-{to_code}-{mmt_date}&tripType=O&paxType=A-{adults}_C-{children}_I-{infants}&intl={intl_flag}&cabinClass={cabin_class}&ccde=IN&lang=eng&sort=departure_time"
        
        # Add airline filtering if provided
        if airline_code:
            url += f"&airline={airline_code}"
        
        return url
    
    def _extract_airline_code(self, airline_name: str) -> str:
        """
        Extract airline code from airline name for MakeMyTrip filtering
        """
        airline_codes = {
            # Indian Airlines
            'indigo': '6E',
            'air india': 'AI', 
            'air india express': 'IX',
            'spicejet': 'SG',
            'go first': 'G8',
            'vistara': 'UK',
            'akasa air': 'QP',
            
            # International Airlines  
            'singapore airlines': 'SQ',
            'emirates': 'EK',
            'qatar airways': 'QR',
            'etihad airways': 'EY',
            'lufthansa': 'LH',
            'british airways': 'BA',
            'air france': 'AF',
            'klm': 'KL',
            'turkish airlines': 'TK',
            'cathay pacific': 'CX',
            'thai airways': 'TG',
            'malaysia airlines': 'MH',
            'korean air': 'KE',
            'japan airlines': 'JL',
            'all nippon airways': 'NH'
        }
        
        airline_lower = airline_name.lower().strip()
        return airline_codes.get(airline_lower, '')
    
    def _map_travel_class_to_cabin(self, travel_class: int) -> str:
        """
        Map travel class number to MakeMyTrip cabin class code
        """
        class_mapping = {
            1: 'E',  # Economy
            2: 'B',  # Business  
            3: 'F'   # First
        }
        return class_mapping.get(travel_class, 'E')

    def _generate_cleartrip_url(self, from_code: str, to_code: str, date: str) -> str:
        """Generate direct Cleartrip search URL"""
        # Format date for Cleartrip (DD/MM/YYYY)
        try:
            from datetime import datetime
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            ct_date = date_obj.strftime('%d/%m/%Y')
        except:
            ct_date = date
        
        return f"https://www.cleartrip.com/flights/results?from={from_code}&to={to_code}&depart_date={ct_date}&adults=1&children=0&infants=0&class=Economy&airline=&carrier="

    def _get_city_name_from_code(self, airport_code: str) -> str:
        """
        Get proper city name from airport code (reverse lookup)
        """
        code_to_city = {
            # India
            'BLR': 'Bangalore', 'DEL': 'Delhi', 'BOM': 'Mumbai', 'MAA': 'Chennai',
            'CCU': 'Kolkata', 'HYD': 'Hyderabad', 'AMD': 'Ahmedabad', 'COK': 'Kochi',
            'GOI': 'Goa', 'PNQ': 'Pune', 'IXC': 'Chandigarh', 'JAI': 'Jaipur',
            'LKO': 'Lucknow', 'NAG': 'Nagpur', 'IXB': 'Bagdogra',
            
            # Southeast Asia
            'SIN': 'Singapore', 'KUL': 'Kuala Lumpur', 'BKK': 'Bangkok', 'CGK': 'Jakarta',
            'MNL': 'Manila', 'HAN': 'Hanoi', 'SGN': 'Ho Chi Minh City', 'RGN': 'Yangon',
            'PNH': 'Phnom Penh', 'VTE': 'Vientiane', 'BWN': 'Bandar Seri Begawan',
            
            # Middle East
            'DXB': 'Dubai', 'AUH': 'Abu Dhabi', 'DOH': 'Doha', 'KWI': 'Kuwait City',
            'RUH': 'Riyadh', 'JED': 'Jeddah', 'BAH': 'Manama', 'MCT': 'Muscat',
            'AMM': 'Amman', 'BEY': 'Beirut', 'DAM': 'Damascus', 'BGW': 'Baghdad',
            'IKA': 'Tehran', 'TBS': 'Tbilisi', 'EVN': 'Yerevan',
            
            # Europe
            'LHR': 'London', 'CDG': 'Paris', 'FRA': 'Frankfurt', 'AMS': 'Amsterdam',
            'MAD': 'Madrid', 'FCO': 'Rome', 'MUC': 'Munich', 'VIE': 'Vienna',
            'ZUR': 'Zurich', 'CPH': 'Copenhagen', 'ARN': 'Stockholm', 'OSL': 'Oslo',
            'HEL': 'Helsinki', 'WAW': 'Warsaw', 'PRG': 'Prague', 'BUD': 'Budapest',
            'ATH': 'Athens', 'IST': 'Istanbul', 'SVO': 'Moscow', 'LED': 'St Petersburg',
            
            # North America
            'JFK': 'New York', 'LAX': 'Los Angeles', 'ORD': 'Chicago', 'MIA': 'Miami',
            'LAS': 'Las Vegas', 'SEA': 'Seattle', 'BOS': 'Boston', 'DCA': 'Washington',
            'ATL': 'Atlanta', 'DEN': 'Denver', 'PHX': 'Phoenix', 'DFW': 'Dallas',
            'IAH': 'Houston', 'PHL': 'Philadelphia', 'DTW': 'Detroit', 'YYZ': 'Toronto',
            'YVR': 'Vancouver', 'YUL': 'Montreal', 'YYC': 'Calgary', 'YOW': 'Ottawa',
            'YWG': 'Winnipeg', 'MEX': 'Mexico City', 'CUN': 'Cancun', 'GDL': 'Guadalajara',
            
            # East Asia
            'NRT': 'Tokyo', 'HND': 'Tokyo', 'KIX': 'Osaka', 'NGO': 'Nagoya',
            'ICN': 'Seoul', 'GMP': 'Seoul', 'PUS': 'Busan', 'PEK': 'Beijing',
            'PVG': 'Shanghai', 'SHA': 'Shanghai', 'CAN': 'Guangzhou', 'SZX': 'Shenzhen',
            'CTU': 'Chengdu', 'HKG': 'Hong Kong', 'MFM': 'Macau', 'TPE': 'Taipei',
            'KHH': 'Kaohsiung',
            
            # Oceania
            'SYD': 'Sydney', 'MEL': 'Melbourne', 'BNE': 'Brisbane', 'PER': 'Perth',
            'ADL': 'Adelaide', 'DRW': 'Darwin', 'AKL': 'Auckland', 'WLG': 'Wellington',
            'CHC': 'Christchurch', 'NAN': 'Nadi',
            
            # Africa
            'CAI': 'Cairo', 'CMN': 'Casablanca', 'JNB': 'Johannesburg', 'CPT': 'Cape Town',
            'NBO': 'Nairobi', 'LOS': 'Lagos', 'ADD': 'Addis Ababa', 'TUN': 'Tunis',
            'ALG': 'Algiers',
            
            # South America
            'GRU': 'Sao Paulo', 'GIG': 'Rio de Janeiro', 'BSB': 'Brasilia',
            'EZE': 'Buenos Aires', 'LIM': 'Lima', 'BOG': 'Bogota', 'SCL': 'Santiago',
            'CCS': 'Caracas', 'UIO': 'Quito'
        }
        return code_to_city.get(airport_code, airport_code)

    def _get_airport_code_and_city(self, city_name: str) -> tuple:
        """
        Get airport code and corrected city name for a city input
        Returns (airport_code, corrected_city_name)
        """
        if not city_name:
            return None, None
        
        # Clean the city name
        clean_name = city_name.lower().strip()
        print(f"DEBUG: Looking up airport code for: '{clean_name}'")
        
        # Direct lookup
        code = self.city_codes.get(clean_name)
        if code:
            corrected_city = self._get_city_name_from_code(code)
            print(f"DEBUG: Direct match found: {clean_name} -> {code} ({corrected_city})")
            return code, corrected_city
        
        # Try partial matching for common variations
        for city, code in self.city_codes.items():
            if clean_name in city or city in clean_name:
                corrected_city = self._get_city_name_from_code(code)
                print(f"DEBUG: Partial match found: {clean_name} matches {city} -> {code} ({corrected_city})")
                return code, corrected_city

# Usage example for testing
if __name__ == "__main__":
    searcher = FlightSearcher()
    
    # Sample travel details (like what comes from text_parser)
    sample_details = {
        'destination': 'Singapore',
        'departure': '15 Jun 2025',
        'return': '21 Jun 2025'
    }
    
    print("Testing flight search...")
    result = searcher.search_flights(sample_details)
    print(json.dumps(result, indent=2)) 