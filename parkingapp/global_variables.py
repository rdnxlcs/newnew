class Global:
    def __init__(self, default_start_time, default_end_time) -> None:
        self.default_start_time = default_start_time
        self.default_end_time = default_end_time

global_variables = Global(default_start_time='2024-02-05', default_end_time='2024-02-25')