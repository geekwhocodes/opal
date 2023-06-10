from fastapi import FastAPI


def create_app() -> FastAPI:

    return FastAPI(title="opal")


app = create_app()


@app.get("/ping")
def get_ping() -> int:
    return 1

