# -*- coding: utf-8 -*-
import logging
import requests
from slack import WebClient

LOGGER = logging.getLogger(__name__)
logging.getLogger('slack.web.slack_response').setLevel(logging.INFO)


class Slack(object):
    def __init__(self, token=None):
        self.client = WebClient(token)

    @staticmethod
    def notify(webhook_url, **kwargs):
        if not kwargs.get('text') and not kwargs.get('attachments'):
            raise ValueError('text or attachments parameters is required')

        LOGGER.debug(kwargs)

        response = requests.post(webhook_url, json=kwargs)
        if response.status_code != 200:
            raise ValueError('Request to slack returned an errors {0}, the response is: {1}'.format(
                response.status_code, response.text))

        return response.text

    def api_call(self, method, timeout=None, **kwargs):
        response = self.client.api_call(method, json=dict(**kwargs))
        if not response.get('ok'):
            LOGGER.error('slack api_call {0} error'.format(method))

        return response

    def users(self):
        response = self.api_call('users.list')

        users = []
        for member in response.get('members', []):
            profile = member.get('profile', {})
            if not member.get('is_bot'):
                real_name = "%s %s" % (profile.get('first_name', ''), profile.get('last_name', ''))
                users.append({
                    'id': member.get('id'),
                    'name': member.get('name'),
                    'email': profile.get('email'),
                    'display_name': profile.get('display_name'),
                    'real_name': real_name,
                    'title': profile.get('title'),
                    'skype': profile.get('skype'),
                    'phone': profile.get('phone'),
                    'image': profile.get('image_72'),
                    'deleted': member.get('deleted')
                })

        return users
    
    def channels(self):
        channels = self.api_call('channels.list', exclude_archived=True).get('channels', [])
        LOGGER.debug('{0} channels'.format(len(channels)))
        groups = self.api_call('groups.list', exclude_archived=True).get('groups', [])
        LOGGER.debug('{0} groups'.format(len(groups)))

        return channels + groups

    def channel_members(self, channel_name):
        users = self.users()
        channels = self.channels()

        channel = next((item for item in channels if item['name'] == channel_name.lstrip('#').lstrip('@')), {})

        members = []
        for member in channel.get('members', []):
            user = next((item for item in users if item['id'] == member), None)
            if user:
                members.append(user)
        
        return members
    
    def im_channels(self, slack_ids=[], make_channel=True):
        im_list = self.api_call('im.list', exclude_archived=True)
        
        user_channels = dict()

        if not slack_ids:
            for channel in im_list.get('ims', []):
                user_channels[channel['user']] = channel['id']

        for slack_id in slack_ids if isinstance(slack_ids, list) else [slack_ids]:
            user_channel = None
            for channel in im_list.get('ims'):
                if channel.get('user') == slack_id:
                    user_channel = channel.get('id')

            # 채널 정보가 없으면 im.open을 통해서 오픈하고, 새로 생성된 채널 id 를 넘겨준다
            if not user_channel and make_channel:
                response = self.api_call('im.open', user=slack_id)
                user_channel = response.get('channel').get('id')

            user_channels[slack_id] = user_channel

        return user_channels
