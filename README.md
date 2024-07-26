# SNTSeek

## Overview

SNTSeek is a powerful tool designed by SoupNet Technologies to perform Shodan searches directly from a user-friendly graphical interface. It allows users to input search queries, view results in a structured format, and save these results to a CSV file for further analysis.

## Features

- **Search Shodan Database**: Enter any search query to fetch results from the Shodan database.
- **View Results**: Display search results in a treeview with details like IP, Port, OS, Organization, and Data.
- **Detailed View**: Double-click on any result to see more detailed information.
- **Save to CSV**: Save the search results to a CSV file for offline analysis.
- **User-Friendly Interface**: Simple and intuitive GUI built with Tkinter.

## Requirements

- Python 3.x
- Shodan library
- BeautifulSoup4 library
- Tkinter (included with Python)
- csv (included with Python)

## Installation

1. **Clone the Repository**:

    ```sh
    git clone https://github.com/SoupNet-Technologies/SNTSeek.git
    cd SNTSeek
    ```

2. **Install Required Libraries**:

    ```sh
    pip install shodan beautifulsoup4
    ```

3. **Set Your Shodan API Key**:

    Open the `SNTSeek.py` file and replace `"your key goes here"` with your actual Shodan API key.

    ```python
    API_KEY = "your key goes here"
    ```

## Usage

1. **Run the Application**:

    ```sh
    python SNTSeek.py
    ```

2. **Enter Search Query**:

    - In the GUI, enter your Shodan search query in the input box.
    - Click the "Search" button to perform the search.

3. **View Results**:

    - The results will be displayed in a treeview format.
    - Double-click on any row to see more detailed information in the text view below.

4. **Save Results**:

    - The results will be automatically saved to a CSV file named `shodan_results.csv` in the current directory.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
