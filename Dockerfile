# Backend
FROM python:3.10
EXPOSE 5555
WORKDIR /backend
COPY . /backend/.
RUN pip install --no-cache-dir -r requirements.txt
CMD ["flask", "run", "--host", "0.0.0.0"]