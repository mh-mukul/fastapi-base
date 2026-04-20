class ResponseHelper:
    def response(self, status_code, message, data=None):
        return ({
            "status": status_code,
            "message": message,
            "data": data
        })
