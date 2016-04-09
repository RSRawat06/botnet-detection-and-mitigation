# TCP SYN-ACK Packet Flooding Detector
def detectTCPSynFlooding(pcapRecords, thresholdPercentage, windowSize):		
	for index, record in enumerate(pcapRecords):
			if isTCPSynPacket(record.protocol, record.info):		
				checkWindowFrame(index, pcapRecords, windowSize, thresholdPercentage)
				
				
# Check how many TCP SYN Packets are sent within the WindowSize.				
def checkWindowFrame(index, pcapRecords, windowSize, thresholdPercentage):
	windowStart = index + 1
	countInWindow = 0
	while windowStart < index + windowSize and windowStart < len(pcapRecords):
			if isTCPSynPacket(pcapRecords[windowStart].protocol, pcapRecords[windowStart].info):
					countInWindow = countInWindow + 1
			windowStart = windowStart + 1
	if (countInWindow*100/windowSize) >= thresholdPercentage and index + windowSize < len(pcapRecords):
			print 'Detected TCP SYN Flooding between ' + str(pcapRecords[index].timestamp) + ' and ' + str(pcapRecords[index + windowSize].timestamp) + ': ' + str(countInWindow*100/windowSize) + '%'


# Check if the current packet contributes to the TCP SYN Flooding
def isTCPSynPacket(protocol, info):
	return protocol=='TCP' and all( partialDetector in info for partialDetector in ['[SYN]','LEN=0','Seq=0'])