import os
import integrations.config.data as p

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = p.gcp_public_key_file_path