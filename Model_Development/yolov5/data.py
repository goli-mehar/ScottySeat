import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset( "open-images-v6", split='train', label_types=["detections"], classes=["Person", "Chair", "Table", "Backpack"], max_samples=200,)
dataset.export(
    export_dir="data/OpenImages/group2",
    dataset_type=fo.types.YOLOv5Dataset
)

#print(fiftyone.utils.openimages.get_classes(version='v6', dataset_dir=None)
