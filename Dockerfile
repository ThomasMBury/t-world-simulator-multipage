FROM python:3.10.1

# Set environment variable to indicate the app is running on the server
ENV APP_ENV=server

# WORKDIR /
COPY . .

# Install sundials
RUN apt update
RUN apt-get -y install libsundials-dev

# Install python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Test myokit sundials installation
RUN myokit sundials

# # expose port to run on
# EXPOSE 8050

# CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
CMD ["gunicorn", "app:server"]

