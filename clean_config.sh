#!/bin/sh

awk '{if (/GRAPHDB_URL/) print "GRAPHDB_URL=<ADD NEO4J URL HERE>"; else print $0;}' |  \
	awk '{if (/GRAPHDB_USER/) print "GRAPHDB_USER=<ADD NEO4J USER HERE>"; else print $0;}'  | \
	awk '{if (/GRAPHDB_PASSWD/) print "GRAPHDB_PASSWD=<ADD NEO4J PASSWORD HERE>"; else print $0;}' 

exit 0