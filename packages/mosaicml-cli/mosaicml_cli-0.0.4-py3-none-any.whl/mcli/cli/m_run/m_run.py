""" mcli run Entrypoint """
import argparse
import json
import logging
from typing import Any, Dict, Optional

from mcli.models.run import RunModel
from mcli.runs import pipeline

log = logging.getLogger(__name__)


def run(
    file: Optional[str] = None,
    name: Optional[str] = None,
    instance: Optional[str] = None,
    image: Optional[str] = None,
    git_repo: Optional[str] = None,
    git_branch: Optional[str] = None,
    model: Optional[str] = None,
    command: Optional[str] = None,
    parameters: Optional[Dict[str, Any]] = None,
    dry_run: Optional[bool] = False,
    **kwargs,
) -> int:
    del kwargs
    print('The entrypoint for mosaic run!')

    # convert the args to a list of partial run models
    partial_run_model = pipeline.create_partial_run_models(
        file=file,
        name=name,
        instance=instance,
        image=image,
        git_repo=git_repo,
        git_branch=git_branch,
        model=model,
        command=command,
        parameters=parameters,
    )

    # merge the partial run models into a single complete run model
    run_model = RunModel.from_partial_run_model(partial_run_model)

    # convert the run model into a mcli job object
    mcli_job = pipeline.mcli_job_from_run_model(run_model)

    if dry_run:
        log.info(f'Generated RunModel {run_model} and MCLIJob {mcli_job}')
    else:
        # submit the job - logic within here will eventually be moved server-side
        pipeline.submit_mcli_job(mcli_job, run_model)

    return 0


def add_run_argparser(subparser: argparse._SubParsersAction) -> None:
    run_parser: argparse.ArgumentParser = subparser.add_parser(
        'run',
        aliases=['r'],
        help='Run stuff',
    )
    run_parser.set_defaults(func=run)
    _configure_parser(run_parser)


def _configure_parser(parser: argparse.ArgumentParser):
    parser.add_argument('-f',
                        '--file',
                        dest='file',
                        help='File from which to load arguments.'
                        'Arguments present in the file can be overridden by the command line.')
    parser.add_argument('--name', dest='name', help='Run name')
    parser.add_argument('--instance', dest='instance', help='The instance to run on.')
    parser.add_argument('--image', dest='image', help='Docker image to use')
    parser.add_argument('--git-repo', dest='git_repo', help='Which repo to clone')
    parser.add_argument('--git-branch', dest='git_branch', help='Commit/branch/tag to use in the clone')
    parser.add_argument('-m', '--model', dest='model', default=None, help='Model to run')
    parser.add_argument('--command', dest='command', nargs='+', help='Command to use for each run group')
    parser.add_argument('-p',
                        '--parameters',
                        dest='parameters',
                        default=None,
                        type=json.loads,
                        help='Default parameters to include in every run in JSON format')
    parser.add_argument('--dry-run',
                        dest='dry_run',
                        action='store_true',
                        help='Do not submit any runs, just generate run configs')
