#!/bin/bash
start_time=`date +%s`
python textual_feat.py
python visual_feat.py
python compoundClassification.py
echo run time is$(expr `date +%s` - $start_time) s