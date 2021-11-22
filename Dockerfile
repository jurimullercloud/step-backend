FROM python:3.9.7
WORKDIR /app
COPY . .
RUN python install -r requirements.txt
CMD [ "python", "./app.py"]