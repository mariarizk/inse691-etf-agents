from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import pandas as pd

from backend.etf_pipeline import ETFPipeline
from backend.system_health import SystemHealth
from agents.conversation_agent import ConversationAgent




app = FastAPI(
    title="QQQ Multi-Agent Decision Support System"
)

pipeline = ETFPipeline()

templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/data",
    StaticFiles(directory="data"),
    name="data"
)


@app.get("/")
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "result": None,
            "error": None
        }
    )

@app.post("/analyze")
async def analyze(
    request: Request,
    article: str = Form(...)
):

    try:

        price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date"
        )

        result = pipeline.run(
            price_df,
            article
        )

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "result": result
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "error": str(e)
            }
        )
    
@app.get("/agents")
async def agents(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="agents.html",
        context={
            "agents": pipeline.blackboard.all()
        }
    )




app = FastAPI(
    title="QQQ Multi-Agent Decision Support System"
)

pipeline = ETFPipeline()

conversation_agent = ConversationAgent()

templates = Jinja2Templates(
    directory="templates"
)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

app.mount(
    "/data",
    StaticFiles(directory="data"),
    name="data"
)


@app.get("/")
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "result": None,
            "error": None
        }
    )


@app.post("/analyze")
async def analyze(
    request: Request,
    article: str = Form(...)
):

    try:

        price_df = pd.read_csv(
            "data/QQQ.csv",
            parse_dates=["Date"],
            index_col="Date"
        )

        result = pipeline.run(
            price_df,
            article
        )

        # Save article and analysis
        conversation_agent.store_analysis(
            article_text=article,
            blackboard_data=result
        )

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "result": result,
                "article": article,
                "error": None
            }
        )

    except Exception as e:

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "result": None,
                "error": str(e)
            }
        )


@app.post("/chat")
async def chat(
    request: Request,
    message: str = Form(...)
):

    try:

        response = conversation_agent.chat(
            user_message=message
        )

        return {
            "response": response
        }

    except Exception as e:

        return {
            "error": str(e)
        }


@app.get("/agents")
async def agents(request: Request):

    print("BLACKBOARD CONTENTS:")
    print(pipeline.blackboard.all())

    return templates.TemplateResponse(
        request=request,
        name="agents.html",
        context={
            "agents": pipeline.blackboard.all()
        }
    )

@app.get("/logs")
async def logs(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="logs.html",
        context={
            "logs": pipeline.blackboard.get_log()
        }
    )


@app.get("/backtest")
async def backtest(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="backtest.html",
        context={}
    )


@app.get("/health")
async def health(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="health.html",
        context={
            "health": SystemHealth.get_status()
        }
    )

@app.get("/debug")
async def debug():

    return pipeline.blackboard.all()