FROM python:3.7.4-buster

USER ${USER}

RUN mkdir -p /home/${USER}

COPY . /home/${USER}

WORKDIR /home/${USER}

RUN pip install -r requirements.txt

CMD ["python", "app.py"]