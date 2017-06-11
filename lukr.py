#!/usr/bin/env python3

import lukr_manager
import fire

if __name__ == '__main__':
    manager = lukr_manager.LukrManager()
    fire.Fire(manager)
