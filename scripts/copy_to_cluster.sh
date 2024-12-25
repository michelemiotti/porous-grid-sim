# Copy this repository to the cluster. 
# The first argument should be your username for the cluster.
# Ignore the warnings.
# You may be prompted for your cluster password twice.

cd simulation
echo "Cleaning local simulation results"
./Allclean > /dev/null 
if ! [ $? = 0 ];
    then
        echo "Allclean failed!"
        exit 1
    fi
cd ..

chmod +x scripts/password_wrapper
echo "Cleaning cluster simulation results"
./scripts/password_wrapper $2 ssh $1@calimero.energia.polimi.it > /dev/null "if [ -d /global-scratch/$1/porous-grid-sim ]; then rm -r /global-scratch/$1/porous-grid-sim; fi"
if ! [ $? = 0 ];
    then
        echo "Cluster repo cleanup failed!"
        exit 1
    fi

echo "Transferring to cluster"
./scripts/password_wrapper $2 scp -r . $1@calimero.energia.polimi.it:/global-scratch/$1/porous-grid-sim > /dev/null
if ! [ $? = 0 ];
    then
        echo "Transfer failed!"
        exit 1
    fi