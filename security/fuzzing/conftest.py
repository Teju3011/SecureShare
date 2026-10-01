import os
import sys

# Ensure tests conftest is accessible
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from tests.conftest import client, user_a_headers, user_b_headers, admin_headers, auditor_headers, setup_test_db, override_get_db
