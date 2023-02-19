import csv
import json
import os
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .models import Candle, CandleData, CsvFile


async def process_csv(csv_file_path, timeframe):
        with open(csv_file_path) as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            candles = []
            for row in reader:
                id, date, time, _open, high, low, close, volume = row
                candle_date = datetime.strptime(date + time, "%Y%m%d%H:%M")
                candle = Candle(id, float(_open), float(high), float(low), float(close), candle_date)
                candles.append(candle)
               
                """
                It is required if the csv file data needed to store in database 
                candle = CandleData(id, float(_open), float(high), float(low), float(close), candle_date)
                """
                

        """
        If we want to store the data in our database and then create candles by fetching the data can be done through this
        CandleData.bulk_create(candles)
        """
        generated_candles = []
        start_date = candles[0].date.replace(second=0, microsecond=0)
        end_date = start_date + timedelta(minutes=timeframe)
        candle_group = [candles[0]]

        for candle in candles[1:]:
            if start_date <= candle.date < end_date:
                candle_group.append(candle)
            else:
                generated_candles.append({
                    "open": candle_group[0]._open,
                    "high": max(c.high for c in candle_group),
                    "low": min(c.low for c in candle_group),
                    "close": candle_group[-1].close,
                    "date": start_date.isoformat()
                })
                start_date = end_date
                end_date += timedelta(minutes=timeframe)
                candle_group = [candle]

        # convert last group of candles
        generated_candles.append({
            "open": candle_group[0]._open,
            "high": max(c.high for c in candle_group),
            "low": min(c.low for c in candle_group),
            "close": candle_group[-1].close,
            "date": start_date.isoformat()
        })
        return generated_candles

class UploadCsv(View):

    async def post(self, request):
        csv_file = request.FILES.get('csv_file')
        timeframe = int(request.POST.get('timeframe'))

        """
        Its optional if we want to store this csv file in our database
        CsvFile.objects.create(csv_file=csv_file)

        """

        # Save the CSV file on the Django server
        with open('media/data.txt', 'wb') as f:
            for data in csv_file.chunks():
                f.write(data)

        # Process the CSV file asynchronously
        converted_candles = await process_csv('media/data.txt', timeframe)

        # Store the converted data in a JSON file and store it in the file system
        output_file = 'media/output.json'
        with open(output_file, 'w') as f:
            json.dump(converted_candles, f)


        # Delete the CSV Its optional if we want to store it in our database 
        os.remove('media/data.txt')

        return render(request, 'base.html')    
    
    async def get(self, request):
       
        return render(request, 'index.html')
    

class DownloadJsonFile(View):
    def get(self, request, *args, **kwargs):
        with open('media/output.json', 'rb') as f:
            # Create response to download the file from a link 
            response = HttpResponse(f, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="output.json"'

        return response
    

