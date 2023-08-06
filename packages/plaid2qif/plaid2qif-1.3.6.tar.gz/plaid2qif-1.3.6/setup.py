# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plaid2qif']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'plaid-python>=7.2.0,<8.0.0',
 'python-dateutil>=2.8.1,<3.0.0']

entry_points = \
{'console_scripts': ['plaid2qif = plaid2qif.plaid2qif:main']}

setup_kwargs = {
    'name': 'plaid2qif',
    'version': '1.3.6',
    'description': 'Download financial transactions from Plaid as QIF files.',
    'long_description': '[![CircleCI](https://circleci.com/gh/ebridges/plaid2qif/tree/master.svg?style=svg)](https://circleci.com/gh/ebridges/plaid2qif/tree/master)\n\n### Description\n\nProvides a mechanism for downloading transactions from various financial institutions (as supported by [Plaid](https://www.plaid.com)), and converts to formats (specifically QIF & CSV, but extensible) usable by financial software (especially GNUCash).\n\n### Summary\n\n```\n  # Save a long-lived access token (one-time only)\n  plaid2qif save-access-token --institution=<name> --public-token=<token> --credentials=<file> [--verbose]\n\n  # List out accunts that have been linked to Plaid\n  plaid2qif list-accounts --institution=<name> --credentials=<file> [--verbose]\n\n  # Download transactions in various formats (default QIF) from Plaid\n  plaid2qif download \\\n    --institution=<name> \\\n    --account=<account-name> \\\n    --account-type=<type> \\\n    --account-id=<acct-id> \\\n    --from=<from-date> \\\n    --to=<to-date> \\\n    --credentials=<file> \\\n    [--output-format=<format>] \\\n    [--output-dir=<path>] \\\n    [--ignore-pending] \\\n    [--verbose]\n```\n\n### Usage\n\n1. Install the `plaid2qif` command using `pip`\n\n```\n$ pip install plaid2qif\n```\n\n2. Authenticate and link with your financial institution (first time only) -- see "Authentication Prerequisites" below.\n\n3. Once you\'ve gotten that configured, you\'re ready to download transactions and save them as QIF files:\n\n```\nplaid2qif download \\\n    --from=<yyyy-mm-dd> \\\n    --to=<yyyy-mm-dd> \\\n    --institution=<name> \\\n    --account-type=<type> \\\n    --account=<account-name> \\\n    --account-id=<plaid-account-id> \\\n    --credentials=<file>\n```\n\n  * `account` is the path to an account in the ledger in GnuCash that you ultimately want to import the transactions to.  This is added to the `!Account` header in the QIF file.  e.g.: `Assets: Checking Accounts:Personal Checking Account`.  If the name has spaces be sure to quote this param.\n  * `account-type` is an account identifier type as [documented here](https://github.com/Gnucash/gnucash/blob/cdb764fec525642bbe85dd5a0a49ec967c55f089/gnucash/import-export/qif-imp/file-format.txt#L23).\n  * `account-id` is Plaid\'s account ID for the account you want to download, as obtained via `list-accounts` above.\n  * By default, output will go to stdout to be redirected.  If you want it to be written to a location use the `output-dir` parameter.\n\n### Authentication Prerequisites\n\n* Obtain and save your own personal credentials for Plaid to a local file, e.g. `./plaid-credentials.json`. This JSON file should contain values for the following keys:\n```\n    {\n      "client_id" : "<censored>",\n      "public_key" : "<censored>",\n      "secret" : "<censored>"\n    }\n```\n* Create a `./cfg` directory for institution configuration data to be stored in.\n* Authenticate with your Financial Institution.\n\n#### Steps to Authenticate with your Financial Institution\n\n1. Save this HTML locally, e.g. as `auth.html`\n\n```\n<html>\n<body>\n<button id=\'linkButton\'>Open Link - Institution Select</button>\n<script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>\n<script>\n  var linkHandler = Plaid.create({\n    env: \'development\',\n    clientName: \'Plaid2QIF\',\n    key: \'[PUBLIC_KEY]\', // Replace with your public_key from plaid-credentials.json\n    product: \'transactions\',\n    apiVersion: \'v2\',\n    onLoad: function() {\n      // The Link module finished loading.\n    },\n    onSuccess: function(public_token, metadata) {\n      // Send the public_token to your app server here.\n      // The metadata object contains info about the institution the\n      // user selected and the account ID, if selectAccount is enabled.\n      console.log(\'public_token: \'+public_token+\', metadata: \'+JSON.stringify(metadata));\n    },\n    onExit: function(err, metadata) {\n      // The user exited the Link flow.\n      if (err != null) {\n        // The user encountered a Plaid API error prior to exiting.\n      }\n      // metadata contains information about the institution\n      // that the user selected and the most recent API request IDs.\n      // Storing this information can be helpful for support.\n    }\n  });\n\n  // Trigger the standard institution select view\n  document.getElementById(\'linkButton\').onclick = function() {\n    linkHandler.open();\n  };\n</script>\n</body>\n</html>\n```\n\n2. Open a web server on the root directory and open `auth.html`\n\n```\n$ python3 -m http.server\n$ open auth.html # edit first to add the public token from plaid-credentials.json\n```\n\n3. Follow [instructions here](https://plaid.com/docs/quickstart/#creating-items-with-link-and-the-api) to use the UI to link your financial institution to Plaid.\n\n4. Once you\'ve succesfully linked, look in the browser\'s console (e.g. on Chrome use `⌘-⌥-i`) and copy the `public_token`.  The `public_token` is a short lived credential.\n\n5. Using the `public_token`, generate and save a long-lived `access_token` credential:\n\n```\n$ plaid2qif save-access-token --institution=<name> --public-token=<token> --credentials=<plaid-credentials-file>\n```\n\n  * `institution` should be a string that can be used as a valid (i.e.: `[a-zA-Z0-9_]`) filename, used to store the `access_token`.\n\n6. List the accounts connected with this institution in order to get Plaid\'s `account_id`:\n\n```\n$ plaid2qif list-accounts --institution=<name> --credentials=<plaid-credentials-file>\n```\n\n### Distribution\n\n```\n# increment version in `plaid2qif/__init__.py`\n# commit everything & push\n$ git tag -s vX.Y.Z\n$ git push --tags\n$ python3 setup.py sdist bdist_wheel\n$ twine upload dist/*\n```\n\n[![GitHub watchers](https://img.shields.io/github/watchers/badges/shields.svg?style=social&label=Watch&style=flat-square)]()\n[![Crates.io](https://img.shields.io/crates/l/rustc-serialize.svg?style=flat-square)]()\n[![PyPi](https://img.shields.io/pypi/v/plaid2qif.svg?style=flat-square)]()\n',
    'author': 'Edward Q. Bridges',
    'author_email': 'github@eqbridges.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ebridges/plaid2qif',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
