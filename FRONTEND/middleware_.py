import time

from fastapi import Request
from fastapi.responses import RedirectResponse

SESSION_TIMEOUT = 30 * 60


async def check_session(request: Request):

    user = request.session.get("user")

    if not user:
        return False

    last_activity = request.session.get("last_activity")

    if last_activity:
        inactive_time = time.time() - last_activity

        if inactive_time >= SESSION_TIMEOUT:
            request.session.clear()
            return False

    request.session["last_activity"] = time.time()

    return True


"""












"""