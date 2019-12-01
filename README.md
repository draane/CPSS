# C Projects Security Scanner
_CPSS_ is a tool that automatically scans GitHub for projects written in _C_ and perform static analysis on the code.

## Installation
_CPSS_ requires `cppcheck` to be installed on the system. Also `docker-compose` is used to manage a _RabbitMQ_ instance.

Install the required Python libraries with `pip install -r requirements.txt`.

## Run
- Start the RabbitMQ server using docker-compose: `docker-compose up rabbitmq`. The docker-compose file is in the directory `services`.
- Execute `python github.py` to insert repositories in the queue.
- Execute `python cpss.py` to analyze the repositories in the queue.

Once the analysis is done, the reports can been cleaned up by running the script `report_processing.py`. The final reports will be in the `clean_reports` directory.
