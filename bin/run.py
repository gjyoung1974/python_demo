#!/usr/bin/env python
import argparse
from website_form import app
from website_form.app import run_app


app = run_app()

if __name__ == "__main__":
  app.run()
