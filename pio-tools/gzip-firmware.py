Import('env')
import os
import shutil
import gzip

OUTPUT_DIR = "build_output{}".format(os.path.sep)

def bin_gzip(source, target, env):
    variant = str(target[0]).split(os.path.sep)[2]
    
    # create string with location and file names based on variant
    bin_file = "{}firmware{}{}.bin".format(OUTPUT_DIR, os.path.sep, variant)
    gzip_file = "{}firmware{}{}.bin.gz".format(OUTPUT_DIR, os.path.sep, variant)

    # check if new target files exist and remove if necessary
    if os.path.isfile(gzip_file): os.remove(gzip_file)

    # write gzip firmware file
    with open(bin_file,"rb") as fp:
        with gzip.open(gzip_file, "wb", compresslevel = 9) as f:
            shutil.copyfileobj(fp, f)
    
    ORG_FIRMWARE_SIZE = os.stat(bin_file).st_size
    GZ_FIRMWARE_SIZE = os.stat(gzip_file).st_size

    print("Compression reduced firmware size by {:.0f}% (was {} bytes, now {} bytes)".format((GZ_FIRMWARE_SIZE / ORG_FIRMWARE_SIZE) * 100, ORG_FIRMWARE_SIZE, GZ_FIRMWARE_SIZE))

env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", [bin_gzip])
