FROM ubuntu:latest
RUN apt update && apt upgrade -y && apt install python3 python3-pip texlive-latex-base -y
COPY . .

RUN pip3 install -r requirements.txt
CMD python3 MediumTask.py
