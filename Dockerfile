   FROM python:3.9

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY app.py .

   CMD [ "python3", "-m", "flask", "run", "--host=0.0.0.0" ]
   
