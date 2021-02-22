#!/usr/bash

echo "enter TODAY's date in YYYYMMDD format"
read today_date
yesterday_date=$((today_date - 1))
echo "date is set to $yesterday_date"
python3 update.py 20-21 $yesterday_date
cd data
python3 appender.py
echo "check if schedule.csv is updated with todays games enter 1 when is"
#read schedule_check
#if $schedule_check == "1"; then
cd ../modelling
python3 predictor.py $today_date
python3 predictor40wr.py $today_date
cd ..
python3 plac_preds.py
cd logs
python3 value.py -d today_date
#[else return 0;]
#fi
