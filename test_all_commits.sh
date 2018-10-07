module load compilers/intel/2018_cluster_xe
module load apps/python/3.6.2
for commit in $(cat mpmc_commits.txt); do
  git clone git@github.com:mpmccode/mpmc.git ${commit}
  cd ${commit}
  git checkout -b ${commit} ${commit}
  if [ -f CMakeLists.txt ];then
    echo ${commit} >> ~/test_results.txt
    rm -rf mpmc_testing
    git clone    git@github.com:LucianoLaratelli/mpmc_testing.git
    bash compile.sh
    cd mpmc_testing
    ./run_tests.py >> ~/test_results.txt
  else
    continue
  fi
  cd ..
  rm -rf ${commit}
  exit
done

