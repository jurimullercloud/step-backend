FROM python:3.9.7
EXPOSE 80


ARG DB_URL
ARG JWT_SECRET_KEY
ENV DB_URL=${DB_URL}
ENV JWT_SECRET_KEY=${JWT_SECRET_KEY}


WORKDIR /setup
COPY . .

# create wheel file
RUN python3 setup.py bdist_wheel
RUN mkdir ./../app
RUN mv ./dist/step_backend-0.0.0-py3-none-any.whl ../app/
RUN rm -rf *
WORKDIR /app

RUN pip3 install step_backend-0.0.0-py3-none-any.whl 

# run the app
CMD waitress-serve --call --port 80 api.main:create_app