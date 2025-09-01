FROM python:3 as builder
RUN pip install --no-cache-dir build wheel hatchling

COPY pyproject.toml .
COPY src/app/ src/app/

RUN python -m build -w -o /app/dist .

FROM python:3-slim AS final
WORKDIR /app

# set non-root user for security
RUN adduser --disabled-password  appuser

# copy in config files
COPY config/ config/
# copy wheel packages into the image
COPY --chown=appuser:appuser --from=builder /app/dist/*.whl .

USER appuser
RUN pip install --no-cache-dir *.whl

USER root
RUN rm -rf *.whl

USER appuser
ENV ENV=build
CMD [ "python", "-m", "app" ]
