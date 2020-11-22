# name-orginer
## Introduction
1. Get each Google search results count
2. Save the name and count as csv sorted by count
3. Try to get name origins (e.g. Greek, Hebrew) from any online source you prefer (for example behindthename.com), and generate a csv of origin with number of occurrences. Sort by number of occurrences.

## The behindname API Key
To use the behindthename service, you must get an API (https://www.behindthename.com/api/)

## Create your service account
1. Sign in to the Google API Console.
2. Open the Credentials page. If prompted, select the project that has the Android Management API enabled.
3. Click Create credentials > Service account key.
4. From the dropdown menu, select New service account. Enter a name for your service account.
5. Select your preferred key type and click Create. Your new public/private key pair is generated and downloaded to your machine and is the only copy of this key. You are responsible for storing it securely.
6. (Optional, but highly recommended) Add additional project owners by granting the Owner role to existing project members.

## Install packages
pip install

## run this script
This script supports two commands.
1. python run.py -f mock.txt
2. python run.py -s "name1, name2..."