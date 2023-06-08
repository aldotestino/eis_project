FROM python
WORKDIR /usr/app/api
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY . .
CMD python main.py