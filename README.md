# cmu_sphinx
Test out cmu sphinx on accent archive data set

To run sphinxtrain, first run:
` docker run -p 8888:8888 --mount type=bind,source="$(pwd)"/cmu_sphinx,target=/cmusphinx/ --rm -it  ch8:latest`
(from the same directory you cloned this repository into)

Then run each of the commands from build_model.sh