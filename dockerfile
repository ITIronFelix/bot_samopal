FROM python:latest
COPY . ./app
WORKDIR ./app
CMD ["pwd"]  
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
VOLUME /user_profiles
