## This portion is done in the phone_dic_accent_archive.py file
# Create vocab file
# text2wfreq < etc/accent_archive_train.transcription | wfreq2vocab > etc/accent_archive.vocab

# Create n-gram count from training transcript file
text2idngram -vocab etc/accent_archive.vocab -idngram etc/accent_archive.idngram < etc/accent_archive_train.transcription

# Create language model from n-grams
idngram2lm -vocab_type 0 -idngram etc/accent_archive.idngram -vocab etc/accent_archive.vocab -arpa etc/accent_archive.lm

# Convert language model to binary ( compression )
sphinx_lm_convert -i etc/accent_archive.lm -o etc/accent_archive.lm.DMP


# sphinxtrain -t accent_archive setup
# sphinxtrain run