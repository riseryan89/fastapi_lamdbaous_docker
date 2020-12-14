from fastapi import FastAPI
from models import GetCode, CodeRunResult
import json
import io
import sys
import logging


app = FastAPI()


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = io.StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio  # 메모리 관리
        sys.stdout = self._stdout


@app.post("/run/python", response_model=CodeRunResult)
async def run_python(code: GetCode):
    logger = logging.getLogger("basic_logger")
    logger.setLevel(logging.DEBUG)
    code = code.code
    # 아웃풋 에러 캡쳐
    log_capture_string = io.StringIO()
    ch = logging.StreamHandler(log_capture_string)

    logger.addHandler(ch)
    a = ""
    try:
        with Capturing() as output:
            try:
                exec(code, globals(), globals())
                function_handler()  # 메인함수 실행
            except Exception as e:
                a = output
                raise e
        # restore stdout and stderr
    except:
        logger.error("error", exc_info=True)
        log_contents = log_capture_string.getvalue()
        log_capture_string.close()
        body = dict(printed=a, error=log_contents)
        return {"statusCode": 400, "body": json.dumps(body, ensure_ascii=False)}
    else:
        log_capture_string.close()
        body = dict(printed=output, error="Process finished with exit code 0")
        return {"statusCode": 200, "body": json.dumps(body, ensure_ascii=False)}
