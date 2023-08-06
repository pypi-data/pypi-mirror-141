"""Task class for submitting the quality report to the metadata store."""
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.quality import QualityMixin


__all__ = ["SubmitQuality"]


class SubmitQuality(WorkflowTaskBase, QualityMixin):
    """Task class for submitting the quality report to the metadata store."""

    def run(self):
        """Run method for the task."""
        with self.apm_step("Building quality report"):
            report = self.quality_build_report()
        with self.apm_step("Submitting quality report"):
            self.metadata_store_add_quality_report(
                dataset_id=self.constants.dataset_id, quality_report=report
            )
