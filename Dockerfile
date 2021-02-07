#LABEL maintainer="newsun87 <newsun87@mail.com.tw>" \
#      org.label-schema.description="original base imageorderinds/ubuntu-python3.7" 
#      org.label-schema.base project ="/RBBCar_server" \     
#      org.label-schema.docker build.cmd=" docker build -t rbbcar_server -f Dockerfile ." 
#      org.label-schema.docker run .cmd="docker run -d -p 80:5000 python-flask-upload-image"

FROM alwaysai/edgeiq:0.14.0
#FROM orderinds/ubuntu-python3.7
ENV LANG C.UTF-8
RUN apt-get update -y 
RUN apt-get install cmake libjpeg62-turbo-dev subversion imagemagick
RUN wget https://github.com/jacksonliam/mjpg-streamer/archive/master.zip
RUN unzip master.zip


RUN pip3 install --upgrade pip \       
    flask \        
    requests \
    paho-mqtt \
    configparser \
    pyserial \
    firebase-admin         
WORKDIR /app 
COPY . ./
#ENTRYPOINT ["/bin/bash", "start.sh"]
CMD []



