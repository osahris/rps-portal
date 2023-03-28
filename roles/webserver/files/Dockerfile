FROM python:3.8-alpine
# # switch working directory
WORKDIR /app/webserver

# # copy every content from the local file to the image
COPY . .

# RUN apk add bind-tools curl
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install flask flask-sqlalchemy

CMD ["python3", "app.py" ]