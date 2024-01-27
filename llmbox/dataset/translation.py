from langcodes import Language

from ..metric import Bleu
from .generation_dataset import GenerationDataset


class Translation(GenerationDataset):
    """The dataset of Wmt dataset.

    Example:
        subset_name: ro-en
        instance: {'translation': {'en': 'Obama welcomes Netanyahu', 'ro': 'Obama primește Netanyahu'}
        prediction: Obama receives Netanyahu
        reference: Obama welcomes Netanyahu
    """

    evaluation_set = "test"
    example_set = "train"
    metrics = [Bleu()]
    instruction = ""
    load_args = ()
    extra_model_args = dict(temperature=0, stop=["\n"])

    def __init__(self, args, model, subset_name):
        self.language = Language(subset_name[3:5]).language_name("en")
        super().__init__(args, model, subset_name)

    def format_instance(self, instance):
        instance = instance["translation"]
        source_text = f"Q: Translate to {self.language}. {instance[self.subset_name[:2]]}\nA:"
        target_text = " " + instance[self.subset_name[3:5]]
        return dict(source=source_text, target=target_text)

    @staticmethod
    def post_processing(preds):
        return [pred.strip().split("\n")[0] for pred in preds]

    @property
    def references(self):
        return [instance["translation"][self.subset_name[3:]] for instance in self.evaluation_data]
