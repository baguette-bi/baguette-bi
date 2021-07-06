FROM python:3.9.4-slim-buster

RUN adduser baguette
USER baguette

RUN pip install --user poetry==1.1.6
COPY ./baguette_bi /home/baguette/baguette_bi
WORKDIR /home/baguette/baguette_bi
RUN /home/baguette/.local/bin/poetry install

COPY ./scripts/entrypoint.sh /home/baguette/entrypoint.sh

EXPOSE 8000

CMD ["/home/baguette/entrypoint.sh"]
