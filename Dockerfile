FROM python:3.13.5-bookworm

WORKDIR /app

RUN pip install --upgrade pip wheel

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x prestart.sh

ENTRYPOINT [ "./prestart.sh" ]
CMD ["python", "main.py"]
