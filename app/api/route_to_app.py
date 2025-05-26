from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi import HTTPException

app = FastAPI()

PACKAGE_NAME = " " # 내 애플리케이션 패키지 이름름
FALLBACK_URL = f"https://play.google.com/store/apps/details?id={PACKAGE_NAME}"

@app.get("/route-to-app")
def route_to_app(type: str, id: int, request: Request):
    user_agent = request.headers.get("user-agent", "").lower()

    if type not in ("product", "bundle", "supplier"):
        raise HTTPException(status_code=400, detail="유효하지 않은 type")

    scheme_path = f"{type}/{id}"  # 예: product/42

    if "android" in user_agent:
        intent_url = (
            f"intent://{scheme_path}#Intent;"
            f"scheme=myapp;"
            f"package={PACKAGE_NAME};"
            f"S.browser_fallback_url={FALLBACK_URL};"
            f"end"
        )
        return RedirectResponse(url=intent_url)

    elif "iphone" in user_agent or "ipad" in user_agent:
        ios_scheme = f"myapp://{scheme_path}"
        return RedirectResponse(url=ios_scheme)

    return RedirectResponse(url=FALLBACK_URL)
