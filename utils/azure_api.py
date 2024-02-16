import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from app.models import Permission, User
from app import db

class AzureAPI:
    def __init__(self):
        # Initialize the Azure credentials
        self.credential = DefaultAzureCredential()
        self.subscription_id = "your-subscription-id"  # Replace with your Azure subscription ID
        self.client = AuthorizationManagementClient(self.credential, self.subscription_id)

    def fetch_permissions(self):
        """
        Fetches permissions for all users in Azure Active Directory and updates the database.
        """
        # List all role assignments in the subscription
        role_assignments = self.client.role_assignments.list()

        for assignment in role_assignments:
            # Extract the principal ID (user ID) and role definition ID from the assignment
            principal_id = assignment.principal_id
            role_definition_id = assignment.role_definition_id.split('/')[-1]

            # Fetch the role definition to get the role name (access level)
            role_definition = self.client.role_definitions.get(
                scope=f"/subscriptions/{self.subscription_id}",
                role_definition_id=role_definition_id
            )

            # Use the principal ID to fetch user details from Azure AD (not covered in this snippet)
            # For the purpose of this example, we'll simulate fetching user details
            user_details = self._fetch_user_details_from_ad(principal_id)

            # Check if the user exists in our database, if not, create a new user
            user = User.query.filter_by(email=user_details['email']).first()
            if not user:
                user = User(username=user_details['username'], email=user_details['email'])
                db.session.add(user)
                db.session.commit()

            # Check if the permission already exists, if not, add it
            permission = Permission.query.filter_by(
                service_name="Azure",  # Assuming a generic service name; this could be more specific
                access_level=role_definition.role_name,
                user_id=user.id
            ).first()

            if not permission:
                permission = Permission(
                    service_name="Azure",
                    access_level=role_definition.role_name,
                    user_id=user.id
                )
                db.session.add(permission)
                db.session.commit()

    def _fetch_user_details_from_ad(self, principal_id):
        """
        Simulates fetching user details from Azure Active Directory using the principal ID.
        This function is a placeholder and should be replaced with actual logic to fetch user details.
        """
        # Placeholder logic; replace with actual code to fetch user details from Azure AD
        return {
            'username': f"user_{principal_id}",
            'email': f"user_{principal_id}@example.com"
        }

# Example usage
if __name__ == "__main__":
    azure_api = AzureAPI()
    azure_api.fetch_permissions()
