# No meaningful functions to test in this file.
# The run_chatbot function is a thin CLI wrapper that only orchestrates I/O (prompts, printing)
# and delegates to get_response. It contains no business logic, calculations, or transformations
# worth unit testing independently. The actual logic resides in portkey_client.get_response
# and models.ClientProfile which should be tested in their own test files.