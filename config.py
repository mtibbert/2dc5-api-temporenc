
#
# This file contains high-level configuration variables for CultureMeshFFB.
#
#     DO NOT INCLUDE SENSITIVE CONFIGURATION HERE.  THIS WILL BE
#     IN VERSION CONTROL.
#

import datetime

PORT=5000
ADDR='127.0.0.1'
DEBUG_PORT=8080
DEBUG_ADDR=ADDR
DATETIME_FMT_STR = "%Y-%m-%d %H:%M:%S"
PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
