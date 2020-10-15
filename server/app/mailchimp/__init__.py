"""This package contains all of the modules for interacting with the MailChimp API."""

# Campaigns
# client.campaigns.create(data={})
# client.campaigns.all(get_all=False)
# client.campaigns.get(campaign_id='')
# client.campaigns.update(campaign_id='')
# client.campaigns.delete(campaign_id='')

# # Campaign actions
# client.campaigns.actions.schedule(campaign_id='', data={})
# client.campaigns.actions.send(campaign_id='')
# client.campaigns.actions.test(campaign_id='', data={})
# client.campaigns.actions.unschedule(campaign_id='')

# Lists
# client.lists.create(data={})
# client.lists.update_members(list_id='', data={})
# client.lists.all(get_all=False)
# client.lists.get(list_id='')
# client.lists.update(list_id='', data={})
# client.lists.delete(list_id='')

# List Members
# client.lists.members.create(list_id='', data={})
# client.lists.members.all(list_id='', get_all=False)
# client.lists.members.get(list_id='', subscriber_hash='')
# client.lists.members.up
# date(list_id='', subscriber_hash='', data={})
# client.lists.members.create_or_update(list_id='', subscriber_hash='', data={})
# client.lists.members.delete(list_id='', subscriber_hash='')
# client.lists.members.delete_permanent(list_id='', subscriber_hash='')


# #Campaign Content
# client.campaigns.content.get(campaign_id='')
# client.campaigns.content.update(campaign_id='', data={})

# Reports
# client.reports.all(get_all=False)
# client.reports.get(campaign_id='')


# My requirements
# Create, read, update and delete a campaign
# Add content, read content, and update content in a campaign
# Send, schedule, and unschedule a campaign
# Send images to be used in the content
# Read data about the campaign
# Read, create, update, and delete member lists (figure this out later)
# Choose which list to send to for each campaign

