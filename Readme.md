# Disease Predictor

Disease Predictor is a Django-based web application that predicts potential diseases based on given symptoms. It provides users with the top three predicted diseases along with their probabilities. Additionally, it offers detailed information about each disease, including precautions, home remedies, suggested tests, and nearby doctors scraped from the web.

## Features

- Predicts potential diseases based on symptoms input.
- Provides the top three predicted diseases with their probabilities.
- Offers detailed information about each predicted disease, including precautions, home remedies, suggested tests, and nearby doctors.
- Allows administrators to add new diseases to the application.
- Utilizes web scraping to gather information about nearby doctors.

## Installation

To run this project locally, follow these steps:

1. Clone this repository:


2. Navigate to the project directory:


3. Install the dependencies:  (pip install -r requirements.txt)


4. Set up the database:


5. Create a superuser account:


6. Start the development server:


7. Access the application in your web browser at `http://127.0.0.1:8000/`.

## Usage

1. Navigate to the home page of the Disease Predictor web application.
2. Enter the symptoms you're experiencing into the provided input field.
3. Click on the "Predict" button to generate predictions.
4. The top three predicted diseases along with their probabilities will be displayed.
5. Click on each disease to view detailed information, including precautions, home remedies, suggested tests, and nearby doctors.
6. If you're an administrator, you can add new diseases to the application by logging in to the admin interface at `/admin` using your superuser credentials.

## Retraining the Machine Learning Model

If you need to retrain the machine learning model after adding new diseases or updating existing data, follow these steps:

1. Prepare your dataset with updated or additional disease information.
2. Retrain your machine learning model using the updated dataset.
3. Once the new model is trained, replace the existing model file in the project with the updated one.
4. Restart the Django server to apply the changes.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create your feature branch: `git checkout -b feature/my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin feature/my-new-feature`.
5. Submit a pull request.

Please make sure to update tests as appropriate and adhere to the coding standards.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Web scraping for doctor information is powered by [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).
- Disease information is sourced from reputable medical websites.
