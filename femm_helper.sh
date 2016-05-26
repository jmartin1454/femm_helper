#!/bin/sh

./femm_helper.py -s -f spherical.fem < femm_helper.in
./femm_helper.py -c -f cylindrical.fem < femm_helper_cyl.in
./femm_helper.py -c -r -f read.fem < femm_helper_read.in
# ./femm_helper.py -c -r -f read-100.fem -i Cylinder-100-turns-inner.txt -o Cylinder-100-turns-outer.txt < femm_helper_read.in
# ./femm_helper.py -c -r -f read-100mA.fem -i Cylinder-Inner-100mA.txt -o Cylinder-outer-100mA.txt < femm_helper_read.in
