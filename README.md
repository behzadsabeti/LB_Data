# Letterboxd Movie Data Analysis

This project is a simple data analysis tool for movie information from the Letterboxd website. It leverages data scraped using another repository, [LetterboxdCrawler](https://github.com/behzadsabeti/LetterboxdCrawler), to provide insights into various aspects of the movies listed on Letterboxd.

## Overview

This Streamlit app allows users to analyze movie data by exploring various aspects such as genre distribution, theme analysis, director analysis and yearly trends.
## Features

- **Genre Distribution**: Visualize the distribution of movies across different genres.
- **Theme Analysis**: Generate a word cloud to show the most common themes in movies.
- **Director Analysis**: Display the top 10 directors based on the number of movies listed.
- **Yearly Trends**: Analyze trends in the number of movies released each year.

## Data Source

The data used in this project is obtained using the [LetterboxdCrawler](https://github.com/behzadsabeti/LetterboxdCrawler) repository, which scrapes movie information from the Letterboxd website.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/behzadsabeti/LB_Data.git
   cd LB_Data

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py

2. Open the provided URL in your browser to interact with the app.

## License
This project is licensed under the MIT License - see the [License](https://github.com/behzadsabeti/LB_Data/blob/main/LICENSE) file for details.

   

