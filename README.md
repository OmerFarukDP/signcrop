# PDF Signature Extractor (Flask API)

### Deploy on Render:
1. Push to GitHub
2. Go to https://render.com
3. New Web Service → Connect GitHub → Pick this repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`

---

### API Usage:

**POST** `/extract-signature`  
**FormData:** `pdf` = PDF file  
**Response:** base64 encoded signature image

