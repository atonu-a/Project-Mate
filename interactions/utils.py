def attach_comment_tree(project):
    comments_by_parent = {}

    for comment in project.all_comments:
        comment.prefetched_replies = []
        comments_by_parent.setdefault(comment.parent_id, []).append(comment)

    for comment in project.all_comments:
        comment.prefetched_replies = comments_by_parent.get(comment.id, [])

    project.prefetched_comments = sorted(
        comments_by_parent.get(None, []),
        key=lambda comment: comment.created_at,
        reverse=True,
    )
