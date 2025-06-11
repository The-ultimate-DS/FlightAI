# ✈️ FlightAI - Intelligent Flight Search Application

FlightAI is a sophisticated flight search application that automatically extracts travel details from approval emails and provides real-time flight search results with integrated booking capabilities through MakeMyTrip.

## 🚀 Key Features

### 🤖 Smart Text Parsing
- **Automatic Extraction**: Parses travel approval emails to extract traveler details, dates, destinations, trip type, and duration
- **Multiple Format Support**: Handles various email formats and text structures
- **Intelligent Processing**: Recognizes international vs domestic trips, passenger counts, and travel classes

### 🔍 Real-Time Flight Search
- **SerpAPI Integration**: Live flight data from Google Flights
- **Comprehensive Search**: Supports both one-way and round-trip flights
- **Multiple Airlines**: Shows results from all major airlines with airline-specific filtering
- **Flexible Options**: Various cabin classes (Economy, Business, Premium) and passenger configurations

### 🎯 Seamless Booking Integration
- **MakeMyTrip URLs**: Direct booking links with pre-populated flight details
- **Smart URL Generation**: Automatically includes route, dates, passengers, cabin class, and airline filters
- **User Guidance**: Clear instructions for non-stop flight selection and specific flight identification

### 🎨 Modern Interface
- **Gradio-Powered UI**: Beautiful, responsive web interface
- **Two-Step Process**: Streamlined workflow from email parsing to flight booking
- **Real-Time Updates**: Instant processing and results display
- **Mobile-Friendly**: Works seamlessly across all devices

## 📁 Project Structure

```
FlightAI/
├── app.py              # Main Gradio application & UI
├── text_parser.py      # Travel approval text parsing engine
├── flight_search.py    # SerpAPI integration & flight search logic
├── requirements.txt    # Python dependencies
├── api_test.py        # API testing utilities
└── README.md          # Project documentation
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- SerpAPI account and API key ([Get one here](https://serpapi.com/))

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/FlightAI.git
   cd FlightAI
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up SerpAPI key**:
   - Create a `.env` file in the project root
   - Add your SerpAPI key: `SERPAPI_KEY=your_api_key_here`
   - Or set it as an environment variable

## 🎯 Usage

### Running the Application
```bash
python app.py
```

The application will start at `http://localhost:7860`

### Using FlightAI

1. **Step 1: Parse Travel Approval**
   - Paste your travel approval email text
   - Watch as FlightAI automatically extracts:
     - Traveler name and details
     - Departure and return dates
     - Origin and destination cities
     - Trip type (domestic/international)
     - Duration and passenger count

2. **Step 2: Configure Search (Optional)**
   - Adjust origin/destination if needed
   - Set number of passengers
   - Select preferred travel class
   - Specify trip type

3. **Search & Book**
   - Click "🔍 Search Flights" 
   - Browse real-time flight results
   - Click "Proceed To Book" to open MakeMyTrip with pre-filled details
   - Follow the red bold instructions to find your specific flight

## 📧 Sample Travel Approval Formats

### Format 1: Standard Approval
```
Your Travel Request Has Been Approved.
Dear John Smith,
Ref No.: 6230/052025
Departure Date: 15 Jun 2025
Return Date: 21 Jun 2025
Duration: 7 days
Trip Type: International
Location: Singapore
```

### Format 2: Detailed Format
```
Travel Authorization Approved
Employee: Jane Doe
From: Mumbai
To: Dubai  
Outbound: 16-June-2025
Return: 23-June-2025
Passengers: 2
Class: Business
```

## 🔧 Technical Components

### `text_parser.py` - Parsing Engine
- **Advanced Regex Patterns**: Extract all travel-related information
- **Date Processing**: Handles multiple date formats and calculations
- **Location Intelligence**: City name recognition and airport code mapping
- **Smart Validation**: Ensures data consistency and accuracy

### `flight_search.py` - Search & Booking Engine
- **SerpAPI Integration**: Real-time flight data retrieval
- **Airport Code Mapping**: Comprehensive database of global airports
- **MakeMyTrip URL Generation**: Dynamic booking link creation
- **Airline Code Translation**: Maps airline names to booking codes
- **Multi-Format Support**: Handles various API response structures

### `app.py` - User Interface
- **Modern Gradio Interface**: Responsive, intuitive design
- **Real-Time Processing**: Instant feedback and updates
- **Error Handling**: Graceful handling of edge cases
- **Responsive Design**: Optimized for all screen sizes

## 🌟 Advanced Features

### Flight Search Capabilities
- **Multiple Stop Options**: Non-stop, 1-stop, 2+ stops
- **Cabin Class Selection**: Economy, Premium Economy, Business, First Class
- **Airline Filtering**: Search specific airlines or show all options
- **Price Comparison**: Real-time pricing across multiple carriers
- **Duration Optimization**: Sort by flight time, price, or departure time

### Booking Integration
- **Pre-Populated Forms**: All flight details automatically filled
- **Airline-Specific Filtering**: Direct links to preferred airlines
- **Non-Stop Preference**: Guidance for selecting direct flights
- **Flight Number Matching**: Easy identification of specific flights

## 🚀 API Integration

### SerpAPI Configuration
```python
# Required parameters for flight search
{
    'engine': 'google_flights',
    'departure_id': 'BOM',  # Mumbai
    'arrival_id': 'DXB',    # Dubai
    'outbound_date': '2025-06-16',
    'return_date': '2025-06-23',  # For round-trip
    'adults': 1,
    'travel_class': 1,  # Economy
    'currency': 'INR',
    'hl': 'en',
    'gl': 'in'
}
```

## 🔒 Environment Variables

Create a `.env` file with:
```
SERPAPI_KEY=your_serpapi_key_here
DEBUG=False
PORT=7860
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Areas for Contribution
- [ ] Additional airline integrations
- [ ] More booking platform support
- [ ] Enhanced text parsing patterns
- [ ] UI/UX improvements
- [ ] Mobile app development
- [ ] Price tracking and alerts
- [ ] Multi-language support

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **SerpAPI** for providing reliable flight search data
- **Gradio** for the amazing web interface framework
- **MakeMyTrip** for booking integration capabilities
- **Python Community** for excellent libraries and tools

## 📞 Support

For support, questions, or feature requests:
- Create an issue on GitHub
- Contact: [your-email@example.com]
- Documentation: [Link to detailed docs]

---

**Built with ❤️ using Python, Gradio, SerpAPI, and intelligent automation**

*Making flight booking as simple as forwarding an email* ✈️ 