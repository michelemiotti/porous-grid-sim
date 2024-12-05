# Copy this repository to the cluster. 
# The first argument should be your username for the cluster.
# Ignore the warnings.
# You may be prompted for your cluster password twice.

cd test
./Allclean
if ! [ $? = 0 ];
    then
        echo "Allclean failed!"
        exit 1
    fi
cd ..

ssh $1@calimero.energia.polimi.it "if [ -d /global-scratch/$1/porous-grid-sim ]; then rm -r /global-scratch/$1/porous-grid-sim; fi"
if ! [ $? = 0 ];
    then
        echo "Cluster repo cleanup failed!"
        exit 1
    fi

scp -r . $1@calimero.energia.polimi.it:/global-scratch/$1/porous-grid-sim
if ! [ $? = 0 ];
    then
        echo "Transfer failed!"
        exit 1
    fi