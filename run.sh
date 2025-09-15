

































#!/bin/bash

# Function to stop processes on exit
function cleanup {
  echo "Stopping servers..."
  kill $(jobs -p) 2>/dev/null
}

# Register the cleanup function to be called on exit
trap cleanup EXIT

# Start backend server
echo "Starting backend server..."
cd backend
python run.py &

# Wait a bit for backend to start
sleep 2

# Start frontend server
echo "Starting frontend server..."
cd ../frontend
./run.sh &

# Wait for both processes
wait

































