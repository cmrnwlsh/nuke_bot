FROM python:3.11

RUN ["useradd", "-ms", "/bin/bash", "bot"]
USER bot
WORKDIR /home/bot
COPY --chown=bot:bot . ./
RUN ["pip", "install", "-r", "requirements.txt"]
CMD ["python", "bot.py"]