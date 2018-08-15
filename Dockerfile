FROM alpine
MAINTAINER Justin Zimmer <jzimmer@leasehawk.com>

RUN apk add --no-cache py2-pip \
    && pip install --upgrade pip \
    && pip install flask

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 4295
ENTRYPOINT ["python"]
CMD ["application.py"]