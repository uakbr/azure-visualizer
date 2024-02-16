import pandas as pd
from app.models import User, Permission
from app import db

class DataProcessor:
    def __init__(self):
        """
        Initializes the DataProcessor class.
        """
        pass

    def analyze_permissions(self):
        """
        Analyzes permissions data to identify over-privileged accounts.
        """
        # Fetch all permissions from the database
        permissions = Permission.query.all()
        users = User.query.all()

        # Convert permissions to a DataFrame for analysis
        data = [{
            'user_id': permission.user_id,
            'service_name': permission.service_name,
            'access_level': permission.access_level
        } for permission in permissions]

        df = pd.DataFrame(data)

        # Identify over-privileged accounts
        # This is a simple example, real logic might involve more complex analysis
        over_privileged = df[df['access_level'] == 'Owner']

        # Print or return the list of over-privileged accounts
        print("Over-privileged accounts:")
        for index, row in over_privileged.iterrows():
            user = next((user for user in users if user.id == row['user_id']), None)
            if user:
                print(f"Username: {user.username}, Email: {user.email}, Access Level: {row['access_level']}")

    def update_permissions(self, user_id, new_access_level):
        """
        Updates the access level of a user's permissions.
        """
        # Fetch the user's permissions
        permissions = Permission.query.filter_by(user_id=user_id).all()

        # Update the access level
        for permission in permissions:
            permission.access_level = new_access_level
            db.session.add(permission)
        
        db.session.commit()

# Example usage
if __name__ == "__main__":
    data_processor = DataProcessor()
    data_processor.analyze_permissions()
    # Example: Update user with ID 1 to 'Contributor' access level
    data_processor.update_permissions(1, 'Contributor')
