FROM concentration-aware-ns:su2-time-control
COPY replace.py /tmp/output-clock-replace.py
RUN python3 /tmp/output-clock-replace.py && ninja -C /opt/SU2/build -j2 install
WORKDIR /case
