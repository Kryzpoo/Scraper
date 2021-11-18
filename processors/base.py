import logging
from abc import ABC
from concurrent import futures
from typing import List, Tuple

log = logging.getLogger('scraper')


class BaseProcessor(ABC):

    MAX_WORKERS = 1

    def get_data_one(self, data_unit) -> Tuple[str, str, dict, list]:
        pass

    def process(self, data_set) -> List[Tuple[str, str, dict, list]]:
        # Processing with ThreadPoolExecutor
        result = []
        with futures.ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            to_do_map = {}

            # Creating futures
            for data_unit in data_set:
                future = executor.submit(self.get_data_one, data_unit)
                to_do_map[future] = data_unit

            # Processing futures
            done_iter = futures.as_completed(to_do_map)
            for future in done_iter:
                try:
                    result.append(future.result())
                except Exception as e:
                    log.error(e, exc_info=True)
        return result

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass
