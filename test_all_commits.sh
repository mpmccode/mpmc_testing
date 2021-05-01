#!/bin/bash
rm test_results.txt
for commit in $(cat mpmc_commits.txt); do
  git clone git@github.com:mpmccode/mpmc.git ${commit}
  cd ${commit}
  git checkout -b ${commit} ${commit}
  if [ -f CMakeLists.txt ];then
    rm -rf mpmc_testing
    git clone    git@github.com:mpmccode/mpmc_testing.git
    mkdir build
    cd build
    cmake -DQM_ROTATION=OFF -DVDW=OFF -DMPI=OFF -DOPENCL=OFF -DCUDA=OFF -DCMAKE_BUILD_TYPE=Release -Wno-dev ../
    make
    cd ..
    cd mpmc_testing
    echo ${commit} >> ../../test_results.txt
    ./run_tests.py >> ../../test_results.txt
  else
    continue
  fi
  cd ../..
  #rm -rf ${commit}
done

