FROM concentration-aware-ns:su2-time-control
RUN python3 -c 'from pathlib import Path; p=Path("/opt/SU2/SU2_CFD/src/drivers/CSinglezoneDriver.cpp"); s=p.read_text(); old="SetPhysicalTime(static_cast<su2double>(TimeIter)*"; assert s.count(old)==1; p.write_text(s.replace(old,"SetPhysicalTime(static_cast<su2double>(TimeIter+1)*"))' \
 && ninja -C /opt/SU2/build -j2 install
WORKDIR /case
