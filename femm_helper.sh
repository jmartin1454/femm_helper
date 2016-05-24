#!/bin/sh

./femm_helper.py -s -f spherical.fem < femm_helper.in
./femm_helper.py -c -f cylindrical.fem < femm_helper_cyl.in
./femm_helper.py -c -r -f read.fem < femm_helper_read.in
