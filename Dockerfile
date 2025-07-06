FROM python:3.11-slim

ENV ANDROID_HOME=/opt/android-sdk
ENV PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools"

RUN apt-get update && apt-get install -y \
    unzip zip git curl openjdk-17-jdk \
    build-essential libncurses5 libncurses5-dev \
    libstdc++6 zlib1g zlib1g-dev libncurses6 \
    python3-pip python3-setuptools python3-wheel \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Install Buildozer and dependencies
RUN pip install --upgrade pip setuptools Cython buildozer

# Download Android command-line tools
RUN mkdir -p $ANDROID_HOME/cmdline-tools && \
    curl -sSL https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -o cmdline.zip && \
    unzip -q cmdline.zip -d $ANDROID_HOME/cmdline-tools && \
    mv $ANDROID_HOME/cmdline-tools/cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm cmdline.zip

# Install Android SDK components
RUN yes | sdkmanager --sdk_root=$ANDROID_HOME --licenses && \
    sdkmanager --sdk_root=$ANDROID_HOME "platform-tools" "platforms;android-30" "build-tools;30.0.3"

# Compatibility: create legacy tools path so Buildozer can find sdkmanager
RUN ln -s $ANDROID_HOME/cmdline-tools/latest $ANDROID_HOME/tools

