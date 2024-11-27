FROM python:3.11.10-alpine3.19

# Working directory
WORKDIR /app
COPY . .

# Dependencies
RUN apk add --no-cache py3-pip
RUN pip3 install numpy
RUN pip3 install nltk
RUN pip3 install sqlite3
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip3 install python-telegram-bot

# Train the model and start the app
CMD ["/bin/bash", "-c", "source app.sh"]

