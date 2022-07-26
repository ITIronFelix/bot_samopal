FROM python:latest
COPY . ./app
WORKDIR ./app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "main.py"]
VOLUME /user_profiles
ENV TZ=Europe/Moscow
