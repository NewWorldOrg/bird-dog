FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip && pip install pipenv

CMD ["/bin/bash"]