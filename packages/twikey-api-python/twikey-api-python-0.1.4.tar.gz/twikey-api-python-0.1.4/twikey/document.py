import requests
import logging


class Document(object):
    def __init__(self, client) -> None:
        super().__init__()
        self.client = client
        self.logger = logging.getLogger(__name__)

    def create(self, data):
        url = self.client.instance_url("/invite")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(url=url, data=data, headers=self.client.headers())
        jsonResponse = response.json()
        if "ApiErrorCode" in response.headers:
            error = jsonResponse
            raise Exception("Error invite : %s" % error)
        self.logger.debug("Added new mandate : %s" % jsonResponse["mndtId"])
        return jsonResponse

    def update(self, data):
        url = self.client.instance_url("/mandate/update")
        data = data or {}
        self.client.refreshTokenIfRequired()
        response = requests.post(url=url, data=data, headers=self.client.headers())
        self.logger.debug(
            "Updated mandate : %s status=%d" % (data.mndtId, response.status_code)
        )
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error invite : %s" % error)

    def cancel(self, mandate_number, reason):
        url = self.client.instance_url(
            "/mandate?mndtId=" + mandate_number + "&rsn=" + reason
        )
        self.client.refreshTokenIfRequired()
        response = requests.delete(url=url, headers=self.client.headers())
        self.logger.debug(
            "Updated mandate : %s status=%d" % (mandate_number, response.status_code)
        )
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error invite : %s" % error)

    def feed(self, documentFeed):
        url = self.client.instance_url("/mandate")

        self.client.refreshTokenIfRequired()
        response = requests.get(url=url, headers=self.client.headers())
        response.raise_for_status()
        if "ApiErrorCode" in response.headers:
            error = response.json()
            raise Exception("Error feed : %s" % error)
        feedResponse = response.json()
        while len(feedResponse["Messages"]) > 0:
            self.logger.debug("Feed handling : %d" % (len(feedResponse["Messages"])))
            for msg in feedResponse["Messages"]:
                if "AmdmntRsn" in msg:
                    mndt_id_ = msg["OrgnlMndtId"]
                    self.logger.debug("Feed update : %s" % (mndt_id_))
                    mndt_ = msg["Mndt"]
                    rsn_ = msg["AmdmntRsn"]
                    documentFeed.updatedDocument(mndt_id_, mndt_, rsn_, msg["EvtTime"])
                elif "CxlRsn" in msg:
                    self.logger.debug("Feed cancel : %s" % (msg["OrgnlMndtId"]))
                    documentFeed.cancelDocument(
                        msg["OrgnlMndtId"], msg["CxlRsn"], msg["EvtTime"]
                    )
                else:
                    self.logger.debug("Feed create : %s" % (msg["Mndt"]))
                    documentFeed.newDocument(msg["Mndt"], msg["EvtTime"])
            response = requests.get(url=url, headers=self.client.headers())
            if "ApiErrorCode" in response.headers:
                error = response.json()
                raise Exception(
                    "Error invite : %s - %s" % (error["code"], error["message"])
                )
            feedResponse = response.json()


class DocumentFeed:
    def newDocument(self, doc, evtTime):
        pass

    def updatedDocument(self, original_mandate_number, doc, reason, evtTime):
        pass

    def cancelDocument(self, docNumber, reason, evtTime):
        pass
