#!/usr/bin/env python
# -*- coding: utf-8; -*-
#
# This file is part of SAMS.
#
# Copyright 2020 Sourcefabric z.u. and contributors.
#
# For the full copyright and license information, please see the
# AUTHORS and LICENSE files distributed with this source code, or
# at https://www.sourcefabric.org/superdesk/license

from superdesk import blueprint
from sams.factory.app import SamsApp
from .assets import asset_binary_bp


def init_app(app: SamsApp):
    blueprint(asset_binary_bp, app)
