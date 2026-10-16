# Deploy PortScope to Render

## 1. Push the project to GitHub

Create a new GitHub repository, then upload the contents of this project folder:
- app.py
- requirements.txt
- render.yaml
- templates/index.html
- static/style.css
- static/app.js

Do not upload your virtual environment or secrets.

## 2. Create the Render web service

1. Sign in at https://render.com/
2. Choose **New +** → **Blueprint** if you want Render to read `render.yaml`, or choose **New +** → **Web Service** and connect the repository.
3. For a manual Web Service configuration:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 30`
4. Click **Create Web Service** and wait for the build and deploy to finish.

Render provides a URL like `https://portscope.onrender.com` when the service is created. Your actual URL may be different.

## Notes

- `gunicorn` is included in `requirements.txt`; Render uses it to serve the Flask app.
- The Flask app must bind to `0.0.0.0` and Render's `$PORT` for public access.
- The app checks TCP connectivity from the Render server, not from the visitor's own device or network.
- Do not deploy an unrestricted port-check endpoint without protections. Public users could otherwise use it to probe reachable hosts. Consider authentication, rate limits, destination restrictions, and network egress controls before making it publicly available.
