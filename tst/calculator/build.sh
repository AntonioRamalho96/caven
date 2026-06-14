set -e
rm -rf libcalculator.so
INCLUDE_FLAGS_DEPS=$( caven use -if -s . )
LINK_FLAGS_DEPS=$( caven use -lf -s .)
g++ -v -shared -fPIC -I inc  $INCLUDE_FLAGS_DEPS src/calculator.cpp -o libcalculator.so  $LINK_FLAGS_DEPS -Wl,--no-undefined