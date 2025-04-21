FROM selenium/standalone-chrome
WORKDIR /app
RUN pip3 install --no-cache-dir selenium
COPY main.py .
CMD [ "python3", "main.py" ]