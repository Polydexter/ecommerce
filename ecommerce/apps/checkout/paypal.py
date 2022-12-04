import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AQ84lkl9z-6GiVa9cMXD7zkDyCWyghoKWf2viMTZz4AGwz7951RHgtwz4nma08gRxFtDiBAbY-Au5O17"
        self.client_secret = "EODIPtz5CQ32hf6X6JcMj6ZRhaOkaZ2p419xOwW5QaxUT7XuxV6qKZ0dlaBg0goKGWP0psOT0aRkYeBR"
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.client = PayPalHttpClient(self.environment)
