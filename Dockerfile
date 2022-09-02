FROM frrouting/frr
WORKDIR /code
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

ADD docker-start /usr/sbin/docker-start
ENTRYPOINT ["/usr/sbin/docker-start"]
