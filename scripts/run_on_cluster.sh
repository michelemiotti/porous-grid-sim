# Copy repo to cluster.
chmod +x scripts/copy_to_cluster.sh
./scripts/copy_to_cluster.sh $1 $2
if ! [ $? = 0 ];
then
    echo "Copying to cluster failed!"
    exit 1
fi

# Start the simulation.
echo "Running on cluster"
./scripts/password_wrapper $2 ssh $1@calimero.energia.polimi.it > /dev/null "cd /global-scratch/$1/porous-grid-sim/simulation && qsub Allrun_cluster"