class ProviderBase:
    def send(self, messages):
        raise NotImplementedError("send() must be implemented by subclasses")