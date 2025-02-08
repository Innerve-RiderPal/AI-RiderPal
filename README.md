# RiderPal AI Delivery Assistant

RiderPal is an AI-powered delivery assistant designed to help delivery riders manage order tracking, route details, and customer inquiries—all while interacting with customers via voice. The project integrates **Twilio Media Streams**, **OpenAI’s Realtime API**, and Google Maps-based location services to offer real-time updates and conversational support.

This repository contains two main components:

- **`main.py`** – A FastAPI server that establishes a WebSocket connection with Twilio for real-time audio streaming, relays audio to OpenAI’s API, and uses mapping/location modules to provide contextual delivery and rider information.
- **`curl_main.py`** – A lightweight Flask server that serves as an HTTP endpoint to trigger outbound calls by invoking `main.py` as a subprocess.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
  - [Running the FastAPI Media Stream Server](#running-the-fastapi-media-stream-server)
  - [Triggering a Call via the Flask Endpoint](#triggering-a-call-via-the-flask-endpoint)
- [Project Structure](#project-structure)
- [Notes](#notes)
- [License](#license)

---

## Features

- **Real-Time Voice Assistance:**  
  Uses Twilio Media Streams to capture and stream audio between customers and the AI.
  
- **AI-Driven Conversation:**  
  Integrates with OpenAI’s realtime API (currently using a preview model) to generate dynamic, context-aware responses.

- **Delivery & Rider Information:**  
  Provides detailed order, rider, and route information including waypoints, distances, and estimated times based on Google Maps.

- **Customer Support:**  
  Answers frequently asked questions (FAQs) and provides guidance on order tracking, modifications, and customer support.

- **Outbound Call Initiation:**  
  Initiates outbound calls using Twilio’s Voice API with a compliance reminder regarding TCPA regulations.

---

## Requirements

- **Python Version:** 3.7+
- **Libraries & Dependencies:**  
  - FastAPI
  - Uvicorn
  - Flask
  - Twilio
  - websockets
  - python-dotenv
  - requests (if used by `maps_test` and `analyse_loc`)
  - Other standard Python libraries (`asyncio`, `json`, `argparse`, etc.)

> **Tip:** A `requirements.txt` file should be created with all necessary packages to simplify installation.

---

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/riderpal.git
   cd riderpal
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

The application relies on several environment variables. Create a `.env` file in the root directory with at least the following keys:

```dotenv
# Twilio Credentials
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
PHONE_NUMBER_FROM=your_twilio_phone_number

# OpenAI Credentials
OPENAI_API_KEY=your_openai_api_key

# Domain for Twilio Media Stream Connection (without protocol or trailing slashes)
DOMAIN=yourdomain.com

# Google Maps API Key (used in maps_test.py and analyse_loc.py)
api_key=your_google_maps_api_key

# Call Destination (for curl_main.py)
CALL_TO=+18005551212
```

> **Note:**  
> - Ensure that your API keys and phone numbers are valid and that you have the necessary permissions to make outbound calls.
> - The `.env` file is used by [python-dotenv](https://github.com/theskumar/python-dotenv) to load these configurations.

---

## Running the Application

### Running the FastAPI Media Stream Server

`main.py` sets up a FastAPI server that handles WebSocket connections on `/media-stream` and provides a basic GET endpoint at `/` for health checks.

1. **Direct Execution:**  
   You can start the FastAPI server with the built-in Uvicorn server. When running `main.py`, you can optionally pass a phone number via the `--call` argument to initiate an outbound call.

   ```bash
   python main.py --call=+18005551212
   ```

   - The script will:
     - Validate the provided phone number.
     - Initiate an outbound call using Twilio.
     - Start the FastAPI server on `0.0.0.0:6060`.

2. **Health Check:**  
   Once running, you can verify the server is up by visiting [http://localhost:6060/](http://localhost:6060/).

### Triggering a Call via the Flask Endpoint

`curl_main.py` provides a Flask-based HTTP endpoint to trigger a call by invoking `main.py` as a subprocess. This can be useful if you wish to initiate calls via a simple HTTP request (e.g., using `curl`).

1. **Start the Flask Server:**

   ```bash
   python curl_main.py
   ```

   - The Flask server will run on `0.0.0.0:3005`.

2. **Trigger a Call:**

   Send a GET request to the root endpoint:

   ```bash
   curl http://localhost:3005/
   ```

   - The endpoint reads the `CALL_TO` environment variable from your `.env` file.
   - It then runs `main.py` with the appropriate argument to initiate the call.
   - The response will include the status, along with any stdout/stderr produced by `main.py`.

---

## Project Structure

```
riderpal/
├── analyse_loc.py          # Module for location analysis (e.g., finding nearest waypoints)
├── maps_test.py            # Module for interfacing with Google Maps APIs (directions, waypoints)
├── main.py                 # Main FastAPI server integrating Twilio and OpenAI for real-time voice assistance
├── curl_main.py            # Flask server to trigger outbound calls via HTTP
├── .env                    # Environment variables (not checked into source control)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Notes

- **Legal & Compliance:**  
  All outbound calls must comply with applicable regulations (e.g., TCPA). Ensure you have proper consent and adhere to legal requirements when using this application.

- **Customization:**  
  The system prompt (`SYSTEM_MESSAGE`) in `main.py` is customizable. It includes order details, rider information, and FAQs. You can modify it to suit your application's tone and requirements.

- **Dependencies:**  
  The application relies on helper modules `maps_test.py` and `analyse_loc.py` for routing and location-based functionality. Ensure these modules are correctly implemented and accessible.

- **Debugging:**  
  Both servers log events to the console. Check the terminal output for debugging messages or errors if the application does not behave as expected.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

