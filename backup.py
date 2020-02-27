import os
import time

source = ['C:\\workspace\\hello', 'C:\\workspace\\hello']
target_dir = 'C:\\workspace'

target = target_dir + os.sep + time.strftime('%Y%m%d%H%M%S') + '.zip'

zip_command = "zip -r {0} {1}".format(target, ' '.join(source))

if os.system(zip_command) == 0 :
    print("Success")
else :
    print("Fail")