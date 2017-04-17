#!/bin/bash

threshold=20
if [ ! -z $1 ]
then
    threshold=$1
fi

file='testing_phrases/phrases_shuffled.csv'

echo -n "bad phrases at $threshold: "
for i in {0..4}
do
    range_start=$((i*100+1))
    range_end=$(((i+1)*100))
    COUNT=`sed -n -e "${range_start},${range_end}p" $file | cut -d$'\t' -f1 | python tf_rnnlm/word_lm.py --action loglikes --threshold $threshold --compare gt --model_dir ../real_since_jan_shuffled_small_15000 | wc -l` ###  5 extra from warnings
    COUNT=`expr $COUNT - 5`
    echo $COUNT
done | awk '{ sum += $1; n++; print $1 } END { if (n > 0) print "AVG:", sum / n; }'

echo -n "good phrases at $threshold: "
for i in {0..4}
do
    range_start=$((i*100+1))
    range_end=$(((i+1)*100))
    COUNT=`sed -n -e "${range_start},${range_end}p" $file | cut -d$'\t' -f2 | python tf_rnnlm/word_lm.py --action loglikes --threshold $threshold --compare lt --model_dir ../real_since_jan_shuffled_small_15000 | wc -l` ###  5 extra from warnings
    COUNT=`expr $COUNT - 5`
    echo $COUNT
done | awk '{ sum += $1; n++; print $1 } END { if (n > 0) print "AVG:", sum / n; }'
