from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


# Templates are stored in the project's root templates folder
templates = Jinja2Templates(
    directory="templates"
)

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@router.get(
    "/login",
    response_class=HTMLResponse,
)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={},
    )


@router.get(
    "/register",
    response_class=HTMLResponse,
)
def register_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={},
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={},
    )


@router.get(
    "/history",
    response_class=HTMLResponse,
)
def history_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={},
    )


@router.get(
    "/home-planner",
    response_class=HTMLResponse,
)
def home_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planners/home.html",
        context={},
    )


@router.get(
    "/party-planner",
    response_class=HTMLResponse,
)
def party_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planners/party.html",
        context={},
    )


@router.get(
    "/jewelry-planner",
    response_class=HTMLResponse,
)
def jewelry_planner(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="planners/jewelry.html",
        context={},
    )