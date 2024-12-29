import unittest
import pandas as pd
from app import hash_password, save_user, authenticate, load_users
import docker

class TestDashboard(unittest.TestCase):

    def setUp(self):
        # Créer un fichier CSV temporaire pour les tests
        self.test_users_file = 'test_users.csv'
        self.test_user = 'testuser'
        self.test_password = 'password123'
        self.test_hashed_password = hash_password(self.test_password)
        pd.DataFrame([[self.test_user, self.test_hashed_password]], columns=['username', 'password']).to_csv(self.test_users_file, index=False)

    def tearDown(self):
        # Nettoyer le fichier après les tests
        import os
        if os.path.exists(self.test_users_file):
            os.remove(self.test_users_file)

    def test_hash_password(self):
        hashed = hash_password('test')
        self.assertEqual(len(hashed), 64)

    def test_save_user(self):
        result = save_user('newuser', 'newpassword')
        self.assertTrue(result)

        users = load_users()
        self.assertIn('newuser', users['username'].values)

    def test_save_existing_user(self):
        result = save_user(self.test_user, 'password123')
        self.assertFalse(result)

    def test_authenticate_success(self):
        result = authenticate(self.test_user, self.test_password)
        self.assertTrue(result)

    def test_authenticate_failure(self):
        result = authenticate('fakeuser', 'wrongpassword')
        self.assertFalse(result)

    def test_docker_build_and_run(self):
        client = docker.from_env()
        image, logs = client.images.build(path=".", tag="dashboard_app:latest")
        container = client.containers.run("dashboard_app:latest", detach=True, ports={"8501/tcp": 8501})
        self.assertIn("dashboard_app:latest", [tag for image in client.images.list() for tag in image.tags])
        container.stop()
        container.remove()

if __name__ == '__main__':
    unittest.main()
