# Reality-scraper
Scraping fisrt 500 offers (title and first image) from sreality.cz (flats, sell) using Selenium. After succesfull scraping data are saved in the Postgresql database. All results are then available via running Flask web. Setup is dockerized, for running use:

```
docker-compose up
```

During running of commands firstly Postgresql image is created.  After database is succesfully running second image with Python and Selenium starts. When flask server is running just use browser and type:
```
http://127.0.0.1:8080/
```
# Page sample:
![Page with loaded data](https://github.com/JiriSvacek/Reality-scraper/blob/master/pic/page.PNG)
