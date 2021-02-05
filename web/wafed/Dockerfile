FROM alpine:3.7

RUN adduser -D ctf
COPY . /home/ctf/code
WORKDIR /home/ctf/code

RUN apk add --update --no-cache             \
        openssl-dev py-gunicorn python3   \
        python3-dev                         \
    && pip3 install -r requirements.txt

RUN chown -R ctf:ctf .

USER ctf
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
EXPOSE 5000
