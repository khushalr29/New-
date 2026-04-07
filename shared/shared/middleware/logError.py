import re
import os
import json
import logging
import socket
from pathlib import Path
from logging.handlers import RotatingFileHandler
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


LOG_MAX_BYTES = getattr(settings, "API_LOG_MAX_BYTES", 10 * 1024 * 1024)
LOG_BACKUP_COUNT = getattr(settings, "API_LOG_BACKUP_COUNT", 5)
REQUEST_BODY_MAX = getattr(settings, "API_LOG_REQUEST_BODY_MAX", 2000)


class APILoggerMiddleware(MiddlewareMixin):
    def _sanitize_filename(self, path: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9]+", "_", path.strip("/"))
        return clean or "root"

    def _log_dir(self) -> Path:
        log_dir = Path(settings.BASE_DIR) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir

    def _get_logger(self, request):
        log_dir = self._log_dir()
        filename = f"{self._sanitize_filename(request.path)}.log"
        log_file = log_dir / filename

        logger_name = str(log_file)
        logger = logging.getLogger(logger_name)

        if not logger.handlers:
            handler = RotatingFileHandler(
                log_file,
                maxBytes=LOG_MAX_BYTES,
                backupCount=LOG_BACKUP_COUNT,
                encoding="utf-8",
            )
            formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False

        return logger

    def _get_client_ip(self, request):
        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        if xff:
            ip = xff.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def _get_server_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        except Exception:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip

    def _safe_body(self, raw_body: bytes):
        if not raw_body:
            return ""
        try:
            text = raw_body.decode("utf-8")
        except Exception:
            return "[binary or undecodable body]"
        try:
            parsed = json.loads(text)
            pretty = json.dumps(parsed, ensure_ascii=False, indent=2)
            if len(pretty) > REQUEST_BODY_MAX:
                return pretty[:REQUEST_BODY_MAX] + "\n...[truncated]"
            return pretty
        except Exception:
            text = text.strip()
            if len(text) > REQUEST_BODY_MAX:
                return text[:REQUEST_BODY_MAX] + "\n...[truncated]"
            return text


    def process_response(self, request, response):
        logger = self._get_logger(request)
        client_ip = self._get_client_ip(request)
        server_ip = self._get_server_ip()

        try:
            resp_body = self._safe_body(response.content) if hasattr(response, "content") else ""
        except Exception:
            resp_body = "[unreadable response body]"

        log_entry = {
            "client_ip": client_ip,
            "server_ip": server_ip,
            "method": request.method,
            "path": request.get_full_path(),
            "status": getattr(response, "status_code", "unknown"),
            "response_body": resp_body,
        }
        logger.info("RESPONSE:\n" + json.dumps(log_entry, indent=2, ensure_ascii=False))
        return response

    def process_exception(self, request, exception):
        logger = self._get_logger(request)
        client_ip = self._get_client_ip(request)
        server_ip = self._get_server_ip()

        error_entry = {
            "client_ip": client_ip,
            "server_ip": server_ip,
            "method": request.method,
            "path": request.get_full_path(),
            "exception": str(exception),
        }
        logger.error("EXCEPTION:\n" + json.dumps(error_entry, indent=2, ensure_ascii=False), exc_info=True)
        return None
