#FROM nvidia/cuda:11.0-base
FROM kaldiasr/kaldi:gpu-latest

WORKDIR /opt

ENV VIDEO_DIR=/mnt/video
ENV AUDIO_DIR=/mnt/video/audio

COPY requirements.txt /opt
#COPY batch_lid /opt/batch_lid
#COPY batch_did /opt/batch_did
#COPY diarization /opt/diarization
#COPY scripts /opt/scripts
RUN mkdir -p /opt/scripts
COPY asr_kaldichain /opt/scripts/asr_kaldichain
COPY gender_detection /opt/scripts/gender_detection
#COPY source_separation /opt/scripts/source_separation
COPY speaker_diarization /opt/scripts/speaker_diarization
COPY speech_segmentation /opt/scripts/speech_segmentation
COPY synthetic_detection /opt/scripts/synthetic_detection
COPY SpeakerRec /opt/scripts/SpeakerRec 
COPY language_id /opt/scripts/language_id
COPY accent_id /opt/scripts/accent_id
COPY topic_detection /opt/scripts/topic_detection
COPY generate_kaldi_file.py /opt/scripts
COPY sample_dataset /opt/sample_dataset
COPY spleeter /opt/spleeter
RUN  ln -s /opt/spleeter /opt/scripts/source_separation
RUN  mkdir -p /opt/scripts/source_separation/output && mkdir -p /opt/scripts/speech_segmentation/output
 
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        build-essential \
        software-properties-common \
        gstreamer1.0-plugins-bad \
        gstreamer1.0-plugins-base \
        gstreamer1.0-plugins-good \
        gstreamer1.0-pulseaudio \
        gstreamer1.0-plugins-ugly \
        gstreamer1.0-tools \
        libgstreamer1.0-dev \
        curl \
        python2.7 \
        # python-pip \
        python-yaml \
        # libcairo2-dev \
        libgirepository1.0-dev \
        # python-gi-cairo \
        libjansson4 \
        ffmpeg \
        sox \
        unzip \
        wget \
        gfortran \
        subversion \
        git \
        vim \
        psmisc \
        libsndfile-dev \
        supervisor \
        flac && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get install -y --no-install-recommends \
        python3.8 python3.8-dev python3.8-distutils python3.8-venv && \
    ln -fs /usr/bin/python3.8 /usr/bin/python3 && \
    ln -fs /usr/bin/python2.7 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/* && \
    curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py && \
    python3 /tmp/get-pip.py && \
    python3 -m pip install setuptools && \
    python3 -m pip install wheel && \
    # PYGOBJECT_WITHOUT_PYCAIRO=1 python3 -m pip install --no-build-isolation --no-use-pep517 PyGObject==3.36.0 && \
    python3 -m pip install -r requirements.txt && \
    python3 -m pip install speechbrain sklearn xgboost
#RUN cd /opt/spleeter && poetry update && poetry install 

RUN cd /opt && git clone https://github.com/ghuawhu/end-to-end-synthetic-speech-detection.git && \
    /bin/bash -c "virtualenv -p python3 inaSpeechSegEnv && \
    source inaSpeechSegEnv/bin/activate && \
    python3 -m pip install tensorflow-gpu && \
    python3 -m pip install tensorflow && \
    python3 -m pip install inaSpeechSegmenter && \
    deactivate" && \
    chmod -R 777 ./scripts
 
    #cd /opt && git clone https://github.com/google/uis-rnn && \

#RUN /bin/bash -c "virtualenv -p python3 inaSpeechSegEnv && \
#    source inaSpeechSegEnv/bin/activate && \
#    python3 -m pip install tensorflow-gpu && \
#    python3 -m pip install tensorflow && \
#    python3 -m pip install inaSpeechSegmenter && \
#    deactivate"
