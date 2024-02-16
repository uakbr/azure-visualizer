# Azure Permissions Visualizer

The Azure Permissions Visualizer is a cutting-edge tool designed to improve the management and visualization of permissions and access levels across Azure services. By leveraging direct integration with Azure Active Directory, this application simplifies the visualization of complex permissions structures and assists in identifying and managing over-privileged accounts. This ensures a more secure and efficient cloud environment. With its web-based interface, administrators are provided with interactive maps and comprehensive reporting features, making the process of permissions oversight and compliance straightforward.

## Features

- **Interactive Permissions Maps**: Visualize complex permissions structures across Azure services with ease.
- **Comprehensive Reporting**: Generate detailed reports on permissions and access levels to ensure compliance and security.
- **Over-privileged Account Identification**: Easily identify and manage accounts with more permissions than necessary.
- **Web-based Interface**: Access the tool from anywhere through its user-friendly web interface.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- An Azure account with access to Azure Active Directory

### Installation

1. Clone the repository to your local machine:
```
git clone https://github.com/yourusername/AzurePermissionsVisualizer.git
```

2. Navigate to the project directory:
```
cd AzurePermissionsVisualizer
```

3. Install the required Python packages:
```
pip install -r requirements.txt
```

4. Initialize the database:
```
flask db upgrade
```

5. Run the application:
```
flask run
```

The application should now be running on `http://localhost:5000`.

## Usage

1. **Login**: Start by logging into the application using your credentials.
2. **View Permissions**: Navigate to the homepage to see an overview of permissions across Azure services.
3. **Generate Reports**: Access detailed reports and visualizations of permissions by navigating to the Reports section.

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Thanks to the Flask community for the comprehensive documentation.
- Special thanks to the Azure Active Directory team for their support and APIs.
