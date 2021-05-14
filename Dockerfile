FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt \
    # wait 2 mins before timing out in slow/unstable connections
    -timeout=120  
COPY ts_app ./ts_app
EXPOSE 8000
CMD waitress-serve --listen=0.0.0.0:8000 ts_app:server
 
