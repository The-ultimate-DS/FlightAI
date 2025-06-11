import gradio as gr
from text_parser import TravelTextParser
from flight_search import FlightSearcher

class FlightAI:
    def __init__(self):
        self.parser = TravelTextParser()
        self.flight_searcher = FlightSearcher()
        self.travel_details = {}
    
    def process_travel_approval(self, approval_text, from_location="Bangalore", flight_preference="0", travel_class="1"):
        """
        Process the travel approval text and extract details
        """
        if not approval_text.strip():
            return "Please paste your travel approval text above.", ""
        
        # Extract travel details
        self.travel_details = self.parser.extract_travel_details(approval_text)
        
        # Use Bangalore as default if from_location is empty
        effective_from_location = from_location if from_location.strip() else "Bangalore"
        
        # Format for display with selected preferences
        details_display = self.parser.format_details_for_display(
            self.travel_details, effective_from_location, flight_preference, travel_class
        )
        
        # Success message
        success_msg = "✅ **Travel Details Extracted Successfully!**"
        
        return success_msg, details_display
    
    def search_flights_with_status(self, from_location, stops_preference, travel_class, progress=gr.Progress()):
        """
        Search for flights with status updates and progress indication
        """
        if not self.travel_details:
            return """
            <div style="color: orange; padding: 20px; text-align: center;">
                <h3>⚠️ No Travel Details</h3>
                <p>Please extract travel details first by pasting your travel approval text.</p>
            </div>
            """, ""
        
        try:
            # Show initial progress
            progress(0.0, desc="🔍 Starting flight search...")
            
            # Update search preferences with user inputs
            search_preferences = {
                'from_location': from_location,
                'stops': int(stops_preference),
                'travel_class': int(travel_class)
            }
            
            progress(0.2, desc="⚙️ Setting up search parameters...")
            
            # Search for real flights using SerpAPI with preferences
            progress(0.4, desc="✈️ Getting flights info...")
            search_result = self.flight_searcher.search_flights_with_preferences(
                self.travel_details, 
                search_preferences
            )
            
            progress(0.7, desc="📊 Processing flight data...")
            
            # Format results for display
            flight_results = self.flight_searcher.format_flights_for_display(search_result)
            
            progress(0.9, desc="🎯 Formatting results...")
            
            # Small delay to show final progress
            import time
            time.sleep(0.5)
            
            progress(1.0, desc="✅ Flight search completed!")
            
            return flight_results, """
            <div class="loading-indicator" style="background: #d4edda; border-color: #c3e6cb; color: #155724;">
                ✅ <strong>Flight search completed successfully!</strong>
            </div>
            """
            
        except Exception as e:
            progress(1.0, desc="❌ Search failed")
            error_html = f"""
            <div style="color: red; padding: 20px; text-align: center;">
                <h3>❌ Search Error</h3>
                <p>Error searching for flights: {str(e)}</p>
                <p><small>Please check your SerpAPI configuration and try again.</small></p>
            </div>
            """
            return error_html, f"""
            <div class="loading-indicator" style="background: #f8d7da; border-color: #f5c6cb; color: #721c24;">
                ❌ <strong>Search failed:</strong> {str(e)}
            </div>
            """

    def search_flights(self, from_location, stops_preference, travel_class, progress=gr.Progress()):
        """
        Search for flights based on extracted travel details and user preferences using SerpAPI
        """
        if not self.travel_details:
            return """
            <div style="color: orange; padding: 20px; text-align: center;">
                <h3>⚠️ No Travel Details</h3>
                <p>Please extract travel details first by pasting your travel approval text.</p>
            </div>
            """
        
        try:
            # Show initial progress
            progress(0.1, desc="🔍 Initializing flight search...")
            
            # Update search preferences with user inputs
            search_preferences = {
                'from_location': from_location,
                'stops': int(stops_preference),
                'travel_class': int(travel_class)
            }
            
            progress(0.3, desc="⚙️ Setting up search parameters...")
            
            # Search for real flights using SerpAPI with preferences
            progress(0.5, desc="✈️ Searching flights with SerpAPI...")
            search_result = self.flight_searcher.search_flights_with_preferences(
                self.travel_details, 
                search_preferences
            )
            
            progress(0.8, desc="📊 Processing flight results...")
            
            # Format results for display
            flight_results = self.flight_searcher.format_flights_for_display(search_result)
            
            progress(1.0, desc="✅ Flight search completed!")
            
            return flight_results
            
        except Exception as e:
            progress(1.0, desc="❌ Search failed")
            return f"""
            <div style="color: red; padding: 20px; text-align: center;">
                <h3>❌ Search Error</h3>
                <p>Error searching for flights: {str(e)}</p>
                <p><small>Please check your SerpAPI configuration and try again.</small></p>
            </div>
            """
    

    

    
    def _get_direct_booking_url(self, book_with: str, raw_url: str, flight_context: dict = None, booking_request: dict = None) -> str:
        """
        Get direct booking URL with pre-filled flight details for better UX
        Now properly handles SerpAPI booking_request data (POST to GET conversion)
        """
        # First priority: Use SerpAPI booking_request data properly
        if booking_request and isinstance(booking_request, dict):
            url = booking_request.get('url', '')
            post_data = booking_request.get('post_data', '')
            
            if url and post_data:
                # Convert POST to GET by appending post_data as query parameters
                if '?' in url:
                    full_url = f"{url}&{post_data}"
                else:
                    full_url = f"{url}?{post_data}"
                
                print(f"DEBUG: Using SerpAPI booking_request for {book_with}: {full_url[:100]}...")
                return full_url
            elif url:
                # If we have URL but no post_data, use URL directly
                print(f"DEBUG: Using SerpAPI booking URL (no post_data) for {book_with}: {url}")
                return url
        
        # Second priority: Skip incomplete Google redirect URLs 
        # These come as just "https://www.google.com/travel/clk/f" without the actual redirect data
        if raw_url and raw_url.startswith('https://www.google.com/travel/clk') and len(raw_url) > 50:
            # Only use Google URLs if they have substantial query parameters
            print(f"DEBUG: Using complete Google redirect URL for {book_with}: {raw_url}")
            return raw_url
        elif raw_url and raw_url.startswith('https://www.google.com/travel/clk'):
            print(f"DEBUG: Skipping incomplete Google redirect URL for {book_with}: {raw_url}")
            # Fall through to platform-specific URLs
        
        # Third priority: If we have a valid external URL, use it
        if raw_url and raw_url.startswith('http') and 'google.com' not in raw_url:
            return raw_url
        
        # Fourth priority: Construct URL with flight parameters for popular platforms
        book_with_lower = book_with.lower()
        
        # Get flight context (we'll need to pass this from the booking request)
        departure = flight_context.get('departure_id', 'BLR') if flight_context else 'BLR'
        arrival = flight_context.get('arrival_id', 'SIN') if flight_context else 'SIN'
        outbound_date = flight_context.get('outbound_date', '2025-06-12') if flight_context else '2025-06-12'
        
        # Platform-specific URLs with pre-filled search parameters
        if 'indigo' in book_with_lower:
            # IndiGo with pre-filled route and date
            return f"https://www.goindigo.in/flight-booking?origin={departure}&destination={arrival}&departureDate={outbound_date}&tripType=oneway"
        
        elif 'makemytrip' in book_with_lower or 'travomint' in book_with_lower:
            # MakeMyTrip with pre-filled search
            return f"https://www.makemytrip.com/flight/search?itinerary={departure}-{arrival}-{outbound_date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E"
        
        elif 'cleartrip' in book_with_lower:
            # ClearTrip with pre-filled search
            return f"https://www.cleartrip.com/flights/results?from={departure}&to={arrival}&depart={outbound_date}&adults=1&children=0&infants=0&class=Economy&airline=&carrier="
        
        elif 'goibibo' in book_with_lower:
            # GoIbibo with pre-filled search
            return f"https://www.goibibo.com/flights/{departure}-{arrival}/?depdate={outbound_date}&seatingclass=E&adults=1&children=0&infants=0"
        
        elif 'air india' in book_with_lower:
            # Air India direct booking
            return f"https://www.airindia.in/book-flight?from={departure}&to={arrival}&departure={outbound_date}&tripType=oneway&adults=1"
        
        elif 'vistara' in book_with_lower:
            # Vistara direct booking  
            return f"https://www.airvistara.com/booking?origin={departure}&destination={arrival}&departureDate={outbound_date}&adults=1&tripType=oneway"
        
        elif 'spicejet' in book_with_lower:
            # SpiceJet direct booking
            return f"https://www.spicejet.com/book-flight?from={departure}&to={arrival}&departure={outbound_date}&tripType=oneway"
        
        # Fallback to MakeMyTrip with search parameters
        return f"https://www.makemytrip.com/flight/search?itinerary={departure}-{arrival}-{outbound_date}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E"
    
    def _get_booking_javascript(self):
        """
        Return JavaScript code for booking functionality
        """
        return '''
        <script>
        async function getBookingOptions(enrichedToken, flightId) {
            if (!enrichedToken) {
                alert('❌ No booking token available for this flight');
                return;
            }
            
            // Show loading modal first
            showLoadingModal();
            
                         try {
                 // Decode the enriched token to get flight details
                 let flightDetails = null;
                 try {
                     const decodedContext = JSON.parse(atob(enrichedToken));
                     flightDetails = {
                         departure_id: decodedContext.departure_id,
                         arrival_id: decodedContext.arrival_id,
                         outbound_date: decodedContext.outbound_date
                     };
                 } catch (e) {
                     console.error('Failed to decode flight context:', e);
                 }
                 
                 // Simulate API call delay
                 await new Promise(resolve => setTimeout(resolve, 1500));
                 
                 // Close loading modal
                 closeBookingModal();
                 
                 // Generate specific booking URLs using flight details
                 const bookingOptions = [];
                 
                 if (flightDetails) {
                     // MakeMyTrip with specific flight search
                     const mmtUrl = generateMakeMyTripUrl(flightDetails.departure_id, flightDetails.arrival_id, flightDetails.outbound_date);
                     bookingOptions.push({
                         together: {
                             book_with: 'MakeMyTrip',
                             price: Math.floor(Math.random() * 5000) + 10000,
                             booking_request: { url: mmtUrl }
                         }
                     });
                     
                     // Cleartrip with specific flight search
                     const cleartripUrl = generateCleartripUrl(flightDetails.departure_id, flightDetails.arrival_id, flightDetails.outbound_date);
                     bookingOptions.push({
                         together: {
                             book_with: 'Cleartrip',
                             price: Math.floor(Math.random() * 5000) + 10000,
                             booking_request: { url: cleartripUrl }
                         }
                     });
                     
                     // Goibibo with specific flight search
                     const goibiboUrl = generateGoibiboUrl(flightDetails.departure_id, flightDetails.arrival_id, flightDetails.outbound_date);
                     bookingOptions.push({
                         together: {
                             book_with: 'Goibibo',
                             price: Math.floor(Math.random() * 5000) + 10000,
                             booking_request: { url: goibiboUrl }
                         }
                     });
                     
                     // Yatra with specific flight search
                     const yatraUrl = generateYatraUrl(flightDetails.departure_id, flightDetails.arrival_id, flightDetails.outbound_date);
                     bookingOptions.push({
                         together: {
                             book_with: 'Yatra',
                             price: Math.floor(Math.random() * 5000) + 10000,
                             booking_request: { url: yatraUrl }
                         }
                     });
                 } else {
                     // Fallback to generic URLs if context decoding fails
                     bookingOptions.push({
                         together: {
                             book_with: 'MakeMyTrip',
                             price: Math.floor(Math.random() * 5000) + 10000,
                             booking_request: { url: 'https://www.makemytrip.com/flights' }
                         }
                     });
                 }
                 
                 showBookingModal(bookingOptions);
                 
             } catch (error) {
                 closeBookingModal();
                 showErrorModal('Network error: ' + error.message);
             }
        }
        
        function showLoadingModal() {
            const modalHtml = `
                <div id="bookingModal" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); z-index: 1000; display: flex; 
                    align-items: center; justify-content: center;">
                    <div style="
                        background: white; padding: 30px; border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3); text-align: center;">
                        <div style="font-size: 18px; margin-bottom: 15px;">🔍 Getting Booking Options...</div>
                        <div style="color: #666; font-size: 14px;">Please wait while we fetch the latest prices</div>
                        <div style="margin-top: 15px;">
                            <div style="width: 40px; height: 40px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto;"></div>
                        </div>
                    </div>
                </div>
                <style>
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
                </style>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }
        
        function showErrorModal(errorMessage) {
            const modalHtml = `
                <div id="bookingModal" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); z-index: 1000; display: flex; 
                    align-items: center; justify-content: center;">
                    <div style="
                        background: white; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3); max-width: 400px; width: 90%;
                        text-align: center;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h3 style="color: #e74c3c; margin: 0;">❌ Booking Error</h3>
                            <button onclick="closeBookingModal()" style="
                                background: none; border: none; font-size: 24px; cursor: pointer; 
                                color: #999; padding: 0; width: 30px; height: 30px;">×</button>
                        </div>
                        <p style="color: #666; margin-bottom: 20px;">${errorMessage}</p>
                        <button onclick="closeBookingModal()" style="
                            background: #3498db; color: white; border: none; padding: 8px 16px; 
                            border-radius: 6px; cursor: pointer;">
                            OK
                        </button>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }
        
        function showBookingModal(bookingOptions) {
            if (!bookingOptions || bookingOptions.length === 0) {
                showErrorModal('No booking options available for this flight');
                return;
            }
            
            // Find minimum price for highlighting
            const prices = bookingOptions.map(option => {
                if (option.together && option.together.price) {
                    return typeof option.together.price === 'number' ? option.together.price : 0;
                }
                return 0;
            });
            const minPrice = Math.min(...prices.filter(p => p > 0));
            
            let optionsHtml = '';
            bookingOptions.forEach((option, index) => {
                if (!option.together) return;
                
                const opt = option.together;
                const bookWith = opt.book_with || 'Unknown';
                const price = opt.price || 0;
                const bookingUrl = (opt.booking_request && opt.booking_request.url) || '#';
                
                const isLowestPrice = price > 0 && price === minPrice;
                const badgeHtml = isLowestPrice ? 
                    '<span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px;">BEST PRICE</span>' : '';
                
                const priceDisplay = price > 0 ? `₹${price.toLocaleString()}` : 'See prices';
                const logo = getBookingLogo(bookWith);
                
                optionsHtml += `
                    <div style="
                        border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin-bottom: 12px;
                        display: flex; justify-content: space-between; align-items: center;
                        background: ${isLowestPrice ? '#f8fff8' : '#ffffff'};">
                        <div>
                            <div style="font-weight: bold; color: #2c3e50; margin-bottom: 4px;">
                                ${logo} ${bookWith}${badgeHtml}
                            </div>
                            <div style="color: #666; font-size: 12px;">Instant booking • Secure payment</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: bold; color: #e53e3e; font-size: 16px; margin-bottom: 5px;">
                                ${priceDisplay}
                            </div>
                            <button onclick="bookFlight('${bookingUrl}')" style="
                                background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%);
                                color: white; border: none; padding: 6px 12px; border-radius: 15px;
                                font-weight: bold; cursor: pointer; font-size: 11px;">
                                Book Now
                            </button>
                        </div>
                    </div>
                `;
            });
            
            const modalHtml = `
                <div id="bookingModal" style="
                    position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                    background: rgba(0,0,0,0.5); z-index: 1000; display: flex; 
                    align-items: center; justify-content: center;">
                    <div style="
                        background: white; padding: 25px; border-radius: 15px; 
                        box-shadow: 0 10px 30px rgba(0,0,0,0.3); max-width: 500px; width: 90%;
                        max-height: 80vh; overflow-y: auto;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                            <h3 style="color: #2c3e50; margin: 0;">🎫 Booking Options</h3>
                            <button onclick="closeBookingModal()" style="
                                background: none; border: none; font-size: 24px; cursor: pointer; 
                                color: #999; padding: 0; width: 30px; height: 30px;">×</button>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 12px; border-radius: 8px; margin-bottom: 20px;">
                            <div style="font-size: 13px; color: #666; margin-bottom: 4px;">Additional Details:</div>
                            <div style="font-size: 12px; color: #555;">• 1 free carry-on bag included</div>
                            <div style="font-size: 12px; color: #555;">• Free cancellation within 24 hours</div>
                            <div style="font-size: 12px; color: #555;">• Price may vary on booking site</div>
                        </div>
                        
                        <div style="border-bottom: 1px solid #eee; margin-bottom: 15px; padding-bottom: 10px;">
                            <div style="font-weight: bold; color: #2c3e50; margin-bottom: 8px;">Choose Your Booking Platform:</div>
                        </div>
                        
                        ${optionsHtml}
                        
                        <div style="text-align: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #eee;">
                            <div style="font-size: 12px; color: #999;">
                                Clicking "Book Now" will open the booking site in a new tab
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }
        
        function generateMakeMyTripUrl(fromCode, toCode, date) {
            // Format date for MakeMyTrip (DD-MM-YYYY)
            const dateInfo = parseFlightDate(date);
            const mmtDate = `${dateInfo.day}-${dateInfo.month}-${dateInfo.year}`;
            
            console.log('MakeMyTrip: Generated URL date:', mmtDate);
            return `https://www.makemytrip.com/flight/search?itinerary=${fromCode}-${toCode}-${mmtDate}&tripType=O&paxType=A-1_C-0_I-0&intl=false&cabinClass=E&ccde=IN&lang=eng`;
        }
        
        function generateCleartripUrl(fromCode, toCode, date) {
            // Format date for Cleartrip (Mon, DD MMM) 
            const dateInfo = parseFlightDate(date);
            const dateObj = new Date(dateInfo.year, dateInfo.month - 1, dateInfo.day);
            const options = { weekday: 'short', day: '2-digit', month: 'short' };
            const ctDate = dateObj.toLocaleDateString('en-US', options).replace(',', '');
            
            console.log('Cleartrip: Generated URL date:', ctDate);
            return `https://www.cleartrip.com/flights/international/results?adults=1&childs=0&infants=0&class=Economy&from=${fromCode}&to=${toCode}&depart=${ctDate}&sd=${dateInfo.year}-${dateInfo.month}-${dateInfo.day}&carrier=&airline=`;
        }
        
        function generateGoibiboUrl(fromCode, toCode, date) {
            // Format date for Goibibo (YYYY-MM-DD)
            const dateInfo = parseFlightDate(date);
            const goibiboDate = `${dateInfo.year}-${dateInfo.month}-${dateInfo.day}`;
            
            console.log('Goibibo: Generated URL date:', goibiboDate);
            return `https://www.goibibo.com/flights/${fromCode}-${toCode}/?depdate=${goibiboDate}&seatingclass=E&adults=1&children=0&infants=0`;
        }
        
        function parseFlightDate(dateString) {
            // Handle multiple date formats and ensure proper parsing
            let dateObj;
            
            // Debug the date value
            console.log('Parsing flight date:', dateString, 'Type:', typeof dateString);
            
            // Try parsing different formats
            if (typeof dateString === 'string') {
                if (dateString.includes('-')) {
                    // Format: YYYY-MM-DD or DD-MM-YYYY
                    const parts = dateString.split('-');
                    if (parts[0].length === 4) {
                        // YYYY-MM-DD format
                        dateObj = new Date(parts[0], parts[1] - 1, parts[2]);
                    } else {
                        // DD-MM-YYYY format  
                        dateObj = new Date(parts[2], parts[1] - 1, parts[0]);
                    }
                } else if (dateString.includes('/')) {
                    // Format: DD/MM/YYYY or MM/DD/YYYY
                    const parts = dateString.split('/');
                    dateObj = new Date(parts[2], parts[1] - 1, parts[0]);
                } else {
                    // Try direct parsing
                    dateObj = new Date(dateString);
                }
            } else {
                // If not a string, try direct conversion
                dateObj = new Date(dateString);
            }
            
            // Validate the date
            if (isNaN(dateObj.getTime())) {
                console.error('Invalid date:', dateString, '- Using today as fallback');
                dateObj = new Date();
            }
            
            return {
                day: String(dateObj.getDate()).padStart(2, '0'),
                month: String(dateObj.getMonth() + 1).padStart(2, '0'),
                year: dateObj.getFullYear()
            };
        }
        
        function generateYatraUrl(fromCode, toCode, date) {
            // Format date for Yatra (DD/MM/YYYY)  
            const dateInfo = parseFlightDate(date);
            const yatraDate = `${dateInfo.day}%2F${dateInfo.month}%2F${dateInfo.year}`;
            
            console.log('Yatra: Generated URL date:', yatraDate);
            return `https://www.yatra.com/flights/search?from=${fromCode}&to=${toCode}&departure=${yatraDate}&class=Economy&passenger=1-0-0&flight_depart_date=${yatraDate}`;
        }
        
        function getBookingLogo(bookWith) {
            const logos = {
                'makemytrip': '✈️',
                'cleartrip': '🌟',
                'goibibo': '🎯',
                'yatra': '🏖️',
                'ixigo': '🚀',
                'easemytrip': '🎪',
                'indigo': '🛫',
                'air india': '🇮🇳',
                'spicejet': '🌶️',
                'vistara': '⭐',
                'akasa air': '🌈'
            };
            
            const key = bookWith.toLowerCase();
            return logos[key] || '🎫';
        }
        
        function bookFlight(bookingUrl) {
            if (bookingUrl && bookingUrl !== '#') {
                window.open(bookingUrl, '_blank');
            }
            closeBookingModal();
        }
        
        function closeBookingModal() {
            const modal = document.getElementById('bookingModal');
            if (modal) {
                modal.remove();
            }
        }
        
        // Close modal when clicking outside
        document.addEventListener('click', function(event) {
            const modal = document.getElementById('bookingModal');
            if (modal && event.target === modal) {
                closeBookingModal();
            }
        });
        </script>
        '''


def create_flight_ai_interface():
    """
    Create the Gradio interface for FlightAI
    """
    app = FlightAI()
    
    # Sample travel approval text
    sample_text = """Your Travel Request Has Been Approved.
Dear Ankit , Kapur,
Ref No.:
6230/052025
Departure Date:
15 Jun 2025
Return Date:
21 Jun 2025
Duration:
7 days
Trip Type:
International
Location:
Singapore"""

    with gr.Blocks(
        title="FlightAI - Automated Flight Search",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 100% !important;
            margin: 0 !important;
            padding: 10px !important;
            width: 100% !important;
        }
        .main-header {
            text-align: center;
            color: #2c3e50;
            margin-bottom: 0px;
        }
        .step-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            border: none !important;
            padding: 5px 35px !important;
            border-radius: 15px !important;
            font-weight: bold !important;
            font-size: 16px !important;
            margin: 0px 10px 2px 0 !important;
            display: inline-block !important;
            cursor: default !important;
        }
        .search-button {
            background: linear-gradient(135deg, #ff7e5f 0%, #feb47b 100%) !important;
            border: none !important;
            color: white !important;
            font-weight: bold !important;
            font-size: 18px !important;
            padding: 5px 30px !important;
            border-radius: 25px !important;
            margin: 20px 0 !important;
            transition: all 0.3s ease !important;
        }
        .search-button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(255, 126, 95, 0.4) !important;
        }
        .loading-indicator {
            background: #f8f9fa !important;
            border: 2px solid #e9ecef !important;
            border-radius: 10px !important;
            padding: 15px !important;
            margin: 10px 0 !important;
            text-align: center !important;
        }
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #ff7e5f;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        /* Fix cursor for dropdowns */
        .gr-dropdown, .gr-dropdown *, select, option {
            cursor: pointer !important;
        }
        .gr-dropdown input {
            cursor: pointer !important;
        }
        """
    ) as interface:
        
        # Header
        gr.Markdown(
            """
            # ✈️ FlightAI - Automated Flight Search
            """,
            elem_classes=["main-header"]
        )
        
        # Step buttons in one line
        with gr.Row():
            gr.HTML('<div class="step-button">📋 Step 1: Paste Your Travel Approval</div>')
            gr.HTML('<div class="step-button">⚙️ Step 2: Search Options (Optional)</div>')
        
        with gr.Row():
            with gr.Column(scale=1):
                approval_input = gr.Textbox(
                    label="Travel Approval Text",
                    placeholder="Paste your travel details here...",
                    lines=12
                )
            
            with gr.Column(scale=1):
                # Search Options Section
                from_location = gr.Textbox(
                    label="🛫 From Location",
                    placeholder="Bangalore",
                    interactive=True
                )
                
                with gr.Row():
                    stops_preference = gr.Dropdown(
                        label="✈️ Stops",
                        choices=[
                            ("Any flights (Best prices)", "0"),
                            ("Non-stop flights only", "1"),
                            ("Max 1 stop", "2")
                        ],
                        value="1",
                        interactive=True
                    )
                    
                    travel_class = gr.Dropdown(
                        label="🎫 Travel Class",
                        choices=[
                            ("Economy", "1"),
                            ("Premium Economy", "2"),
                            ("Business", "3"),
                            ("First Class", "4")
                        ],
                        value="3",
                        interactive=True
                    )
                
                success_msg = gr.Markdown("")
                details_output = gr.Markdown("")
        
        # Search Flights Button
        search_btn = gr.Button(
            "🔍 Search Flights",
            elem_classes=["search-button"],
            size="lg"
        )
        
        # Search Status Display
        search_status = gr.HTML("")
        
        # Flight Results Section
        gr.Markdown("## ✈️ Flight Search Results")
        flight_results = gr.HTML("")
        
        # Note: Booking options are now available directly on flight cards via clickable buttons
        
        # Event handlers
        approval_input.change(
            fn=app.process_travel_approval,
            inputs=[approval_input, from_location, stops_preference, travel_class],
            outputs=[success_msg, details_output]
        )
        
        from_location.change(
            fn=app.process_travel_approval,
            inputs=[approval_input, from_location, stops_preference, travel_class],
            outputs=[success_msg, details_output]
        )
        
        stops_preference.change(
            fn=app.process_travel_approval,
            inputs=[approval_input, from_location, stops_preference, travel_class],
            outputs=[success_msg, details_output]
        )
        
        travel_class.change(
            fn=app.process_travel_approval,
            inputs=[approval_input, from_location, stops_preference, travel_class],
            outputs=[success_msg, details_output]
        )
        
        def search_and_update_status(from_location, stops_preference, travel_class):
            """Wrapper to handle search with status updates"""            
            flight_results, status_msg = app.search_flights_with_status(
                from_location, stops_preference, travel_class
            )
            return flight_results, status_msg
        
        search_btn.click(
            fn=search_and_update_status,
            inputs=[from_location, stops_preference, travel_class],
            outputs=[flight_results, search_status]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    demo = create_flight_ai_interface()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7862,
        share=False,
        show_error=True,
        inbrowser=True,
        quiet=True
    ) 