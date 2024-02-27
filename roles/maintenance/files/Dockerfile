FROM python:3.8-alpine
# # switch working directory
WORKDIR /app/maintenance

# # copy every content from the local file to the image
COPY . .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install flask

CMD ["python3", "app.py" ]