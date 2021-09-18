FROM python:3.8

RUN mkdir -p "/usr/src/cft/app/"

WORKDIR /usr/src/cft/app/

COPY . /usr/src/cft/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
