# -*- coding: utf-8 -*-
#
# Author:        alisue
# Date:            2010/12/01
#
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from ...utils import pull_tweet_from_twitter

class Command(BaseCommand):
    help = u"""Pull tweets from twitter with `profile.twitter_token` and put to tweets.tweet"""
    
    def handle(self, *labels, **options):
        if not labels:
            output = [self.handle_noargs(**options)]
        else:
            output = []
            for label in labels:
                label_output = self.handle_label(label, **options)
                if label_output:
                    output.append(label_output)
        return '\n'.join(output)

    def handle_user(self, user, **options):
        try:
            result = pull_tweet_from_twitter(user)
        except:
            result = None
        output = ""
        if result:
            if options['verbosity'] != 0:
                output = "%d tweets has pulled for %s" % (len(result), user.username)
        else:
            if options['verbosity'] == 2:
                output = "Skipped: %s" % user.username
        return output
    
    def handle_label(self, label, **options):
        user = User.objects.get(username=label)
        return self.handle_user(user, **options)
    
    def handle_noargs(self, **options):
        users = User.objects.filter(is_active=True).exclude(profile__twitter_token='')
        output = []
        for user in users:
            _output = self.handle_user(user, **options)
            if _output:
                output.append(_output)
        return "\n".join(output)
