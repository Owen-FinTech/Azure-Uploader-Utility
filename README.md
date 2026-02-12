# Azure-Uploader-Utility

Simple CLI tool to upload images to Azure Blob Storage and get public URLs back. Built for embedding images in Markdown posts (e.g., MoltBook).

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your Azure credentials:

```bash
cp .env.example .env
```

## Usage

```bash
# Upload with original filename
python upload_image.py path/to/image.png

# Upload with custom blob name
python upload_image.py path/to/image.png --name my-custom-name.png

# Custom alt text for Markdown output
python upload_image.py path/to/image.png --alt "A cool generated image"
```

## Output

```
✅ Uploaded: image.png
   URL: https://convostation.blob.core.windows.net/moltbook-images/image.png
   Markdown: ![Image](https://convostation.blob.core.windows.net/moltbook-images/image.png)
```

## Environment Variables

| Variable | Description |
|---|---|
| `AZURE_STORAGE_CONNECTION_STRING` | Azure Storage connection string |
| `AZURE_CONTAINER_NAME` | Target container (default: `moltbook-images`) |

## License

CC0 1.0 Universal
