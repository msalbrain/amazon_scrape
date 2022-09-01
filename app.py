from fastapi import FastAPI, HTTPException, status, BackgroundTasks

from scrape import entry
from db import *


app = FastAPI(title="Review scrapper",description="This api is used to automate the scraping of reviews on specific products fom amazon",
             version="0.1.0")


@app.get("/update", status_code=200)
async def update_route(background_tasks: BackgroundTasks):
    """
    route description :
        This endpoint is used to update the database of reviews. If an update is happening while the
        route is called nothing will happen. A message of:
        {"msg": "scrape in progress"}  will be returned
    """
    try:
        stat = status_col.find_one()
        if stat["active"] == 1:
            return {"msg": "scraping in progress"}
        elif stat["active"] == 0:
            background_tasks.add_task(entry)
            return {"msg": "scraping has been initiated"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"error": "sorry something went wrong on the back"})



@app.get("/stop", status_code=200)
async def stop_route():
    """
        route description :
            This endpoint is used to stop any scrapping process going on
            {"msg": "scraping successfully stopped"}  will be returned
        """
    try:
        stat = status_col.find_one({"_id": 1})
        stat.update({"active": 0})
        status_col.replace_one({"_id": 1}, stat)
        return {"msg": "scraping successfully stopped"}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail={"error": "sorry something went wrong on the back"})


@app.on_event("shutdown")
async def alter_status():
    reset_status()