#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def before_scenario(context, scenario):
    """Seed empty HTTP headers to steps do not need to check and create."""
    context.headers = {}
    context.data = u""
    context.query = {}