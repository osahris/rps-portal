import logging
import os
import requests
import urllib
import json

try:
    from alerta.plugins import app  # alerta >= 5.0
except ImportError:
    from alerta.app import app  # alerta < 5.0
from alerta.plugins import PluginBase


LOG = logging.getLogger("alerta.plugins.matrix")

MATRIX_HOMESERVER_URL = [
    os.environ.get("MATRIX_HOMESERVER") or app.config["MATRIX_HOMESERVER"],
    "/_matrix/client/r0/rooms/",
    urllib.parse.quote(os.environ.get("MATRIX_ROOM") or app.config["MATRIX_ROOM"], ":"),
    "/send/m.room.message"
]
MATRIX_ACCESS_TOKEN = os.environ.get("MATRIX_ACCESS_TOKEN") or app.config["MATRIX_ACCESS_TOKEN"]
MATRIX_MESSAGE_TYPE = os.environ.get("MATRIX_MESSAGE_TYPE") or app.config.get("MATRIX_MESSAGE_TYPE", "notice")
MATRIX_MESSAGE_TYPES = {
    "notice": "m.notice",
    "text": "m.text"
}
DASHBOARD_URL = os.environ.get("DASHBOARD_URL") or app.config.get("DASHBOARD_URL", "")

# ---------- Custom block ---------- #
SEVERITY_ICON = {
    "critical": "🔴 ",
    "major": "🚨 ",
    "minor": "🟡 ",
    "warning": "⚠️ ",
    "ok": "✅ ",
    "normal": "✅ ",
    "debug": "🔧 ",
    "unknown": "❓ "
}
MATRIX_IGNORE_SEVERITY = os.environ.get("MATRIX_IGNORE_SEVERITY", "")
# ------ End of Custom Block ------ #


class SendMessage(PluginBase):
    def pre_receive(self, alert):
        return alert

    def post_receive(self, alert):

        if alert.repeat:
            return

        # ---------- Custom block ---------- #
        if alert.severity in MATRIX_IGNORE_SEVERITY:
            return # Alerts with such severity are not reported to Matrix 
        # ------ End of Custom Block ------ #

        severity_icon = SEVERITY_ICON.get(alert.severity, "")

        # ---------- Custom block ---------- #
        # body = "{}{}: {} alert for {} \n{} - {} - {} \n{} \nDate: {}".format(
        body = "{1}: {2}\n{0}{3}".format(
            severity_icon,
            alert.environment,
            # alert.severity.capitalize(),
            # ",".join(alert.service),
            alert.resource,
            # alert.event,
            # alert.value,
            alert.text,
            # alert.create_time,
        )
        # ------ End of Custom Block ------ #

        # ---------- Custom block ---------- #
        formatted_alert_text = alert.text.replace(alert.severity.upper(), '')
        formatted_alert_text = formatted_alert_text.replace('\n', '</br>')
        formatted_alert_text = formatted_alert_text.replace('"', '')
        formatted_alert_text = formatted_alert_text.replace('{', '')
        formatted_alert_text = formatted_alert_text.replace('}', '')
        # ------ End of Custom Block ------ #
        # ---------- Custom block ---------- #
        # formatted_body = "{}<strong>{}: {} alert for {} </br>{} - {} - {} </strong></br>{} </br><strong>Date: </strong> {} | <a rel='noopener' href='{}/#/alert/{}'>View alert</a>".format(
        formatted_body = "<strong>{1}: {0} {2}</strong>{3}<strong><a rel='noopener' href='{4}/#/alert/{5}'>View alert</a>".format(
            severity_icon,
            alert.environment,
            # alert.severity.capitalize(),
            # ",".join(alert.service),
            alert.resource,
            # alert.event,
            # alert.value,
            formatted_alert_text, #alert.text,
            # alert.create_time,
            DASHBOARD_URL,
            alert.id,
        )
        # ------ End of Custom Block ------ #

        payload = {
            "msgtype": MATRIX_MESSAGE_TYPES.get(MATRIX_MESSAGE_TYPE, "m.notice"),
            "format": "org.matrix.custom.html",
            "body": body,
            "formatted_body": formatted_body,
        }

        # LOG.debug("Matrix: %s", payload)

        try:
            r = requests.post(
                "".join(MATRIX_HOMESERVER_URL),
                headers={"Authorization": "Bearer " + MATRIX_ACCESS_TOKEN},
                data=json.dumps(payload).encode("utf-8"),
                timeout=2,
            )
        except Exception as e:
            raise RuntimeError("Matrix: ERROR - %s" % e)

        # LOG.debug("Matrix: %s - %s", r.status_code, r.text)

    def status_change(self, alert, status, text):
        return
