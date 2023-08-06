import time

from werkzeug.exceptions import NotFound

from biolib.typing_utils import Dict, List
from biolib.compute_node.webserver.worker_thread import WorkerThread


JOB_ID_TO_COMPUTE_STATE_DICT: Dict = {}
UNASSIGNED_COMPUTE_PROCESSES: List = []


def get_job_compute_state_or_404(job_id: str):
    compute_state = JOB_ID_TO_COMPUTE_STATE_DICT.get(job_id)
    if compute_state:
        return compute_state

    raise NotFound('Job not found')


def get_compute_state(unassigned_compute_processes):
    if len(unassigned_compute_processes) == 0:
        start_compute_process(unassigned_compute_processes)

    return unassigned_compute_processes.pop()


def start_compute_process(unassigned_compute_processes):
    compute_state = {
        'job_id': None,
        'cloud_job_id': None,
        'status': {
            'status_updates': [
                {
                    'progress': 10,
                    'log_message': 'Initializing'
                }
            ],
            'stdout_and_stderr_packages_b64': []
        },
        'progress': 0,
        'result': None,
        'attestation_document': b'',
        'received_messages_queue': None,
        'messages_to_send_queue': None,
        'worker_process': None
    }

    WorkerThread(compute_state).start()

    while True:
        if compute_state['attestation_document']:
            break
        time.sleep(0.25)

    unassigned_compute_processes.append(compute_state)


def validate_saved_job(saved_job):
    if 'app_version' not in saved_job['job']:
        return False

    if 'access_token' not in saved_job:
        return False

    if 'module_name' not in saved_job:
        return False

    return True
