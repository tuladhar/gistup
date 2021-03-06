#!/usr/bin/env python

#
# CLI tool to upload file to GIST using Github API
# By Puru Tuladhar
#

import os
import sys
import json
import urllib.request
import argparse

def parse_args():
  parser = argparse.ArgumentParser(description='CLI tool to upload file to GIST using Github API')
  parser.add_argument('-f', '--filename', dest='filename')
  parser.add_argument('-d', '--description', dest='description', default=None, help='optional description')
  parser.add_argument('-t', '--token', dest='token', help='personal access token generated from your github account')
  parser.add_argument('--public', dest='public', action='store_true', default=False, help='toggle to make this gist available publicly')
  return parser.parse_args()

def upload(token, filename, description, make_public):
  description = description if description else 'uploaded via gistup.py (https://github.com/tuladhar/gistup)'
  content = open(filename, 'r').read()
  post =  json.dumps({
    'description': description,
    'public': make_public,
    'files': {
      filename: {
        'content': content
      }
    }
  })
  post = str(post).encode('utf-8')
  try:
    api_url = 'https://api.github.com/gists'
    req = urllib.request.Request(url=api_url, headers={'Authorization': 'token '+token}, data=post)
    res = urllib.request.urlopen(req)
    url = json.loads(res.read())
    print(url['html_url'])
  except Exception as upload_error:
    print(upload_error)
    sys.exit(1)

def main():
  args = parse_args()

  filename = args.filename
  description = args.description
  token = args.token
  make_public = args.public
  if not os.path.exists(filename):
    print('file not found: {}'.format(filename))
    sys.exit(1)

  upload(token, filename, description, make_public)
  sys.exit(0)

if __name__ == '__main__':
  main()
