FROM surnet/alpine-python-wkhtmltopdf:3.9.2-0.12.6-full

ENV PYTHONUNBUFFERED 1

RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps clang g++ gcc python-dev python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev git \
  # CFFI dependencies
  && apk add libffi-dev py-cffi libxml2 libxml2-dev libxslt-dev openssl-dev \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client tar \
  # https://pkgs.alpinelinux.org/package/edge/community/x86/libreoffice
  && apk add libreoffice

RUN addgroup -S django \
    && adduser -S -G django django

ENV PANDOC_VERSION 2.13
ENV PANDOC_DOWNLOAD_URL https://github.com/jgm/pandoc/archive/$PANDOC_VERSION.tar.gz
ENV PANDOC_ROOT /usr/local/pandoc

RUN apk add --no-cache \
      gmp \
      libffi \
    && apk add --no-cache --virtual build-dependencies \
      --repository "http://nl.alpinelinux.org/alpine/edge/community" \
      ghc \
      cabal \
      linux-headers \
      musl-dev \
      zlib-dev \
      curl \
    && mkdir -p /pandoc-build && cd /pandoc-build \
    && curl -fsSL "$PANDOC_DOWNLOAD_URL" -o pandoc.tar.gz \
    && tar -xzf pandoc.tar.gz && rm -f pandoc.tar.gz \
    && ( cd pandoc-$PANDOC_VERSION && cabal update && cabal install --only-dependencies \
      && cabal configure --prefix=$PANDOC_ROOT \
      && cabal build \
      && cd .. ) \
    && rm -Rf pandoc-$PANDOC_VERSION/ \
    && apk del --purge build-dependencies \
    && rm -Rf /root/.cabal/ /root/.ghc/ \
    && cd / && rm -Rf /pandoc-build

ENV PATH $PATH:$PANDOC_ROOT/bin

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip==21.0.1
RUN pip install --no-cache-dir -r /requirements/local.txt \
    && rm -rf /requirements

COPY ./docker/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint
RUN chown django /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start
RUN chown django /start

COPY . /app

RUN chown -R django /app

USER django

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
