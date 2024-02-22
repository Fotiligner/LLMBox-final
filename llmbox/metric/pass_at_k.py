import itertools
from typing import List, Union
import numpy as np

from .metric import Metric
from ..dataset.gsm8k import Timeout

class PassAtK(Metric):
    r""" Calculate the Pass@K score.

    Return:
        # TODO:RETURN

    """

    def __call__(self, predictions, references):
        result = []
        for pred, refer in zip(predictions, references):
            code = pred + "\n" + "\n".join(references["test_list"])
            with Timeout():
                try:
                    exec(code)
                    result.append('passed')
                except TimeoutError:
                    result.append("timed out")
                except AssertionError:
                    result.append(f"failed: AssertionError")
                except BaseException as e:
                    result.append(f"failed: {e}")


    def estimate_pass_at_k(
            num_samples: Union[int, List[int], np.ndarray],
            num_correct: Union[List[int], np.ndarray],
            k: int
    ) -> np.ndarray:
        """
        Estimates pass@k of each problem and returns them in an array.
        """

        def estimator(n: int, c: int, k: int) -> float:
            """
            Calculates 1 - comb(n - c, k) / comb(n, k).
            """
            if n - c < k:
                return 1.0
            return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

        if isinstance(num_samples, int):
            num_samples_it = itertools.repeat(num_samples, len(num_correct))
        else:
            assert len(num_samples) == len(num_correct)
            num_samples_it = iter(num_samples)

        return np.array([estimator(int(n), int(c), k) for n, c in zip(num_samples_it, num_correct)])