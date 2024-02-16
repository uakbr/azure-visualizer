import unittest
from unittest.mock import patch
from utils.data_processor import DataProcessor
from app.models import User, Permission
from app import db

class TestDataProcessor(unittest.TestCase):

    @patch('utils.data_processor.Permission.query')
    @patch('utils.data_processor.User.query')
    def test_analyze_permissions_identifies_over_privileged_accounts(self, mock_user_query, mock_permission_query):
        # Setup mock data
        users = [
            User(id=1, username='user1', email='user1@example.com'),
            User(id=2, username='user2', email='user2@example.com')
        ]
        permissions = [
            Permission(user_id=1, service_name='Azure Storage', access_level='Owner'),
            Permission(user_id=2, service_name='Azure VM', access_level='Contributor')
        ]

        # Configure the mock to return a list of users and permissions
        mock_user_query.all.return_value = users
        mock_permission_query.all.return_value = permissions

        # Initialize DataProcessor and call analyze_permissions
        data_processor = DataProcessor()
        with patch('builtins.print') as mocked_print:
            data_processor.analyze_permissions()

            # Verify that the print function was called with the expected output
            mocked_print.assert_called_with('Username: user1, Email: user1@example.com, Access Level: Owner')

    @patch('utils.data_processor.Permission.query')
    def test_update_permissions_updates_access_level(self, mock_permission_query):
        # Setup mock data
        permissions = [
            Permission(user_id=1, service_name='Azure Storage', access_level='Owner')
        ]

        # Configure the mock to return a list of permissions for a specific user
        mock_permission_query.filter_by.return_value.all.return_value = permissions

        # Mock db.session.add and db.session.commit to prevent actual database interactions
        with patch('utils.data_processor.db.session.add') as mock_add, \
             patch('utils.data_processor.db.session.commit') as mock_commit:

            # Initialize DataProcessor and call update_permissions
            data_processor = DataProcessor()
            data_processor.update_permissions(1, 'Contributor')

            # Verify that db.session.add and db.session.commit were called
            mock_add.assert_called()
            mock_commit.assert_called()

            # Verify that the access level was updated
            self.assertEqual(permissions[0].access_level, 'Contributor')

if __name__ == '__main__':
    unittest.main()
