import os
import praw
import argparse
import random
import string
import sys
import time

__version__ = '0.2.0'

def id_generator(size = 16, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def get_args(argv):
    """get args.
    Args:
        argv (list): List of arguments.
    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description=("Votes on a user's Reddit posts")
    )

    parser.add_argument("-c", "--client-id", help="pass in client id as argument", type=str)
    parser.add_argument("-s", "--client-secret", help="pass in client secret as argument", type=str)
    parser.add_argument("-u", "--username", help="pass in client secret as argument", type=str)
    parser.add_argument("-p", "--password", help="pass in client secret as argument", type=str)

    parser.add_argument("-P", "--profile", help="pass in profile as argument", type=str)
    parser.add_argument("-l", "--limit", help="pass in limit as argument", type=str)

    parser.add_argument("-up", "--upvote", help="upvote user posts", action="store_true")
    parser.add_argument("-down", "--downvote", help="downvote user posts", action="store_true")
    
    parser.add_argument("-v", "--version", help="get program version.", action="store_true")

    args = parser.parse_args(argv)
    return args

def login(args):
    """login method.

    Args:
        args (argparse.Namespace): Parsed arguments.

    Returns: a logged on praw instance
    """

    try:
        reddit = praw.Reddit(
            user_agent=id_generator(),
            client_id=args.client_id,
            client_secret=args.client_secret,
            username=args.username,
            password=args.password
        )
        return reddit
    except Exception as e:
        print("\033[1;31;40mLogin Failed \033[1;37;40m")
        print(e)
        sys.exit(0)

def vote(reddit, args):
    counter = 0
    profile = reddit.redditor(args.profile)
    limit = int(args.limit) if args.limit else int(25)
    list = profile.comments.new(limit=limit)
    for comment in list:
        time.sleep(0.5)
        counter += 1
        print('\033[1;34;40m[VOTING] ' + str(args.profile) + ' (' + str(counter) + ' / ' + str(limit) + ')\033[1;37;40m \n')
        print(str(comment.body) + '\n')
        print('(r/' + str(comment.subreddit) + ')\n')
        if args.downvote:
            downvote(comment)
        elif args.upvote:
            upvote(comment)
    label = str("Downvoted ") if args.downvote else str("Upvoted ")
    print ('\033[1;32;40m[SUCCESS] ' + str(label) + str(counter) + ' of u/' + str(profile) + '\'s comments. \033[1;37;40m \n')
    return 0

def main():
    """main func."""
    args = get_args(sys.argv[1:])

    # print program version.
    if args.version:
        print(__version__)
        sys.exit(0)

    print('---RedditBot---')

    if args.upvote or args.downvote and args.client_id and args.client_secret and args.username and args.password and args.profile:
        reddit = login(args=args)
        vote(reddit, args)
    else:
        print("\033[1;31;40mYou'll need to pass a client-id (-c), client-secret (-s), username (-u), password (-p) and profile (-P).\033[1;37;40m")

    sys.exit(0)

if __name__ == "__main__":  # pragma: no cover
    main()