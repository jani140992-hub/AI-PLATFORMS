class OmniFlowSDKError(Exception):
    def __init__(self, message: str, status_code: int = 500, response_body: str = ""):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_body = response_body

class AuthenticationError(OmniFlowSDKError):
    pass

class RateLimitError(OmniFlowSDKError):
    pass

class APIConnectionError(OmniFlowSDKError):
    pass
