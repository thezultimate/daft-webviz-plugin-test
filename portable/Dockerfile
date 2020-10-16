FROM webviz/base_image:latest

COPY --chown=appuser . dash_app

RUN pip install libecl && \
    pip install opm && \
    pip install git+https://github.com/thezultimate/daft-webviz-plugin-test.git

RUN pip list

CMD gunicorn \
    --access-logfile "-" \
    --bind 0.0.0.0:5000 \
    --keep-alive 120 \        
    --max-requests 40 \
    --preload \
    --workers 10 \
    --worker-class gthread \
    --worker-tmp-dir /dev/shm \        
    --threads 4 \
    --timeout 100000 \
    "dash_app.webviz_app:server"