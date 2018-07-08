#! /bin/python

# Stress test for socrates-soil.net

import requests
import json
import urllib
import time
import sys


def run(is_stress):
    start_url = 'http://socrates-soil.net/input'
    start = requests.get(start_url)
    assert (start.status_code == 200)

    sample_url = 'http://socrates-soil.net/socrates/load/sample'
    sample = requests.post(sample_url)
    sample_json = json.loads(sample.text)
    assert (sample_json['simulation']['startYear'] == 1963)

    run_url = 'http://socrates-soil.net/socrates/run'
    socrates_model = {'socratesModel': sample_json}
    model = urllib.urlencode(socrates_model)
    run_model = requests.post(run_url, data=model)
    assert (run_model.status_code == 200)

    if not is_stress:
        print("All OK")


def stress(amount):
    print "Will test %d times" % amount
    for x in range(1, amount + 1):
        print "Test %d" % x
        run(is_stress=True)
        time.sleep(1)
    print("All OK")


def main():
    if not len(sys.argv) > 1:
        print "Running one test"
        run(is_stress=False)
    else:
        stress(int(sys.argv[1]))


if __name__ == '__main__':
    main()
