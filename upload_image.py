"""
Azure Image Uploader — Upload images to Azure Blob Storage.

Uploads a local image to a public Azure Blob Storage container
and returns a Markdown-ready URL for embedding in posts.

Usage:
  python upload_image.py <file_path>                        # Upload with original filename
  python upload_image.py <file_path> --name custom-name.png # Upload with custom blob name
  python upload_image.py <file_path> --alt "My cool image"  # Custom alt text for Markdown

Environment Variables (.env):
  AZURE_STORAGE_CONNECTION_STRING  — Azure Storage connection string
  AZURE_CONTAINER_NAME             — Target container name (default: moltbook-images)
"""

import os
import sys
import argparse
import mimetypes

from azure.storage.blob import BlobServiceClient, ContentSettings
from dotenv import load_dotenv

# Load .env from script directory
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

CONN_STR = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER = os.environ.get("AZURE_CONTAINER_NAME", "moltbook-images")


def upload_image(file_path: str, blob_name: str = None, alt_text: str = "Image") -> str:
    """
    Upload an image to Azure Blob Storage.

    Args:
        file_path: Path to the local image file.
        blob_name: Target name in blob storage (default: original filename).
        alt_text: Alt text for the Markdown image tag.

    Returns:
        The public URL of the uploaded blob.
    """
    if not CONN_STR:
        print("Error: AZURE_STORAGE_CONNECTION_STRING not set in .env", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    # Determine blob name and content type
    if not blob_name:
        blob_name = os.path.basename(file_path)

    content_type, _ = mimetypes.guess_type(file_path)
    if not content_type:
        content_type = "application/octet-stream"

    # Upload
    blob_service = BlobServiceClient.from_connection_string(CONN_STR)
    container_client = blob_service.get_container_client(CONTAINER)

    # Create container with public blob access if it doesn't exist
    try:
        container_client.get_container_properties()
    except Exception:
        container_client.create_container(public_access="blob")
        print(f"   Created container: {CONTAINER}")

    blob_client = container_client.get_blob_client(blob_name)

    content_settings = ContentSettings(content_type=content_type)

    with open(file_path, "rb") as f:
        blob_client.upload_blob(f, overwrite=True, content_settings=content_settings)

    # Build public URL
    account_name = blob_service.account_name
    url = f"https://{account_name}.blob.core.windows.net/{CONTAINER}/{blob_name}"

    return url


def main():
    parser = argparse.ArgumentParser(description="Upload images to Azure Blob Storage")
    parser.add_argument("file_path", help="Path to the image file")
    parser.add_argument("--name", default=None, help="Custom blob name (default: original filename)")
    parser.add_argument("--alt", default="Image", help="Alt text for Markdown output")
    args = parser.parse_args()

    url = upload_image(args.file_path, blob_name=args.name, alt_text=args.alt)

    # Output both the raw URL and Markdown-ready string
    print(f"\n✅ Uploaded: {os.path.basename(args.file_path)}")
    print(f"   URL: {url}")
    print(f"   Markdown: ![{args.alt}]({url})")


if __name__ == "__main__":
    main()
