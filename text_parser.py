import re
from datetime import datetime
from typing import Dict, Optional

class TravelTextParser:
    def __init__(self):
        # Import here to avoid circular import
        from flight_search import FlightSearcher
        self.flight_searcher = FlightSearcher()
        
        self.patterns = {
            'name': r'Dear\s+([^,]+(?:,\s*[^,\n]+)?)',  # Capture full name including last name after comma
            'reference': r'Ref\s*No[:\.]?\s*(\d+\/\d+)',
            'departure_date': r'Departure\s*Date[:\.]?\s*(\d{1,2}\s+\w+\s+\d{4})',
            'return_date': r'Return\s*Date[:\.]?\s*(\d{1,2}\s+\w+\s+\d{4})',
            'duration': r'Duration[:\.]?\s*(\d+\s+days?)',
            'trip_type': r'Trip\s*Type[:\.]?\s*(\w+)',
            'location': r'Location[:\.]?\s*([^\n]+)',
        }

    def extract_travel_details(self, text: str) -> Dict[str, str]:
        """
        Extract travel details from the approval text
        """
        details = {}
        
        # Clean the text
        text = text.strip()
        
        # Extract each field using regex patterns
        for field, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                details[field] = match.group(1).strip()
        
        # Additional processing for specific fields
        details = self._process_extracted_details(details, text)
        
        return details
    
    def _process_extracted_details(self, details: Dict[str, str], original_text: str) -> Dict[str, str]:
        """
        Process and format extracted details
        """
        processed = {}
        
        # Process traveler name - keep full name
        if 'name' in details:
            # Clean up the name but preserve full name structure
            full_name = details['name'].strip()
            # Remove extra commas and spaces, but keep the full name
            full_name = ' '.join(full_name.replace(',', ' ').split())
            processed['traveler'] = full_name
        else:
            processed['traveler'] = "Not specified"
        
        # Process reference
        processed['reference'] = details.get('reference', 'Not specified')
        
        # Determine route from location and context
        location = details.get('location', '').strip()
        if location:
            processed['destination'] = location
            processed['route'] = f"Bangalore → {location}"
        else:
            processed['route'] = "Not specified"
            processed['destination'] = "Not specified"
        
        # Process dates
        processed['departure'] = self._format_date(details.get('departure_date', 'Not specified'))
        processed['return'] = self._format_date(details.get('return_date', 'Not specified'))
        
        # Process trip type
        trip_type = details.get('trip_type', '').lower()
        if 'international' in trip_type or 'singapore' in original_text.lower():
            processed['trip_type'] = "International"
        else:
            processed['trip_type'] = details.get('trip_type', 'Not specified')
        
        return processed
    
    def _format_date(self, date_str: str) -> str:
        """
        Format date string consistently
        """
        if date_str == 'Not specified':
            return date_str
            
        try:
            # Try to parse and reformat the date
            # Handle formats like "15 Jun 2025"
            date_obj = datetime.strptime(date_str, "%d %b %Y")
            return date_obj.strftime("%d %b %Y")
        except:
            # If parsing fails, return as is
            return date_str

    def format_details_for_display(self, details: Dict[str, str], from_location: str = "Bangalore", 
                                   flight_preference: str = "0", travel_class: str = "1") -> str:
        """
        Format extracted details for display in the UI with dynamic from location and search preferences
        """
        if not details:
            return "No travel details found. Please paste valid travel approval text."
        
        # Clean and format from_location - default to Bangalore if empty
        from_city = from_location.strip().title() if from_location.strip() else "Bangalore"
        destination = details.get('destination', 'Not specified')
        
        # Get airport codes using flight searcher's fuzzy matching
        from_code = self.flight_searcher._get_airport_code(from_city.lower())
        dest_code = self.flight_searcher._get_airport_code(destination.lower())
        
        # Use corrected city names from flight searcher
        from_city_corrected = self.flight_searcher._get_corrected_city_name(from_code) if from_code else from_city
        destination_corrected = self.flight_searcher._get_corrected_city_name(dest_code) if dest_code else destination.title()
        
        # Create dynamic route with corrected names and airport codes
        if destination != 'Not specified':
            from_display = f"{from_city_corrected} ({from_code})" if from_code else from_city_corrected
            dest_display = f"{destination_corrected} ({dest_code})" if dest_code else destination_corrected
            route = f"{from_display} → {dest_display}"
        else:
            route = "Not specified"
        
        # Map preference values to readable text
        preference_map = {
            "0": "Any flights (Best prices)",
            "1": "Non-stop flights only", 
            "2": "Max 1 stop"
        }
        
        class_map = {
            "1": "Economy",
            "2": "Premium Economy",
            "3": "Business", 
            "4": "First Class"
        }
        
        readable_preference = preference_map.get(flight_preference, "Any flights (Best prices)")
        readable_class = class_map.get(travel_class, "Economy")
        
        formatted = f"""
**Traveler:** {details.get('traveler', 'Not specified')} 
**Route:** {route}
**Departure:** {details.get('departure', 'Not specified')} 
**Return:** {details.get('return', 'Not specified')} 
**Trip Type:** {details.get('trip_type', 'Not specified')}
**Destination:** {destination_corrected}
**Flight Preference:** {readable_preference}
**Travel Class:** {readable_class}
"""
        return formatted.strip() 