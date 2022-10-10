import urllib.request
import sys
import time


# returns the string contents of the page at url, or "" if there is an error


def read_url(url):
    fail_count = 0

    while fail_count < 10:
        # time.sleep(1)
        try:
            fp = urllib.request.urlopen(url)
            mybytes = fp.read()

            mystr = mybytes.decode(sys.stdout.encoding)
            fp.close()
            #mystr = mystr.split("\n")
            return mystr
        except:
            fail_count += 1
            print("Failed to read " + url + "(" + str(fail_count) + ")")
    return ""
