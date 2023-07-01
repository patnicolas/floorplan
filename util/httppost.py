__author__ = "Patrick Nicolas"
__copyright__ = "Copyright 2022, 23. All rights reserved."

import requests
import time
import constants
import urllib3
import logging

""""
    Simple synchronous implementation of HTTP post using JSON input_tensor line or file. The target can be defined as 
    - Fully defined URL (i.e. http://ip-10-5-47-158.us-east-2.compute.internal:8087/geminiml/predict)
    - Pre-defined targets (i.e. feedback_local)
    Command line: python $target $is_predefined_target
    Example
        python stage_predicted True input_file
        python http://ip-10-5-47-158.us-east-2.compute.internal:8087/geminiml/predict False input_file

    :param target: URL (if is_predefined_target == True) or a pre-defined
    :param headers: Header of the HTTP Post
    :param is_predefined_target: Specify if this is a predefined target (True) or a custom URL (False)
    :exception KeyError: Predefined URL is not found
"""


class HttpPost(object):
    def __init__(self, target: str, headers: list, is_predefined_target: bool = False):
        self.headers = headers
        # If this is a predefined target.
        if is_predefined_target:
            try:
                self.target = predefined_targets[target]
            except KeyError as e:
                self.target = None
                logging.error(str(e))
        # Otherwise a URL
        else:
            self.target = target

    def post_single(self, line: str) -> bool:
        """
            Process an doc_terms_str as single JSON line
            :param line: A single JSON structure
            :return: True if request successful, False otherwise
        """
        if self.target is not None:
            try:
                response = requests.post(self.target, data=line, headers=self.headers)
                logging.info("Received ML Response: {}".format(response.status_code))
                if response.status_code == 200:
                    json_response = response.json()
                    logging.info(json_response)
                    return True
                else:
                    logging.error(f'Error: {line}')
                    return False
            except urllib3.exceptions.ProtocolError as e:
                logging.error(str(e))
                return False
            except Exception as e:
                logging.error(str(e))
                return False
        else:
            return False

    # @timeit
    def post_batch(
            self,
            input_file: str,
            single_record: bool,
            num_iterations: int = 1,
            sleep_time: float = 0.2) -> (int, int):
        """
            Process a batch of JSON entries defined within a single file
            :param input_file: Input file containing the JSON formatted requests
            :param single_record: The file contains a single records
            :param num_iterations: Number of iterations (default 1)
            :param sleep_time: Number of seconds (fraction) the HTTP client thread pauses
            :return: Pair Number of success requests, Total number of requests
        """
        # start_time = time.time()
        total_count = 0
        success_count = 0
        with open(input_file) as input:
            if single_record:
                content = input.read()
                all_requests = [content.replace('\n', ' ')]
            else:
                all_requests = input.readlines()

            if all_requests:
                for _ in range(num_iterations):
                    for line in all_requests:
                        if self.post_single(line):
                            success_count += 1
                        total_count += 1
                        logging.info(f'Successes: {success_count} Count: {total_count}')
                        time.sleep(sleep_time)
        return success_count, total_count


predefined_targets = {
}

