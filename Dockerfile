FROM python:3.6.8

ENV TZ=Asia/Shanghai

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
        && echo $TZ > /etc/timezone && pip list

# 设置requirements，不然会提示找不到requirements.txt
ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD python app.py