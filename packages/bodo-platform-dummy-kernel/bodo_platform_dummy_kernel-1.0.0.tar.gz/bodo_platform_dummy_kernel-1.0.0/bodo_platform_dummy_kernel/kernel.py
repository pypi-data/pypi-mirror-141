from ipykernel.ipkernel import IPythonKernel


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


WARNING_MSG = f"{bcolors.WARNING}{bcolors.BOLD}{bcolors.UNDERLINE}WARNING: You have not attached this notebook to a cluster. Please attach to a cluster.\n{bcolors.ENDC}"


class DummyKernel(IPythonKernel):
    banner = "Dummy Kernel"

    def start(self):
        super().start()

    async def do_execute(
        self,
        code: str,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False,
    ):

        # Display the warning message before executing
        if not silent:
            stream_content = {"name": "stdout", "text": WARNING_MSG}
            self.send_response(self.iopub_socket, "stream", stream_content)

        # Then execute the command as usual
        return await super().do_execute(
            code=code,
            silent=silent,
            store_history=store_history,
            user_expressions=user_expressions,
            allow_stdin=allow_stdin,
        )
