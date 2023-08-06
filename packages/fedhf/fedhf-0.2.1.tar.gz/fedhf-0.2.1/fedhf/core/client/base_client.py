#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   fedhf\component\client\base_client.py
@Time    :   2021-10-26 11:06:33
@Author  :   Bingjie Yan
@Email   :   bj.yan.pa@qq.com
@License :   Apache License 2.0
"""

from abc import ABC, abstractmethod

from fedhf.api import Logger
from fedhf.component import build_evaluator, build_trainer
from fedhf.model import build_criterion, build_model, build_optimizer


class AbsClient(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def train(self):
        raise NotImplementedError

    def evalute(self):
        raise NotImplementedError


class BaseClient(AbsClient):
    def __init__(self, args, client_id) -> None:
        self.args = args
        self.client_id = client_id

        self.trainer = build_trainer(self.args.trainer)(self.args)
        self.evaluator = build_evaluator(self.args.evaluator)(self.args)

        self.logger = Logger(args)
