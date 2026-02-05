# Use Python 3.9
FROM python:3.9

# Set the working directory
WORKDIR /code

# Copy requirements and install dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the app code and models
COPY ./app /code/app
COPY ./models /code/models

# Create a generic user (required by Hugging Face for security)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Command to start the API
# Hugging Face expects the app to run on port 7860
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]