import logging
import time

import click

from .utils import (
    current_user_is_root,
    is_service_running,
    restart_service,
)


__version__ = '0.0.1'
__all__ = ['aws_watchdog', 'aws_watchdog_daemon']


logger = logging.getLogger(__name__)


test_config = {
    'Id': 1,
    'ListOfServices': ['docker', 'ufw'],
    'NumOfSecCheck': 5,
    'NumOfSecWait': 5,
    'NumOfAttempts': 4,
}


def aws_watchdog(config_id):
    """AWS watchdog function. Health check for your services."""
    # TODO: each service checks should be in different process to do thins in
    # parallel and get proper waithing times. use multiprocessing
    # TODO: consider selfhealing of aws_watchdog
    # TODO: systemd service

    # TODO: Config class która będzie pobierać z DynamoDb, walidować, wypluwać
    # nam configi, update co 15minut.
    # TODO: logowanie do s3 (logging) i do SNS (konkretne zdarzenia - down,
    # success after, failture after)
    # TODO: README, instalacje opisać
    while True:
        for service in test_config['ListOfServices']:

            if not is_service_running(service):
                logger.error('{} is down.'.format(service))

                for attempt in range(1, test_config['NumOfAttempts']+1):
                    logger.info(
                        'Restarting {}. Attempt {}'.format(service, attempt)
                    )
                    restart_command_exit_code = restart_service(service)
                    if restart_command_exit_code == 0:
                        logger.info(
                            'Success of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                        break
                    if attempt == test_config['NumOfAttempts']:
                        logger.error(
                            'Failure of restarting {}. On {} attempt.'.format(
                                service,
                                attempt,
                            )
                        )
                    time.sleep(test_config['NumOfSecWait'])

        time.sleep(test_config['NumOfSecCheck'])


@click.command()
@click.option(
    '--config-id',
    default=1,
    help='ID of config entry in DynamoDB (default is 1)',
)
def aws_watchdog_daemon(config_id):
    logger.info(
        'Starting AWS watchdog daemon. (PID )'.format()
    )
    if current_user_is_root():
        logger.warn('Running things as root can be dangerous !!')

    aws_watchdog(config_id)
