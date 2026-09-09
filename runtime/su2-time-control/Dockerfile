FROM concentration-aware-ns:su2
COPY helper.cpp replace.py /tmp/
RUN python3 /tmp/replace.py && ninja -C /opt/SU2/build -j2 install
WORKDIR /case
