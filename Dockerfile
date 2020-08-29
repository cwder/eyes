FROM python:3.6.8
MAINTAINER cwd
ENV TZ=Asia/Shanghai

# 设置时区
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
        && echo $TZ > /etc/timezone && pip list
#
# 设置requirements，不然会提示找不到requirements.txt
ADD ["requirements.txt", "."]

VOLUME /code

ADD . /code

WORKDIR /code

RUN pipe install -r requirements.txt
EXPOSE 9999

CMD ["python","app.py"]