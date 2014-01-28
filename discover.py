#!/usr/bin/env python
import select
import sys
import pybonjour

timeout  = 5
resolved = []

def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                     hosttarget, port, txtRecord):
    if errorCode == pybonjour.kDNSServiceErr_NoError:
        print 'Resolved service:'
        print '  fullname       =', fullname
        print '  flags          =', flags
        print '  hosttarget     =', hosttarget
        print '  interfaceIndex =', interfaceIndex
        print '  txtRecord      =', repr(txtRecord)
        print '  port           =', port
        resolved.append(True)


def browse_callback(sdRef, flags, interfaceIndex, errorCode, serviceName,
                    regtype, replyDomain):
    if errorCode != pybonjour.kDNSServiceErr_NoError:
        return

    if not (flags & pybonjour.kDNSServiceFlagsAdd):
        print 'Service removed'
        return

    print 'Service added; resolving'

    resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                interfaceIndex,
                                                serviceName,
                                                regtype,
                                                replyDomain,
                                                resolve_callback)

    try:
        while not resolved:
            ready = select.select([resolve_sdRef], [], [], timeout)
            if resolve_sdRef not in ready[0]:
                print 'Resolve timed out'
                break
            pybonjour.DNSServiceProcessResult(resolve_sdRef)
        else:
            resolved.pop()
    finally:
        resolve_sdRef.close()

def discoverLoop(regtype):
    browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                          callBack = browse_callback)
    try:
        try:
            while True:
                ready = select.select([browse_sdRef], [], [])
                if browse_sdRef in ready[0]:
                    pybonjour.DNSServiceProcessResult(browse_sdRef)
        except KeyboardInterrupt:
            pass
    finally:
        browse_sdRef.close()

if __name__ == "__main__":
    regtype = sys.argv[1] if len(sys.argv) > 1 else '_airdrop._tcp'
    discoverLoop(regtype)

