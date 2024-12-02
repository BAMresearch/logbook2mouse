# in this script, put things that are to be run at the very end, 
# such as disabling temperature controllers, closing shutters, moving detector to detx=400, etc.

from epics import caput, caget
import logging

logging.info('Measurement entry complete for sample {entry.sampleid}.')
