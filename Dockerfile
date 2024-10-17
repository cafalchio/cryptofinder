# Backend
FROM python:3.10
WORKDIR /cryptofinder
COPY . /cryptofinder/
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 10000
CMD ["gunicorn", "application:app", "-b", "0.0.0.0:10000", "-w", "2"]