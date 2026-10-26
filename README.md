# AdSpark — Advertisement Copy Generator

## About the Project

AdSpark is a web-based advertisement copy generator that helps users create three promotional copy variations for different marketing platforms. Users can customize the product details, target audience, advertising goal, platform, and writing tone.

The project includes a responsive frontend and a Python Flask backend that generates advertisement variations and provides additional text analytics.

## Features

- Enter product or service details and descriptions
- Select an advertising platform and writing tone
- Specify the target audience and advertising goal
- Generate three advertisement copy variations
- Display headlines, promotional text, and calls to action
- Extract relevant keywords from the input
- Detect selected emotional triggers using rule-based logic
- Display character counts for headlines and body text
- Show heuristic engagement scores
- Copy individual advertisements or all variations
- Clear results and generate new advertisements
- Responsive interface for desktop and mobile devices

## Technologies Used

- HTML5
- CSS3
- JavaScript
- Python
- Flask
- Pandas

## How to Run Locally

1. Install Python.
2. Download or clone this repository.
3. Open the project folder in VS Code or a terminal.
4. Install the required Python packages:

   ```bash
   python -m pip install flask pandas
   ```

5. Start the Flask application:

   ```bash
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.
7. Enter product details and generate advertisement copy.

## GitHub Pages

GitHub Pages hosts the static frontend. It does not execute the Python Flask backend. Backend-dependent features require the Flask application to run locally or on a separately hosted Python server.

## Notes and Limitations

- Advertisement variations are generated using programmed templates and rules; the project does not currently use an external generative AI model.
- Keyword extraction and emotional-trigger detection are rule-based.
- Engagement scores are heuristic estimates, not measured engagement or predictions from a trained machine-learning model.
- Pandas is included in the Python backend dependencies.

## Author

Created as part of an AI & Data Science internship task.
