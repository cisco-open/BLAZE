FROM ubuntu:latest
WORKDIR /blaze
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
ENV PATH /opt/conda/envs/aski/bin:$PATH
RUN apt-get update && apt-get -y upgrade 
RUN apt-get install -y python3-pip 
RUN apt-get install -y python3-dev build-essential
RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-x86_64.sh
RUN bash Miniconda3-py39_4.12.0-Linux-x86_64.sh -b
RUN rm -f Miniconda3-py39_4.12.0-Linux-x86_64.sh
COPY . .
RUN conda install -y -c pytorch python=3.7 faiss-gpu 
RUN conda env create -f aski_env.yml
SHELL ["conda", "run", "-n", "aski", "/bin/bash", "-c"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "aski", "python", "build.py"]



