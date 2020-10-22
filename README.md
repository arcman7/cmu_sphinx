# cmu_sphinx
Test out cmu sphinx on accent archive data set

To run sphinxtrain, first run:
` docker run -p 8888:8888 --mount type=bind,source="$(pwd)"/cmu_sphinx,target=/cmusphinx/ --rm -it  ch8:latest`
(from the same directory you cloned this repository into)

Then run the folowoing commands from the `/cmusphinx/accent_archive` directory in the docker container:

* Create n-gram count from training transcript file

`text2idngram -vocab etc/accent_archive.vocab -idngram etc/accent_archive.idngram < etc/accent_archive_train.transcription`

* Create language model from n-grams

`idngram2lm -vocab_type 0 -idngram etc/accent_archive.idngram -vocab etc/accent_archive.vocab -arpa etc/accent_archive.lm`

* Convert language model to binary ( compression )

`sphinx_lm_convert -i etc/accent_archive.lm -o etc/accent_archive.lm.DMP`

`sphinxtrain -t accent_archive setup`

`sphinxtrain run`
