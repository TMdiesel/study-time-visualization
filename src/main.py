# default package
import dataclasses as dc
import sys
from argparse import ArgumentParser
import logging
import typing as t

# third party package
import yaml

# my package
import analyze_activity as aa

# logger
logger=logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--config_path",default="config.yml")
    args = parser.parse_args()
    with open(args.config_path) as f:
        config=yaml.load(f,Loader=yaml.SafeLoader)

    instance=aa.analyze_activitiy(**config)
    instance.generate_df()
    instance.activity_plot()