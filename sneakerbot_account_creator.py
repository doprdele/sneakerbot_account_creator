#/usr/bin/env python

import json
import random
import itertools

def ncycle(iterable, n):
  for item in itertools.cycle(iterable):
    for i in range(n):
      yield item

from argparse import ArgumentParser

def dot_trick(username,domain='e'):
    emails = list()
    username_length = len(username)
    combinations = pow(2, username_length - 1)
    padding = "{0:0" + str(username_length - 1) + "b}"
    for i in range(0, combinations):
        bin = padding.format(i)
        full_email = ""

        for j in range(0, username_length - 1):
            full_email += (username[j]);
            if bin[j] == "1":
                full_email += "."
        full_email += (username[j + 1])
        emails.append(full_email + "@" + domain)
    return emails

def create_record(guest, sitetype, password, email, size, links, keywords, notificationemail,
    ccprofile, only_new, checkoutdelay):

    __links__ = [] if links == None else [links]
    __keywords__ = [] if keywords == None else keywords
    __password__ = password if password else ''

    return {
            u"\u0018": False,
            'EmailAddress': email,
            'Password': __password__,
            'Size': [size],
            'Links': __links__,
            'Keywords' : __keywords__,
            'NotificationEmail' : email,
            'NotificationText': None,
            'SiteType': sitetype,
            'IsGuest': guest,
            'Disabled': False,
            'CheckoutInfo': {
                'PayPalCheckout': False,
                'CcCheckout': True,
                'FinalizeOrder': True,
                'PayPalEmailAddress': '',
                'PayPalPassword': '',
                'CcProfile': ccprofile,
                },
            'OnlyNewSupremeProducts': only_new,
            'CheckoutDelay': checkoutdelay,
            'Quantity': 1
            }

parser = ArgumentParser(
        description="Create BNB accounts"
        )

parser.add_argument('--sitetype', help='Supreme or Adidas', type=str,
    required=True)

parser.add_argument('--guest', help='Use guest accounts',
    action='store_true', default=False)

parser.add_argument('--password', type=str,
    default=None,
    required=False,
    help='Account(s) password'
    )

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument('--email', help='Email for guest accounts',
        type=str)

group.add_argument('--accountsfile', help='Text file listing account email addresses', type=str)

parser.add_argument('--sizes', type=str, nargs='*', required=True,
        metavar=('Size1', 'Size2'),
        help='Sizes to create accounts for')

parser.add_argument('--ccprofiles', type=str, nargs='*', required=True,
        metavar=('CCProfile1', 'CCProfile2'),
        help='CC Profiles')

parser.add_argument('--checkout-delays', type=int, nargs='*',
        required=True,
        default=6000,
        metavar=('Delay1', 'Delay2'),
        help='Checkout Delays')

parser.add_argument('--only-new-products', action='store_true',
    default=True,
    help='Check for only new products in Supreme', required=False)

parser.add_argument('--num', type=int, required=True,
        help='Number of accounts to create',
        )

parser.add_argument('--keywords', type=str, nargs='*',
        default=[],
        metavar=('Keyword1', 'Keyword2'),
        help='Keywords for Supreme')

parser.add_argument('--link', type=str, help='Early link', required=True)

args = parser.parse_args()

#####

generated_emails = []

if args.guest:
  generated_emails = (dot_trick(*args.email.split('@')))[:args.num]

  if len(generated_emails) < args.num:
    base_email = random.choice(generated_emails)
    i = 1
    while len(generated_emails) < args.num:
      email,domain = base_email.split('@')
      generated_emails.append("{0}+{1}@{2}".format(email,i,domain))
      i = i + 1
elif args.guest == False and args.accountsfile:
  with open(args.accountsfile, 'r') as accts:
    generated_emails = map(lambda l: l.rstrip(), accts.readlines())
else:
  print "--accountsfile is required if not using guest accounts."
  exit(1)

ccprofiles = ncycle(args.ccprofiles, 1)
checkoutdelays = ncycle(args.checkout_delays, 1)
sizes = ncycle(args.sizes, 1)
links = args.link
keywords = args.keywords
json_doc = []
sitetype = None

if args.sitetype.lower() == "adidas":
  sitetype = 6
elif args.sitetype.lower() == "supreme":
  sitetype = 5
elif args.sitetype.lower() == "barneys":
  sitetype = 13
elif args.sitetype.lower() == "kithnyc":
  sitetype = 30
elif args.sitetype.lower() == "bodega":
  sitetype = 35
elif args.sitetype.lower() == "yeezysupply":
  sitetype = 34
elif args.sitetype.lower() == "size":
  sitetype = 46
elif args.sitetype.lower() == "footlocker":
  sitetype = 1
elif args.sitetype.lower() == "eastbay":
  sitetype = 0
elif args.sitetype.lower() == "champs":
  sitetype = 3
elif args.sitetype.lower() == "footaction":
  sitetype = 2
else:
  print "Supported --sitetype arguments are Adidas,Supreme,Barneys,KithNYC"
  exit(1)

for email in generated_emails:
  json_doc.append(create_record(args.guest, sitetype, args.password, email, sizes.next(), links, keywords, email, ccprofiles.next(),
    args.only_new_products, checkoutdelays.next()))

print json.dumps(json_doc, indent=4, separators=(',', ': '))
