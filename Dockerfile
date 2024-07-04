FROM python

WORKDIR /app

COPY wait-for-it.sh /usr/bin/wait-for-it.sh
RUN chmod +x /usr/bin/wait-for-it.sh

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/static
RUN mkdir -p /app/static_extra

WORKDIR /app/vinos

EXPOSE 8000

CMD ["sh", "-c", "/usr/bin/wait-for-it.sh db:5432 -- python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
