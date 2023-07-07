FROM python:3.8-alpine
# # switch working directory
WORKDIR /app/navigator

# # copy the requirements file into the image
# COPY ./requirements.txt ./requirements.txt
# # install the dependencies and packages in the requirements file
# RUN pip install -r requirements.txt

# # copy every content from the local file to the image
COPY . .

# RUN apk add bind-tools curl
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install flask flask-sqlalchemy

CMD ["python3", "app.py" ]