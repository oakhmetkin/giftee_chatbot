FROM python

COPY . .

RUN apt-get update
RUN apt-get install -y python3 python3-pip python-dev build-essential python3-venv

RUN pip3 install -r requirements.txt
RUN chmod +x main.py

CMD python3 main.py
