from queue import PriorityQueue
from typing import List


class DomainsCounter:

    def __init__(self):
        # the value is hardcoded for performance but can be changed
        # queue holds by count ordered for set of domains
        # 542 -> google.com, facebook.com, 434 -> yahoo.com, bing.com, 3 -> baidu.com
        # TODO add clean method for dict
        self.priority_queue = PriorityQueue(maxsize=10)
        # domain name -> count
        self.domains_counter_dict = {str: int}

    def update_domain_count(self, domain_name: str, count: int):
        prev_count = self.domains_counter_dict.get(domain_name, 0)
        new_count = prev_count + count
        self.domains_counter_dict[domain_name] = new_count
        self._update_priority_queue(domain_name=domain_name, prev_count=prev_count, new_count=new_count)

    def _update_priority_queue(self, domain_name: str, prev_count: int, new_count: int):
        domains_set: set = self.priority_queue.get(-prev_count)
        domains_set.remove(domain_name)

        updated_domains_set = self.priority_queue.get(-new_count)
        if updated_domains_set is None:
            updated_domains_set = set()
            self.priority_queue.put(-new_count, updated_domains_set)

        updated_domains_set.add(domain_name)

    def get_top_domains(self, limit: int) -> List:

        # copying for iteration 0(n) but only 10 elements
        priority_queue = self.priority_queue.copy()
        result = []
        while not priority_queue.empty():
            count, domains_set = priority_queue.get()
            for domain_name in domains_set:
                result.append({domain_name: count})
                if len(result) == limit:
                    break
            if len(result) == limit:
                break
        return result


