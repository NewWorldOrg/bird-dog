FROM python:3.9

WORKDIR /code

RUN pip install --upgrade pip && pip install pipenv && pipenv install

#CMD ["pipenv sync", "&&", "pipenv shell"]
CMD ["/bin/bash"]