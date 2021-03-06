#!/usr/bin/env python
import select
import sys
import pybonjour

def register_callback(sdRef, flags, errorCode, name, regtype, domain):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        sys.stderr.write('Registered service')

def buildTxtRecord(dic):
   return "".join([chr(len(s)) + s for s in ("%s=%s" % e for e in dic.iteritems())])
    
def registerAirDrop(cname, targetPort=65518, serviceName='d5924ed3d9b2'):
    airDropParams = {
        "flags": "1",
        "phash": "fPy/DAcMib0CKkACSGUAANbNaa8=",
        "ehash": "VfX1TwkwyzXneCgybPQGtm73IQd=",
        "cname": cname,
    }
    sdRef = pybonjour.DNSServiceRegister(name = serviceName,
                                         regtype = '_airdrop._tcp',
                                         port = targetPort,
                                         txtRecord = buildTxtRecord(airDropParams),
                                         callBack = register_callback)
    try:
        try:
            while True:
                ready = select.select([sdRef], [], [])
                if sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(sdRef)
        except KeyboardInterrupt:
            pass
    finally:
        sdRef.close()

if __name__ == "__main__":
    displayName = sys.argv[1] if len(sys.argv) > 1 else 'bera'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 65518
    registerAirDrop(displayName, port)
