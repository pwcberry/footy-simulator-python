class MockBuffer:
    content = ""

    def write(self, input):
        self.content = input
