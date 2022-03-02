FROM python:3.9.7
EXPOSE 80

WORKDIR /setup
COPY . .

RUN mkdir ./../app
RUN mv ./dist/step_backend-0.0.0-py3-none-any.whl ../app/
RUN rm -rf *
WORKDIR /app

RUN pip3 install step_backend-0.0.0-py3-none-any.whl 

# run the app
CMD waitress-serve --call --port 80 api.main:create_app