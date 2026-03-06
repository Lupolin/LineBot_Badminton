from logging import Logger

from domain.routine.repository import GetMemberInfoRepository
from infrastructure.opentelemetry import trace_method


class ResetAttendanceUseCase:
    def __init__(
        self,
        repo: GetMemberInfoRepository,
        logger: Logger,
    ):
        self.repo = repo
        self.logger = logger

    @trace_method("UseCase: ResetAttendanceUseCase")
    def execute(self):
        self.logger.info("Starting attendance reset process for all members.")
        try:
            self.repo.reset_all_attendance()
        except Exception as e:
            raise RuntimeError("Failed to reset attendance") from e
