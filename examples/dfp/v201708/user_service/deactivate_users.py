#!/usr/bin/env python
#
# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This code example deactivates a user.

Deactivated users can no longer make requests to the API. The user making the
request cannot deactivate itself. To determine which users exist, run
get_all_users.py.
"""


# Import appropriate modules from the client library.
from googleads import dfp

USER_ID = 'INSERT_USER_ID_TO_DEACTIVATE_HERE'


def main(client, user_id):
  # Initialize appropriate service.
  user_service = client.GetService('UserService', version='v201708')

  # Create query.
  statement = (dfp.StatementBuilder()
               .Where('id = :userId')
               .WithBindVariable('userId', long(user_id)))

  # Get users by statement.
  response = user_service.getUsersByStatement(statement.ToStatement())
  users = response['results'] if 'results' in response else []

  for user in users:
    print ('User with id "%s", email "%s", and status "%s" will be '
           'deactivated.'
           % (user['id'], user['email'],
              {'true': 'ACTIVE', 'false': 'INACTIVE'}[user['isActive']]))
  print 'Number of users to be deactivated: %s' % len(users)

  # Perform action.
  result = user_service.performUserAction({'xsi_type': 'DeactivateUsers'},
                                          statement.ToStatement())

  # Display results.
  if result and int(result['numChanges']) > 0:
    print 'Number of users deactivated: %s' % result['numChanges']
  else:
    print 'No users were deactivated.'


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage()
  main(dfp_client, USER_ID)
