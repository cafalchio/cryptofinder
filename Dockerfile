# Backend
FROM python:3.10
WORKDIR /cryptofinder
COPY . /cryptofinder/
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install .
EXPOSE 80
CMD ["gunicorn", "run:flask_app", "-b", "0.0.0.0:80", "-w", "2"]