# amazon_scrape

To use this scrapper first 
`pip install -r requirements.txt
`or 
`pip3 install -r requirements.txt
`
After installing needed packages enter database string and uncompressed dataset path in env.py file.

Then run 
`python script.py
`or 
`python3 script.py
`This will populate the database with the data from the dataset file and also flag incorrect asin product. 
 
To run the app locally using uvicorn as so:
`uvicorn app:app 
`
or for production you would have to set up gunicorn


This will activate the api with two endpoint
[/update]() - this initializes the scraping 
[/stop]() - this stops any scrapping process active 


The api was writter in fast api so enpoint [/docs]() and [/redoc]() contain documentation accurate documentation.
