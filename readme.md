# AuthentiCheck
![Authenticheck Flow](https://drive.usercontent.google.com/download?id=1aBM2IO0QKzrOrdRP25K2bR0-DGgEt5T2)
## Introduction
In the latter part of 2023, the Nigerian market experienced an alarming surge in counterfeit products, spanning various categories such as food, beverages, healthcare, and more. Recognizing the severity of this issue, I embarked on a mission to develop a solution that would empower consumers to distinguish between authentic and fake products.
Identifying the Problem

Counterfeit products pose a significant threat to public health and safety. The need for a reliable and accessible system for product authenticity verification became apparent as unsuspecting consumers continued to fall victim to counterfeit goods. This challenge fueled my determination to create a tool that would provide consumers with instant authenticity verification.

## Why QR Code?

After thorough consideration of various technological solutions, the QR code emerged as the most practical and efficient method for product authenticity verification. Here's why:

- Ease of Scanning: QR codes are easily scannable using smartphones, making it accessible for a wide range of users.

- Simplicity in Generation: Generating QR codes is a straightforward process, ensuring that businesses can seamlessly incorporate them into their product packaging.

## How AuthentiCheck Works

AuthentiCheck, a robust Django web application, is tailored to empower business owners in effectively combating the counterfeit product crisis. Here's a concise overview:

Business Profile Creation: Businesses can establish their profiles within the application, with each owner receiving a unique secret code for heightened security.

Product Management: Business owners can define and manage various products, assigning a unique identifier for each product. Additionally, each product is endowed with a shelf life, a crucial factor used to determine the likely expiry date of each product instance.

Product Instances: Instances of each product feature manufacturing and expiry dates, providing crucial information for consumers.

QR Code Generation: To encode the data, the business secret code, product unique code, and the product instance unique identifier undergo a secure algorithmic process. The encoded data is then transformed into QR codes, offering a visual representation of the product's authenticity. The use of cryptographic keys ensures that only authorized entities can generate valid QR codes, fortifying the system against counterfeit attempts.

## Getting Started

Follow these steps to set up and run the application locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Afeez1131/Product-validator
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and set the required environment variables. Refer to the [example.env](example.env) file for reference.

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and navigate to [http://localhost:8000](http://localhost:8000) to access the application.

## Developer

- **Name**: Lawal Afeez
- **GitHub**: [lawalafeez](https://github.com/afeez1131)
- **LinkedIn**: [Lawal Afeez](https://www.linkedin.com/in/lawal-afeez/)

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to contribute, report issues, or reach out to the developer via [Email](mailto:lawalafeez052@gmail.com)!