"""Task(s) for the transfer out of data from a processing pipeline."""
import logging
from abc import ABC
from functools import cached_property
from pathlib import Path
from typing import Iterable
from typing import List

from dkist_processing_common.models.message import CatalogFrameMessage
from dkist_processing_common.models.message import CatalogObjectMessage
from dkist_processing_common.models.message import CreateQualityReportMessage
from dkist_processing_common.models.tags import Tag
from dkist_processing_common.tasks import WorkflowTaskBase
from dkist_processing_common.tasks.mixin.globus import GlobusMixin
from dkist_processing_common.tasks.mixin.globus import GlobusTransferItem
from dkist_processing_common.tasks.mixin.interservice_bus import InterserviceBusMixin
from dkist_processing_common.tasks.mixin.object_store import ObjectStoreMixin


__all__ = [
    "AddDatasetReceiptAccount",
    "PublishCatalogAndQualityMessages",
    "TransferL1Data",
    "L1OutputDataBase",
]


logger = logging.getLogger(__name__)


class L1OutputDataBase(WorkflowTaskBase, ABC):
    """
    Subclass of WorkflowTaskBase used by TransferL1Data (defined below).

    Extends WorkflowTaskBase to provide the destination_bucket property and format_object_key method.
    """

    @cached_property
    def destination_bucket(self) -> str:
        """Get the destination bucket."""
        return self.metadata_store_recipe_run_configuration().get("destination_bucket", "data")

    def format_object_key(self, path: Path) -> str:
        """
        Convert output paths into object store keys.

        Parameters
        ----------
        path: the Path to convert

        Returns
        -------
        formatted path in the object store
        """
        return str(Path(self.constants.proposal_id, self.constants.dataset_id, path.name))


class TransferL1Data(L1OutputDataBase, GlobusMixin, ObjectStoreMixin):
    """Task class for transferring Level 1 processed data to the object store."""

    def transfer_science_frames(self):
        """Transfer the science frames to the object store."""
        transfer_items = []
        for file_path in self.read(tags=[Tag.output(), Tag.frame()]):
            object_key = self.format_object_key(file_path)
            destination_path = Path(self.destination_bucket, object_key)
            item = GlobusTransferItem(
                source_path=file_path,
                destination_path=destination_path,
            )
            transfer_items.append(item)
        logger.info(
            f"Preparing globus transfer {len(transfer_items)} items: recipe_run_id={self.recipe_run_id}. transfer_items={transfer_items[:3]}..."
        )
        self.globus_transfer_scratch_to_object_store(
            transfer_items=transfer_items,
            label=f"Transfer Output Data for recipe_run_id {self.recipe_run_id}",
        )

    def transfer_movie(self):
        """Transfer the movie to the object store."""
        paths = list(self.read(tags=[Tag.output(), Tag.movie()]))
        if len(paths) == 0:
            logger.warning(
                f"No movies found to upload for dataset. recipe_run_id={self.recipe_run_id}"
            )
            return
        movie = paths[0]
        if count := len(paths) > 1:
            # note: this needs to be an error or the dataset receipt accounting will have an
            # expected count > the eventual actual
            raise RuntimeError(
                f"Multiple movies found to upload.  Uploading the first one. "
                f"{count=}, {movie=}, recipe_run_id={self.recipe_run_id}"
            )
        logger.info(f"Uploading Movie: recipe_run_id={self.recipe_run_id}, {movie=}")
        movie_object_key = self.format_object_key(movie)
        self.object_store_upload_movie(
            movie=movie,
            bucket=self.destination_bucket,
            object_key=movie_object_key,
            content_type="video/mp4",
        )

    def run(self) -> None:
        """Transfer the data."""
        with self.apm_step("Upload Science Frames"):
            self.transfer_science_frames()
        with self.apm_step("Upload Movie"):
            self.transfer_movie()


class PublishCatalogAndQualityMessages(L1OutputDataBase, InterserviceBusMixin):
    """Task class for publishing Catalog and Quality Messages."""

    def frame_messages(self, paths: Iterable[Path]) -> List[CatalogFrameMessage]:
        """
        Create the frame messages.

        Parameters
        ----------
        paths
            The input paths for which to publish frame messages

        Returns
        -------
        A list of frame messages
        """
        messages = [
            CatalogFrameMessage(
                objectName=self.format_object_key(path=p),
                conversationId=str(self.recipe_run_id),
                bucket=self.destination_bucket,
            )
            for p in paths
        ]
        return messages

    def object_messages(
        self, paths: Iterable[Path], object_type: str
    ) -> List[CatalogObjectMessage]:
        """
        Create the object messages.

        Parameters
        ----------
        paths
            The input paths for which to publish object messages
        object_type
            The object type

        Returns
        -------
        A list of object messages
        """
        messages = [
            CatalogObjectMessage(
                objectType=object_type,
                objectName=self.format_object_key(p),
                bucket=self.destination_bucket,
                conversationId=str(self.recipe_run_id),
                groupId=self.constants.dataset_id,
            )
            for p in paths
        ]
        return messages

    @property
    def quality_report_message(self) -> CreateQualityReportMessage:
        """Create the Quality Report Message."""
        file_name = Path(f"{self.constants.dataset_id}.pdf")
        return CreateQualityReportMessage(
            bucket=self.destination_bucket,
            objectName=self.format_object_key(file_name),
            conversationId=str(self.recipe_run_id),
            datasetId=self.constants.dataset_id,
        )

    def run(self) -> None:
        """Run method for this trask."""
        with self.apm_step("Gather output data"):
            frames = self.read(tags=[Tag.output(), Tag.frame()])
            movies = self.read(tags=[Tag.output(), Tag.movie()])
        with self.apm_step("Create message objects"):
            messages = []
            messages += self.frame_messages(paths=frames)
            messages += self.object_messages(paths=movies, object_type="MOVIE")
            messages.append(self.quality_report_message)
        with self.apm_step("Publish messages"):
            self.interservice_bus_publish(messages=messages)


class AddDatasetReceiptAccount(WorkflowTaskBase):
    """
    Add a Dataset Receipt Account record to Processing Support for use by the Dataset Catalog Locker.

    Adds the number of files created during the calibration processing to the Processing Support table
    for use by the Dataset Catalog Locker.
    """

    def run(self) -> None:
        """Run method for this task."""
        with self.apm_step("Count Expected Outputs"):
            dataset_id = self.constants.dataset_id
            expected_object_count = self.count(tags=Tag.output())
        logger.info(
            f"Adding Dataset Receipt Account: "
            f"{dataset_id=}, {expected_object_count=}, recipe_run_id={self.recipe_run_id}"
        )
        with self.apm_step("Add Dataset Receipt Account"):
            self.metadata_store_add_dataset_receipt_account(
                dataset_id=dataset_id, expected_object_count=expected_object_count
            )
