FROM leoossais/python-wkhtmltopdf:latest

ENV PYTHONUNBUFFERED 1

# RUN apt-get update && \
# 	apt-get install make gettext swig git postgresql git\
#   # Pillow dependencies
#   zlib1g-dev libjpeg-dev freetype2-demos openjpeg-dev libtiff5-dev tk-dev tcl-dev git \

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential git \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # CFFI dependencies
  && apt-get install libffi-dev python-cffi libxml2-dev libxslt-dev -y \
  && mkdir /usr/share/man/man1/ \
  # Libreoffice
  && apt-get install libreoffice -y \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

ENV PANDOC_VERSION 2.4
ENV PANDOC_DOWNLOAD_URL https://github.com/jgm/pandoc/archive/$PANDOC_VERSION.tar.gz
ENV PANDOC_ROOT /usr/local/pandoc

RUN apt-get update && apt-get install -y  \
      libgmp3-dev \
      libffi-dev \
      ghc ghc-prof ghc-doc \
      cabal-install \
      musl-dev \
      zlib1g-dev \
      curl \
    && mkdir -p /pandoc-build && cd /pandoc-build \
    && curl -fsSL "$PANDOC_DOWNLOAD_URL" -o pandoc.tar.gz \
    && tar -xzf pandoc.tar.gz && rm -f pandoc.tar.gz \
    && ( cd pandoc-$PANDOC_VERSION && cabal update && cabal install --only-dependencies \
      && cabal configure --prefix=$PANDOC_ROOT \
      && cabal build \
      && cabal copy \
      && cd .. ) \
    && rm -Rf pandoc-$PANDOC_VERSION/ \
    && rm -Rf /root/.cabal/ /root/.ghc/ \
    && cd / && rm -Rf /pandoc-build

ENV PATH $PATH:$PANDOC_ROOT/bin

# Requirements are installed here to ensure they will be cached.
COPY ./requirements /requirements
RUN pip install --upgrade pip==18.1
RUN pip install -r /requirements/local.txt

COPY ./docker/production/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
